"""Extract named files from this edition's DATAP.HED/DATAP.WAD into local/disc."""
import argparse
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parent.parent
DISC = ROOT / 'local/disc'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths', nargs='+', help='Archive paths to extract')
    args = parser.parse_args()
    requested = {path.replace('/', '\\').lstrip('\\').lower() for path in args.paths}
    data = (DISC / 'DATAP.HED').read_bytes()
    wad = DISC / 'DATAP.WAD'
    wad_size = wad.stat().st_size
    found = set()
    offset = 0
    with wad.open('rb') as archive:
        while offset + 8 <= len(data):
            sector, size = struct.unpack_from('<II', data, offset)
            offset += 8
            if sector == 0xffffffff:
                break
            end = data.find(b'\x00', offset)
            if end < 0:
                raise ValueError('Malformed HED filename')
            name = data[offset:end].decode('ascii')
            offset = (end + 4) & ~3
            key = name.replace('/', '\\').lstrip('\\').lower()
            if key not in requested:
                continue
            parts = key.split('\\')
            if any(part in ('', '.', '..') or ':' in part for part in parts):
                raise ValueError(f'Unsafe archive path: {name}')
            start = sector * 2048
            if start + size > wad_size:
                raise ValueError(f'Archive entry exceeds WAD: {name}')
            dest = DISC.joinpath(*parts)
            dest.parent.mkdir(parents=True, exist_ok=True)
            temp = dest.with_name(dest.name + '.partial')
            archive.seek(start)
            remaining = size
            with temp.open('wb') as out:
                while remaining:
                    chunk = archive.read(min(remaining, 1024 * 1024))
                    if not chunk:
                        raise ValueError(f'Truncated WAD entry: {name}')
                    out.write(chunk)
                    remaining -= len(chunk)
            temp.replace(dest)
            found.add(key)
            print(f'{name}: {size} bytes')
    missing = requested - found
    if missing:
        raise SystemExit(f'Paths not found: {sorted(missing)}')


if __name__ == '__main__':
    main()

\n