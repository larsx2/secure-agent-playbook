#!/usr/bin/env python3
"""One dependency graph for direct Skills CLI installs and per-skill release ZIPs."""
import argparse
import os
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCE = re.compile(r'(?<![\w-])((?:plays|templates|references)/[\w.-]+\.md)')
DATASET = re.compile(r'(?<![\w/-])data/([a-z-]+)/')
DATAFILE = re.compile(r'(?<![\w/-])(data/[a-z-]+/[\w.-]+\.md)')
MANAGED = ('plays', 'templates', 'data', 'references')
# claude.ai Organization settings > Skills rejected larger ZIPs with "Zip contains
# too many files (maximum 200)" (issue #23). Observed, not a documented limit.
MAX_FILES = 200
NO_SYMLINKS = ('Git checked out the generated resource symlinks as plain-text path stubs '
               '(core.symlinks=false, the default on Windows). Enable symlinks (Windows: turn on '
               'Developer Mode, then git config core.symlinks true) and re-checkout, or install '
               'from the per-skill release ZIPs.')


def skills():
    return sorted(path.parent for path in ROOT.glob('plugins/*/skills/*/SKILL.md'))


def dependency_files(skill):
    """Return installed paths -> canonical sources, following references to a fixed point."""
    plugin = skill.parent.parent
    files = {}
    pending = [(Path('SKILL.md'), skill / 'SKILL.md')]
    datasets = set()

    def add(relative):
        source = plugin / relative
        if relative.parts[0] == 'references':
            source = plugin / 'skills' / relative.stem / 'SKILL.md'
        if not source.is_file():
            raise ValueError(f'Missing dependency for {skill.name}: {relative}')
        pending.append((relative, source))

    def unbundled(dataset, relative):
        # Repo-root research datasets (e.g. data/opencre) are not shipped in a
        # plugin; plays/templates may cite them, but SKILL.md citing one fails.
        return relative != Path('SKILL.md') and not (plugin / 'data' / dataset).is_dir()

    while pending:
        relative, source = pending.pop()
        if relative in files:
            continue
        files[relative] = source
        text = source.read_text(encoding='utf-8')
        # URLs are explicit external lookups, not local dependencies.
        local = re.sub(r'https?://[^\s)<>`]+', '', text)
        for resource in RESOURCE.findall(local):
            add(Path(resource))
        for resource in DATAFILE.findall(local):
            if not unbundled(Path(resource).parts[1], relative):
                add(Path(resource))
        # Older procedures name sibling plays/templates without a directory prefix.
        for name in re.findall(r'(?<![\w/-])([\w-]+\.md)', local):
            for collection in ('plays', 'templates'):
                if (plugin / collection / name).is_file():
                    add(Path(collection) / name)
        for dataset in DATASET.findall(local):
            if unbundled(dataset, relative):
                continue
            if f'data/{dataset}/README.md' in local:
                add(Path('data') / dataset / 'README.md')
            if dataset in datasets:
                continue
            datasets.add(dataset)
            directory = plugin / 'data' / dataset
            if not directory.is_dir():
                raise ValueError(f'Missing dependency for {skill.name}: data/{dataset}')
            # MASTG is selected via MASVS controls and transitive test references,
            # not the entire upstream test corpus (see MAX_FILES).
            paths = sorted(path for path in directory.glob('*.md') if path.name != 'README.md')
            if not paths:
                raise ValueError(f'Empty dataset: {directory}')
            if dataset == 'mastg':
                continue
            for path in paths:
                add(path.relative_to(plugin))
        if relative.parts[:2] in (('data', 'masvs'), ('data', 'mastg')):
            for test_id in set(re.findall(r'MASTG-TEST-\d+', text)):
                test = Path('data/mastg') / f'{test_id}.md'
                if (plugin / test).is_file():
                    add(test)
                # Unextracted upstream cross-references are explicitly external;
                # the mobile play describes how to resolve them.
    return dict(sorted(files.items()))


