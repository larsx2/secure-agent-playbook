"""Exercise the webhook example offline; never send requests or run a target."""
import ast
import hashlib
import hmac
import json
import re
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

PLAY = Path(__file__).resolve().parents[1] / 'plugins/code-security-skills/plays/api-security-review.md'


def webhook_verifier():
    for block in re.findall(r'^```python\n(.*?)^```[ \t]*$', PLAY.read_text(), re.S | re.M):
        if 'def verify_webhook(' not in block:
            continue
        tree = ast.parse(block)
        function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'verify_webhook')
        # Compile only this example function, not adjacent examples or imports.
        namespace = dict(hmac=hmac, hashlib=hashlib, json=json, re=re, time=time)
        exec(compile(ast.Module(body=[function], type_ignores=[]), str(PLAY), 'exec'), namespace)
        return namespace['verify_webhook']
    raise AssertionError('Webhook example missing')


class ReplayStore:
    """Offline stateful substitute for Redis SET NX EX."""
    def __init__(self):
        self.entries = {}
        self.clock = None  # optional independent clock; defaults to time.time()

    def set(self, key, value, *, nx, ex):
        now = self.clock() if self.clock else time.time()
        if nx and self.entries.get(key, 0) > now:
            return False
        self.entries[key] = now + ex
        return True


class WebhookExampleTests(unittest.TestCase):
    def setUp(self):
        self.verify = webhook_verifier()
        self.secret = b'offline-test-key-not-a-credential'
        self.store = ReplayStore()
        self.now = 1700000000
        self.request = SimpleNamespace(body=b'{"event":"example"}', headers={
            'X-Webhook-Timestamp': str(self.now),
            'X-Webhook-Nonce': 'offline_fixture_nonce',
        })
        self.sign()

    def sign(self):
        prefix = json.dumps([
            self.request.headers['X-Webhook-Timestamp'],
            self.request.headers['X-Webhook-Nonce'],
        ], separators=(',', ':')).encode()
        self.request.headers['X-Webhook-Signature'] = hmac.new(
            self.secret, prefix + b'\n' + self.request.body, hashlib.sha256
        ).hexdigest()

    def check(self):
        return self.verify(self.request, self.secret, self.store, 'configured-sender')

    def test_valid_signature_is_accepted_once(self):
        with patch('time.time', return_value=self.now):
            self.assertTrue(self.check())
            with self.assertRaises(ValueError):
                self.check()

    def test_body_timestamp_and_nonce_are_all_authenticated(self):
        for field in ('body', 'X-Webhook-Timestamp', 'X-Webhook-Nonce'):
            with self.subTest(field=field):
                self.setUp()
                if field == 'body':
                    self.request.body = b'{"event":"altered"}'
                elif field == 'X-Webhook-Timestamp':
                    self.request.headers[field] = str(self.now + 1)
                else:
                    self.request.headers[field] = 'different_fixture_nonce'
                with patch('time.time', return_value=self.now):
                    with self.assertRaises(ValueError):
                        self.check()
                self.assertEqual(self.store.entries, {})

    def test_signed_stale_or_future_timestamps_are_rejected(self):
        for offset in (-301, 301):
            with self.subTest(offset=offset):
                self.request.headers['X-Webhook-Timestamp'] = str(self.now + offset)
                self.sign()
                with patch('time.time', return_value=self.now):
                    with self.assertRaises(ValueError):
                        self.check()

    def test_future_dated_request_cannot_replay_at_end_of_acceptance_window(self):
        self.request.headers['X-Webhook-Timestamp'] = str(self.now + 300)
        self.sign()
        with patch('time.time', return_value=self.now):
            self.assertTrue(self.check())
        with patch('time.time', return_value=self.now + 600):
            with self.assertRaises(ValueError):
                self.check()

    def test_replay_rejected_on_node_lagging_by_max_clock_skew(self):
        # The shared store keeps real time; receiver nodes may lag it by up to
        # the documented 30s skew.
        real_time = [self.now]
        self.store.clock = lambda: real_time[0]
        self.request.headers['X-Webhook-Timestamp'] = str(self.now + 300)
        self.sign()
        with patch('time.time', return_value=self.now):  # accurate node
            self.assertTrue(self.check())
        # 630s later, a node 30s behind still sees the timestamp as in-window,
        # so only the shared nonce claim can reject the replay.
        real_time[0] = self.now + 630
        with patch('time.time', return_value=real_time[0] - 30):
            with self.assertRaisesRegex(ValueError, 'Replayed'):
                self.check()

    def test_retry_after_handler_failure_requires_fresh_nonce(self):
        with patch('time.time', return_value=self.now):
            self.assertTrue(self.check())
        # Handler failed; resending the identical signed request is a replay.
        with patch('time.time', return_value=self.now + 5):
            with self.assertRaises(ValueError):
                self.check()
            self.request.headers['X-Webhook-Timestamp'] = str(self.now + 5)
            self.request.headers['X-Webhook-Nonce'] = 'offline_retry_nonce_1'
            self.sign()
            self.assertTrue(self.check())

    def test_missing_headers_are_rejected(self):
        for field in tuple(self.request.headers):
            with self.subTest(field=field):
                self.setUp()
                del self.request.headers[field]
                with self.assertRaises(ValueError):
                    self.check()

    def test_replay_store_outage_fails_closed(self):
        with patch.object(self.store, 'set', side_effect=ConnectionError('offline store')):
            with patch('time.time', return_value=self.now):
                with self.assertRaises(ConnectionError):
                    self.check()


if __name__ == '__main__':
    unittest.main()
