"""Trace QB fixup visits near the observed failing serialized record."""
from pathlib import Path
root = Path(__file__).resolve().parent.parent / 'local/hybrid'
for name in ('func_00292808_0x292808', 'func_00292928_0x292928'):
    path = root / (name + '.cpp')
    text = path.read_text(encoding='utf-8')
    if 'GH3_QB_VISIT_TRACE' in text:
        continue
    marker = f'void {name}(uint8_t* rdram, R5900Context* ctx, PS2Runtime *runtime) {{'
    if text.count(marker) != 1:
        raise RuntimeError(f'Unexpected generated function: {path}')
    trace = '''
    // GH3_QB_VISIT_TRACE: inspect the observed record, preserving guest state.
    if (getRegU32(ctx, 4) >= 0x00a54c40u && getRegU32(ctx, 4) <= 0x00a54cb0u) {
        std::fprintf(stderr, "[GH3 visit] %s pc=%08x a0=%08x a1=%08x ra=%08x sp=%08x\\n",
                     "{NAME}", ctx->pc, getRegU32(ctx, 4), getRegU32(ctx, 5),
                     getRegU32(ctx, 31), getRegU32(ctx, 29));
    }
'''.replace('{NAME}', name)
    path.write_text('#include <cstdio>\n' + text.replace(marker, marker + trace), encoding='utf-8')
    print('Instrumented', name)