def check_size(skill, files):
    if len(files) > MAX_FILES:
        raise ValueError(
            f'{skill.name}: {len(files)} files exceeds the {MAX_FILES}-file limit of the claude.ai '
            f'skills upload (README, "Organization skills"). Shrink this skill\'s dependency closure '
            f'(e.g. narrow the data files or MASTG tests it references, or turn upstream-only '
            f'material into online lookups) instead of dropping files it references.')


def symlink_stub():
    """Return a generated link that Git checked out as a text stub, if any."""
    for skill in skills():
        for name in MANAGED:
            for path in sorted((skill / name).rglob('*.md')):
                if path.is_symlink() or path.stat().st_size > 512:
                    continue
                text = path.read_text(encoding='utf-8', errors='replace')
                if text.startswith('../') and '\n' not in text.strip():
                    return path
    return None


def check_links(skill, files):
    """Fail on stale/missing resource links without modifying the checkout."""
    expected = set(files) - {Path('SKILL.md')}
    actual = set()
    for name in MANAGED:
        directory = skill / name
        if directory.is_symlink():
            raise ValueError(f'Legacy resource directory symlink: {directory}')
        if directory.exists():
            actual.update(path.relative_to(skill) for path in directory.rglob('*') if path.is_file() or path.is_symlink())
    if actual != expected:
        raise ValueError(f'{skill.name}: resource layout differs; run python3 scripts/package_skills.py --sync')
    for relative in expected:
        link = skill / relative
        if not link.is_symlink() or link.resolve() != files[relative].resolve():
            if link.is_file() and symlink_stub():
                raise ValueError(NO_SYMLINKS)
            raise ValueError(f'Incorrect dependency link: {link}')


def sync_links(skill, files):
    """Maintain only generated resource symlinks; never overwrite authored files."""
    expected = set(files) - {Path('SKILL.md')}
    for name in MANAGED:
        directory = skill / name
        if directory.is_symlink():
            directory.unlink()  # obsolete references -> repo-root data layout
        elif directory.exists():
            for path in sorted(directory.rglob('*'), reverse=True):
                if path.is_symlink():
                    if path.relative_to(skill) not in expected:
                        path.unlink()
                elif path.is_file():
                    raise ValueError(f'Refusing to overwrite authored resource: {path}')
                elif path.is_dir() and not any(path.iterdir()):
                    path.rmdir()
    for relative in sorted(expected):
        link = skill / relative
        target = os.path.relpath(files[relative], link.parent)
        link.parent.mkdir(parents=True, exist_ok=True)
        if link.is_symlink():
            if os.readlink(link) == target:
                continue
            link.unlink()
        if link.exists():
            raise ValueError(f'Refusing to overwrite: {link}')
        link.symlink_to(target)
    # Directly opened plugin plays use the same bundled peer-skill references.
    for relative, source in files.items():
        if relative.parts[0] != 'references':
            continue
        link = skill.parent.parent / relative
        target = os.path.relpath(source, link.parent)
        link.parent.mkdir(parents=True, exist_ok=True)
        if link.is_symlink() and os.readlink(link) == target:
            continue
        if link.exists() or link.is_symlink():
            raise ValueError(f'Refusing to overwrite: {link}')
        link.symlink_to(target)


def package_skill(skill, output):
    files = dependency_files(skill)
    check_size(skill, files)
    check_links(skill, files)
    output.mkdir(parents=True, exist_ok=True)
    archive = output / f'{skill.name}.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as bundle:
        for relative, source in files.items():
            bundle.write(source, f'{skill.name}/{relative}')
    return archive


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sync', action='store_true', help='refresh committed resource symlinks after editing references')
    parser.add_argument('--check', action='store_true', help='check resource links without producing archives')
    parser.add_argument('--output', type=Path, default=ROOT / 'dist/skills')
    args = parser.parse_args()
    try:
        run(args)
    except ValueError as error:
        raise SystemExit(f'error: {error}')


def run(args):
    if symlink_stub():
        raise ValueError(NO_SYMLINKS)
    for skill in skills():
        files = dependency_files(skill)
        check_size(skill, files)
        if args.sync:
            sync_links(skill, files)
        check_links(skill, files)
        if not args.check and not args.sync:
            package_skill(skill, args.output)
        print(f'{skill.name}: {len(files)} files')


if __name__ == '__main__':
    main()
