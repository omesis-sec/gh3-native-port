"""Extract an initial or complete PS2 ISO9660 disc tree to local/disc."""
import argparse
from pathlib import Path
import shutil

SECTOR = 2048
ROOT = Path(__file__).resolve().parent.parent


def records(image, extent, length):
    image.seek(extent * SECTOR)
    data = image.read(length)
    pos = 0
    while pos < len(data):
        count = data[pos]
        if count == 0:
            pos = (pos // SECTOR + 1) * SECTOR
            continue
        item = data[pos:pos + count]
        if len(item) != count or count < 34:
            raise ValueError("Invalid directory entry")
        raw = item[33:33 + item[32]]
        pos += count
        if raw in (b"\x00", b"\x01"):
            continue
        name = raw.decode("ascii").split(";", 1)[0]
        if name in ("", ".", "..") or any(c in name for c in '/\\:'):
            raise ValueError(f"Unsafe ISO name: {name!r}")
        if item[25] & 0x80 or item[26] or item[27]:
            raise ValueError(f"Unsupported multi-extent or interleaved file: {name}")
        yield (name, int.from_bytes(item[2:6], 'little'),
               int.from_bytes(item[10:14], 'little'), bool(item[25] & 2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("iso", type=Path)
    parser.add_argument("--full", action="store_true", help="also extract all movies, music and streams")
    parser.add_argument("--sounds", action="store_true", help="also extract SOUNDS for the IOP audio driver")
    args = parser.parse_args()
    out = ROOT / 'local' / 'disc'
    out.mkdir(parents=True, exist_ok=True)
    with args.iso.open('rb') as image:
        image.seek(16 * SECTOR)
        pvd = image.read(SECTOR)
        if pvd[1:6] != b'CD001':
            raise ValueError('Not an ISO9660 image')
        root = pvd[156:]
        stack = [(out, int.from_bytes(root[2:6], 'little'), int.from_bytes(root[10:14], 'little'))]
        total = 0
        while stack:
            folder, extent, size = stack.pop()
            for name, file_extent, file_size, directory in list(records(image, extent, size)):
                if directory and folder == out and not args.full and name.upper() not in ({'IOP', 'SOUNDS'} if args.sounds else {'IOP'}):
                    continue
                target = folder / name
                if directory:
                    target.mkdir(exist_ok=True)
                    stack.append((target, file_extent, file_size))
                    continue
                temp = target.with_name(target.name + '.partial')
                image.seek(file_extent * SECTOR)
                remaining = file_size
                with temp.open('wb') as dst:
                    while remaining:
                        chunk = image.read(min(remaining, 8 * 1024 * 1024))
                        if not chunk:
                            raise ValueError(f'Truncated file: {name}')
                        dst.write(chunk)
                        remaining -= len(chunk)
                temp.replace(target)
                total += file_size
                print(f'{target.relative_to(out)}: {file_size} bytes', flush=True)
        print(f'Extracted {total} bytes into {out}')
    modules = out / 'IOP'
    if modules.is_dir():
        shutil.copytree(modules, out / 'IOPModules', dirs_exist_ok=True)
        print('Prepared IOPModules for host0 paths used by the game')


if __name__ == '__main__':
    main()
