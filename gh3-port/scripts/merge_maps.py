"""Combine the upstream game map with baseline-detected startup and SDK entries."""
import csv
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
LOCAL = ROOT / 'local'
GAME_START, GAME_END = 0x10C000, 0x2EC0AC


def main():
    rows = []
    for line in (ROOT / 'reference/gh3-decomp/config/functions.txt').read_text(encoding='utf-8').splitlines():
        parts = line.split()
        if len(parts) == 4 and parts[1].startswith('0x'):
            rows.append((parts[0], int(parts[1], 16), int(parts[2], 16)))
    approximated = 0
    for file in (LOCAL / 'baseline').glob('*.cpp'):
        if file.name.startswith('entry_'):
            continue
        with file.open(encoding='utf-8') as source:
            head = source.read(1800)
        function = re.search(r'void (\w+)_0x([0-9a-fA-F]+)\(', head)
        if not function:
            continue
        start = int(function.group(2), 16)
        if GAME_START <= start < GAME_END:
            continue
        bounds = re.search(r'// Address: (0x[0-9a-fA-F]+) - (0x[0-9a-fA-F]+)', head)
        if bounds:
            if int(bounds.group(1), 16) != start:
                raise ValueError(f'Mismatched range in {file}')
            end = int(bounds.group(2), 16)
        else:
            # Stub implementations have no range comment. A single instruction
            # is enough to identify the address for the configured handler;
            # this is not a claim about the original function's true size.
            end = start + 4
            approximated += 1
        if end <= start or (start < GAME_START and end > GAME_START):
            raise ValueError(f'Unexpected range in {file}')
        # The heuristic split 0x101080 off as a new function even though it
        # is the delay slot of JAL at 0x10107c. Preserve the slot in the first
        # range and start the following range at the return address instead.
        if start == 0x00100000 and end == 0x00101080:
            end = 0x00101084
        elif start == 0x00101080:
            start = 0x00101084
        rows.append((function.group(1), start, end - start))
    rows.sort(key=lambda row: row[1])
    if any(a + size > b for (_, a, size), (_, b, _) in zip(rows, rows[1:])):
        raise ValueError('Overlapping ranges; refusing to generate map')
    out = LOCAL / 'hybrid-functions.csv'
    with out.open('w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(('Name', 'Start', 'End', 'Size'))
        for name, start, size in rows:
            writer.writerow((name, f'0x{start:08X}', f'0x{start+size:08X}', size))
    config = (LOCAL / 'baseline.toml').read_text(encoding='utf-8')
    config = config.replace('ghidra_output = ""', 'ghidra_output = "local/hybrid-functions.csv"')
    config = config.replace('output = "local/baseline/"', 'output = "local/hybrid/"')
    hints = LOCAL / "entry-hints.txt"
    addresses = {0x0011EA08, 0x002D8378, 0x002A67C8}  # observed missing targets
    if hints.exists():
        addresses.update(int(line, 16) for line in hints.read_text(encoding="utf-8").splitlines() if line.strip())
    entries = "".join(f'\n  "entry_{addr:08X}@0x{addr:08X}",' for addr in sorted(addresses))
    config = config.replace("entry_points = [", "entry_points = [" + entries, 1)
    (LOCAL / 'hybrid.toml').write_text(config, encoding='utf-8')
    print(f'{len(rows)} non-overlapping entries, including {approximated} approximate stub ranges')


if __name__ == '__main__':
    main()
