"""Trace invalid symbol-table entries without changing guest state."""
from pathlib import Path
p=Path(__file__).resolve().parent.parent/'local/hybrid/func_00275A90_0x275a90.cpp'
s=p.read_text(encoding='utf-8')
marker='    // 0x275b28: 0xc0a1ce8  jal         func_2873A0'
trace='''    // GH3_SYMBOL_TRACE
    if ((getRegU32(ctx, 4) & 3u) != 0u) {
        const uint32_t old = getRegU32(ctx, 4), fresh = getRegU32(ctx, 17);
        std::fprintf(stderr, "[GH3 symbol] old=%08x fresh=%08x fresh_flags=%08x fresh_key=%08x fresh_val=%08x fresh_next=%08x gp_table=%08x\\n",
                     old, fresh, READ32(fresh), READ32(fresh+4), READ32(fresh+8), READ32(fresh+16), READ32(0x3710a4u));
    }
'''
if 'GH3_SYMBOL_TRACE' not in s:
 if s.count(marker)!=1: raise ValueError('Unexpected function')
 p.write_text(s.replace(marker,trace+marker),encoding='utf-8')
