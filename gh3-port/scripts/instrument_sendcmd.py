"""Add temporary host-side tracing to the generated sceSifSendCmd wrapper."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
path = ROOT / 'local/hybrid/sub_002F0AB0_0x2f0ab0.cpp'
s = path.read_text(encoding='utf-8')
marker = '    ctx->pc = getRegU32(ctx, 31);'
trace = '''    // GH3_DIAGNOSTIC_SENDCMD: host-only logging, no guest state changes.
    std::fprintf(stderr, "[GH3 sendcmd] ra=%08x cid=%08x packet=%08x bytes=%u src=%08x sp=%08x\\n",
                 getRegU32(ctx, 31), getRegU32(ctx, 4), getRegU32(ctx, 5),
                 getRegU32(ctx, 6), getRegU32(ctx, 7), getRegU32(ctx, 29));
'''
if 'GH3_DIAGNOSTIC_SENDCMD' in s:
    print('Trace already present')
elif s.count(marker) != 1:
    raise SystemExit('Unexpected generated wrapper; no changes made')
else:
    s = '#include <cstdio>\n' + s.replace(marker, trace + marker)
    path.write_text(s, encoding='utf-8')
    print(f'Instrumented {path}')
