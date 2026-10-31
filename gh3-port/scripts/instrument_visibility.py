"""Sample entry to the game's resource-visibility update."""
from pathlib import Path
p=Path(__file__).resolve().parent.parent/'local/hybrid/func_00236210_0x236210.cpp'
s=p.read_text(encoding='utf8')
marker='    // 0x236210:'
code='''    // GH3_VISIBILITY_TRACE
    static unsigned calls=0;
    if ((calls++ % 1000u)==0u) std::fprintf(stderr,"[GH3 visibility] calls=%u self=%08x ra=%08x\\n",calls,getRegU32(ctx,4),getRegU32(ctx,31));
'''
if 'GH3_VISIBILITY_TRACE' not in s:
 if s.count(marker)!=1:raise ValueError('unexpected function')
 p.write_text('#include <cstdio>\n'+s.replace(marker,code+marker),encoding='utf8')
