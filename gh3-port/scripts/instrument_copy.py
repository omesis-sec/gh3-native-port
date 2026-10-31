"""Trace the aligned copy for the small debug package."""
from pathlib import Path
p=Path(__file__).resolve().parent.parent/'local/hybrid/sub_0030A2F4_0x30a2f4.cpp'
s=p.read_text(encoding='utf-8')
for marker in ('label_30a318:', 'label_30a398:'):
 token='GH3_COPY_'+marker[6:]
 code='''
    // TOKEN
    if (getRegU32(ctx,8)==0x01fffe20u) std::fprintf(stderr,"[GH3 copy-step] TAG src=%08x dst=%08x remaining=%08x marker=%08x pc=%08x ra=%08x\\n",getRegU32(ctx,5),getRegU32(ctx,7),getRegU32(ctx,6),READ32(0x01ffffa0u),ctx->pc,getRegU32(ctx,31));
'''.replace('TOKEN',token).replace('TAG',marker)
 if token not in s:
  if s.count(marker)!=1: raise ValueError(marker)
  s=s.replace(marker,marker+code)
if not s.startswith('#include <cstdio>'):s='#include <cstdio>\n'+s
p.write_text(s,encoding='utf-8')
