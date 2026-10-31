"""Sample the outstanding I/O counter during waits."""
from pathlib import Path
p=Path(__file__).resolve().parent.parent/'local/hybrid/func_0011DAA0_0x11daa0.cpp'
s=p.read_text(encoding='utf8')
marker='    // 0x11daa0: 0x8c820040'
code='''    // GH3_WAIT_TRACE
    static unsigned sample=0;
    if ((++sample % 200000u)==0u) {
        const auto p=getRegU32(ctx,4);
        std::fprintf(stderr,"[GH3 wait] self=%08x count=%08x flags=%08x size=%08x ra=%08x\\n",p,READ32(p+0x40),READ32(p),READ32(p+0x30),getRegU32(ctx,31));
    }
'''
if 'GH3_WAIT_TRACE' not in s:
 if s.count(marker)!=1:raise ValueError('unexpected function')
 p.write_text('#include <cstdio>\n'+s.replace(marker,code+marker),encoding='utf8')
