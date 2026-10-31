from pathlib import Path
root=Path(__file__).resolve().parent.parent
for name in ('func_0011FB70_0x11fb70','func_0011FBE0_0x11fbe0','func_0011FC50_0x11fc50','func_0011FCC0_0x11fcc0','func_0011FF58_0x11ff58','func_0011F548_0x11f548','func_0011FDC0_0x11fdc0','func_0011FB38_0x11fb38'):
 p=root/'local/hybrid'/f'{name}.cpp';s=p.read_text(encoding='utf8')
 marker=f'void {name}(uint8_t* rdram, R5900Context* ctx, PS2Runtime *runtime) {{'
 code='''
    // GH3_FD_TRACE
    if (getRegU32(ctx,4)==0x00593f00u || READ32(getRegU32(ctx,4)+0x48)==0xffffffffu)
        std::fprintf(stderr,"[GH3 fd] NAME pc=%08x obj=%08x fd=%08x a1=%08x ra=%08x\\n",ctx->pc,getRegU32(ctx,4),READ32(getRegU32(ctx,4)+0x48),getRegU32(ctx,5),getRegU32(ctx,31));
'''.replace('NAME',name)
 if 'GH3_FD_TRACE' not in s:
  if s.count(marker)!=1:raise ValueError(name)
  p.write_text('#include <cstdio>\n'+s.replace(marker,marker+code),encoding='utf8')
