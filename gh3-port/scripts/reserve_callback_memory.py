"""Keep the game's hardcoded heap below runtime callback stacks (1 MiB)."""
from pathlib import Path
p=Path(__file__).resolve().parent.parent/'local/hybrid/func_00118BD8_0x118bd8.cpp'
s=p.read_text(encoding='utf8')
old='''    // 0x118d58: 0x3c100200  lui         $s0, 0x200
    ctx->pc = 0x118d58u;
    SET_GPR_S32(ctx, 16, (int32_t)((uint32_t)512 << 16));'''
new='''    // GH3_CALLBACK_STACK_RESERVATION: reserve 0x01f00000..0x01ffffff.
    // The original LUI sets the upper limit to 0x02000000.
    ctx->pc = 0x118d58u;
    SET_GPR_S32(ctx, 16, (int32_t)((uint32_t)496 << 16));'''
if 'GH3_CALLBACK_STACK_RESERVATION' not in s:
 if s.count(old)!=1: raise ValueError('Unexpected game heap initialization')
 p.write_text(s.replace(old,new),encoding='utf8')
