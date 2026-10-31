"""Regenerate the hybrid map and update only changed generated sources."""
from pathlib import Path
import filecmp
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
LOCAL = ROOT / 'local'


def checked(command):
    subprocess.run([str(part) for part in command], cwd=ROOT, check=True)


def main():
    checked([sys.executable, ROOT / 'scripts/discover_entries.py'])
    checked([sys.executable, ROOT / 'scripts/merge_maps.py'])
    source = (LOCAL / 'hybrid.toml').read_text(encoding='utf-8')
    expected = 'output = "local/hybrid/"'
    if source.count(expected) != 1:
        raise RuntimeError('Unexpected hybrid output configuration')
    candidate_config = LOCAL / 'hybrid-candidates.toml'
    candidate_config.write_text(source.replace(expected, 'output = "local/hybrid-candidates/"'), encoding='utf-8')
    binary = ROOT.parent / 'out/codex-build/ps2xRecomp/Release/ps2_recomp.exe'
    with (LOCAL / 'hybrid-candidates.log').open('w', encoding='utf-8') as log:
        subprocess.run([str(binary), str(candidate_config)], cwd=ROOT, stdout=log,
                       stderr=subprocess.STDOUT, check=True)
    current, candidate = LOCAL / 'hybrid', LOCAL / 'hybrid-candidates'
    # A fresh checkout has no generated tree yet.
    current.mkdir(parents=True, exist_ok=True)
    old = {p.name for p in current.iterdir() if p.is_file()}
    new = {p.name for p in candidate.iterdir() if p.is_file()}
    # This one generated file is superseded when the startup delay-slot split
    # is repaired. Refuse to remove any other file automatically.
    removed = old - new
    allowed = {'sub_00101080_0x101080.cpp'}
    if removed - allowed:
        raise RuntimeError(f'Unexpected removed generated files: {sorted(removed-allowed)[:10]}')
    for name in removed:
        (current / name).unlink()
    changed = [name for name in sorted(old & new)
               if not filecmp.cmp(current / name, candidate / name, shallow=False)]
    for name in changed + sorted(new - old):
        shutil.copyfile(candidate / name, current / name)
    print(f'Updated {len(changed)} and added {len(new-old)} generated files')
    checked([sys.executable, ROOT / 'scripts/instrument_sendcmd.py'])
    checked([sys.executable, ROOT / 'scripts/instrument_startup.py'])
    checked([sys.executable, ROOT / 'scripts/instrument_fixup.py'])
    checked([sys.executable, ROOT / 'scripts/instrument_qb_visits.py'])
    checked([sys.executable, ROOT / 'scripts/instrument_symbol.py'])
    checked([sys.executable, ROOT / 'scripts/instrument_cursor_writes.py'])
    checked([sys.executable, ROOT / 'scripts/instrument_cursor.py'])
    checked([sys.executable, ROOT / 'scripts/instrument_resource_input.py'])
    checked([sys.executable, ROOT / 'scripts/reserve_callback_memory.py'])
    checked([sys.executable, ROOT / 'scripts/fix_early_open_callback.py'])


if __name__ == '__main__':
    main()
