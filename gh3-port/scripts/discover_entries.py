"""Find possible indirect entries supported by both ELF data and the baseline scan."""
import bisect
from pathlib import Path
import re
import struct

ROOT = Path(__file__).resolve().parent.parent
LOCAL = ROOT / 'local'


def main():
    elf = (LOCAL / 'SLUS_216.72.elf').read_bytes()
    if elf[:4] != b'\x7fELF' or elf[4:6] != b'\x01\x01':
        raise ValueError('Expected a 32-bit little-endian ELF')
    phoff = struct.unpack_from('<I', elf, 28)[0]
    phentsize, phnum = struct.unpack_from('<HH', elf, 42)
    data_start, data_end = 0x32A080, 0x372A40
    data = None
    for index in range(phnum):
        typ, offset, va, _, size, _, _, _ = struct.unpack_from('<8I', elf, phoff + index * phentsize)
        if typ == 1 and va <= data_start < data_end <= va + size:
            data = elf[offset + data_start - va:offset + data_end - va]
            break
    if data is None:
        raise ValueError('Expected initialized data range is absent')
    words = {value[0] for value in struct.iter_unpack('<I', data)}
    baseline = set()
    for file in (LOCAL / 'baseline').glob('sub_*_0x*.cpp'):
        match = re.search(r'_0x([0-9a-f]+)\.cpp$', file.name, re.I)
        if match:
            baseline.add(int(match.group(1), 16))
    functions = []
    for line in (ROOT / 'reference/gh3-decomp/config/functions.txt').read_text(encoding='utf-8').splitlines():
        fields = line.split()
        if len(fields) == 4 and fields[1].startswith('0x'):
            functions.append((int(fields[1], 16), int(fields[2], 16)))
    functions.sort()
    keys = [start for start, _ in functions]
    candidates = []
    for addr in sorted(words & baseline):
        index = bisect.bisect_right(keys, addr) - 1
        if index >= 0 and functions[index][0] < addr < functions[index][0] + functions[index][1]:
            candidates.append(addr)
    out = LOCAL / 'entry-hints.txt'
    out.write_text(''.join(f'0x{addr:08X}\n' for addr in candidates), encoding='utf-8')
    print(f'{len(candidates)} candidate interior entries written to {out}')


if __name__ == '__main__':
    main()
