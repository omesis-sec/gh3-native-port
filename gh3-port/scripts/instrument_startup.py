"""Add bounded host-side tracing to selected generated startup functions."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
NAMES = ('func_00120BC0_0x120bc0', 'func_00120C08_0x120c08',
         'func_00120C80_0x120c80', 'func_002EA460_0x2ea460',
         'sub_002EEA00_0x2eea00', 'func_0011A988_0x11a988',
         'func_0011AA28_0x11aa28', 'func_0027AC90_0x27ac90',
         'func_002791E0_0x2791e0', 'func_00113228_0x113228', 'Heap_Free_0x119400',
         'func_002873A0_0x2873a0', 'func_00275A90_0x275a90')
for name in NAMES:
    path = ROOT / 'local/hybrid' / (name + '.cpp')
    text = path.read_text(encoding='utf-8')
    if 'GH3_STARTUP_TRACE' in text:
        continue
    marker = f'void {name}(uint8_t* rdram, R5900Context* ctx, PS2Runtime *runtime) {{'
    if text.count(marker) != 1:
        raise RuntimeError(f'Unexpected generated function: {path}')
    trace = '''
    // GH3_STARTUP_TRACE: host-only, bounded log.
    static int trace_count = 0;
    if (trace_count++ < 80) {
        std::fprintf(stderr, "[GH3 trace] %s pc=%08x ra=%08x a0=%08x v0=%08x\\n",
                     "{NAME}", ctx->pc, getRegU32(ctx, 31), getRegU32(ctx, 4), getRegU32(ctx, 2));
    }
'''.replace('{NAME}', name)
    if name == 'func_002791E0_0x2791e0':
        trace += '''
    static unsigned node_count = 0;
    if (node_count++ < 80 && ctx->pc == 0x2791e0u && getRegU32(ctx, 4) < 0x01ffffe0u) {
        const uint32_t node = getRegU32(ctx, 4);
        std::fprintf(stderr, "[GH3 node] address=%08x flags=%08x key=%08x value=%08x next=%08x\\n",
                     node, READ32(node), READ32(node+4u), READ32(node+8u), READ32(node+12u));
    }
'''
    path.write_text('#include <cstdio>\n' + text.replace(marker, marker + trace), encoding='utf-8')
    print(f'Instrumented {name}')
