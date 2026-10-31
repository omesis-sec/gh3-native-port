"""Preserve an early open callback when the IOP finishes before async setup."""
from pathlib import Path
p=Path(__file__).resolve().parent.parent/'local/hybrid/func_00120180_0x120180.cpp'
s=p.read_text(encoding='utf8')
old='''    // 0x120360: 0xae030048  sw          $v1, 0x48($s0)
    ctx->pc = 0x120360u;
    WRITE32(ADD32(GPR_U32(ctx, 16), 72), GPR_U32(ctx, 3));'''
new='''    // GH3_EARLY_OPEN_CALLBACK: the callback can finish before this sentinel is installed.
    ctx->pc = 0x120360u;
    if (READ32(ADD32(GPR_U32(ctx, 16), 64)) != 0u)
        WRITE32(ADD32(GPR_U32(ctx, 16), 72), GPR_U32(ctx, 3));'''
if 'GH3_EARLY_OPEN_CALLBACK' not in s:
 if s.count(old)!=1:raise ValueError('Unexpected file-open function')
 p.write_text(s.replace(old,new),encoding='utf8')
