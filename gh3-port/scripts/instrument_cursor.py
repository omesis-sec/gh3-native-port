"""Trace unaligned entries in the QB loader."""
from pathlib import Path
p=Path(__file__).resolve().parent.parent/'local/hybrid/func_00292AF0_0x292af0.cpp'
s=p.read_text(encoding='utf-8')
marker='    // 0x292b48: 0xc0a4a7c  jal         func_2929F0'
trace='''    // GH3_CURSOR_TRACE
    if ((getRegU32(ctx, 17) & 3u) != 0u) {
        std::fprintf(stderr, "[GH3 cursor] cursor=%08x end=%08x base=%08x s3=%08x s4=%08x sp=%08x\\n",
                     getRegU32(ctx,17), getRegU32(ctx,18), getRegU32(ctx,22), getRegU32(ctx,19), getRegU32(ctx,20), getRegU32(ctx,29));
    }
'''
if 'GH3_CURSOR_TRACE' not in s:
 if s.count(marker)!=1: raise ValueError('Unexpected generated function')
 p.write_text('#include <cstdio>\n'+s.replace(marker,trace+marker),encoding='utf-8')
