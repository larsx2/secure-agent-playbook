#!/usr/bin/env bash
# Direct installs and <=200-file release ZIPs share one dependency graph.
set -euo pipefail
exec python3 "$(dirname "$0")/package_skills.py" "$@"
