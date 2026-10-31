"""Track pack entry traversal, including the calculated next header."""
from pathlib import Path
p=Path(__file__).resolve().parent.parent/'local/hybrid/func_00230518_0x230518.cpp'
s=p.read_text(encoding='utf-8')
marker='label_23052c:'
code='''
    // GH3_PACK_WALK_TRACE
    if (getRegU32(ctx,16) < 0x02000000u) std::fprintf(stderr,"[GH3 walk] p=%08x type=%08x offset=%08x size=%08x flags=%08x step=%08x ra=%08x\\n",getRegU32(ctx,16),READ32(getRegU32(ctx,16)),READ32(getRegU32(ctx,16)+4),READ32(getRegU32(ctx,16)+8),READ32(getRegU32(ctx,16)+28),getRegU32(ctx,2),READ32(getRegU32(ctx,29)+8));
'''
if 'GH3_PACK_WALK_TRACE' not in s:
 if s.count(marker)!=1: raise ValueError('unexpected translation')
 p.write_text('#include <cstdio>\n'+s.replace(marker,marker+code),encoding='utf-8')
