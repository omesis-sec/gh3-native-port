"""Trace zero-length archive entries before the game resolves their data."""
from pathlib import Path
p=Path(__file__).resolve().parent.parent/'local/hybrid/func_00230A70_0x230a70.cpp'
s=p.read_text(encoding='utf-8')
marker='    // 0x230a70: 0x27bdff90'
code='''    // GH3_ARCHIVE_ENTRY_TRACE
    if (getRegU32(ctx,5)==0x01fffe20u) std::fprintf(stderr,"[GH3 marker-before] value=%08x\\n",READ32(0x01ffffa0u));
    if (READ32(getRegU32(ctx,5)+8)==0) {
        const uint32_t p=getRegU32(ctx,5);
        std::fprintf(stderr,"[GH3 entry] addr=%08x a2=%08x ra=%08x words=%08x %08x %08x %08x %08x %08x %08x %08x\\n",p,getRegU32(ctx,6),getRegU32(ctx,31),READ32(p),READ32(p+4),READ32(p+8),READ32(p+12),READ32(p+16),READ32(p+20),READ32(p+24),READ32(p+28));
    }
'''
if 'GH3_ARCHIVE_ENTRY_TRACE' not in s:
 if s.count(marker)!=1: raise ValueError('unexpected translation')
 p.write_text('#include <cstdio>\n'+s.replace(marker,code+marker),encoding='utf-8')
