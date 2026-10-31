"""Trace completed I/O callback records during late boot."""
from pathlib import Path
p=Path(__file__).resolve().parent.parent/'local/hybrid/func_001207A0_0x1207a0.cpp'
s=p.read_text(encoding='utf8')
marker='label_1207a0:'
code='''
    // GH3_IO_CALLBACK_TRACE
    if (READ32(getRegU32(ctx,4)+12)>=340u) {
        auto p=getRegU32(ctx,4);
        std::fprintf(stderr,"[GH3 io-callback] p=%08x id=%08x status=%08x flag=%08x len=%08x tail=%08x ra=%08x\\n",p,READ32(p+12),READ32(p+16),READ32(p+20),READ32(p+24),READ32(p+108),getRegU32(ctx,31));
    }
'''
if 'GH3_IO_CALLBACK_TRACE' not in s:
 if s.count(marker)!=1:raise ValueError('unexpected function')
 p.write_text('#include <cstdio>\n'+s.replace(marker,marker+code),encoding='utf8')
