from pathlib import Path
root=Path(__file__).resolve().parent.parent
for name,addr in [('func_0022BCE0_0x22bce0','22bce0'),('func_0022DBB0_0x22dbb0','22dbb0'),('func_0022A9C8_0x22a9c8','22a9c8')]:
 p=root/'local/hybrid'/f'{name}.cpp'
 s=p.read_text(encoding='utf-8')
 marker=f'label_{addr}:'
 code='''\n    // GH3_RESOURCE_INPUT_TRACE
    std::fprintf(stderr, "[GH3 input] NAME a0=%08x a1=%08x a2=%08x a3=%08x ra=%08x sp=%08x t0=%08x t1=%08x t2=%08x t3=%08x\\n", getRegU32(ctx,4),getRegU32(ctx,5),getRegU32(ctx,6),getRegU32(ctx,7),getRegU32(ctx,31),getRegU32(ctx,29),getRegU32(ctx,8),getRegU32(ctx,9),getRegU32(ctx,10),getRegU32(ctx,11));
'''.replace('NAME',name)
 if 'GH3_RESOURCE_INPUT_TRACE' not in s:
  if s.count(marker)!=1: raise ValueError(name)
  p.write_text('#include <cstdio>\n'+s.replace(marker,marker+code),encoding='utf-8')
