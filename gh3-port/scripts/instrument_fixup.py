"""Log mismatched fixup positions in the generated QB parser."""
from pathlib import Path
p = Path(__file__).resolve().parent.parent / 'local/hybrid/func_00292928_0x292928.cpp'
s = p.read_text(encoding='utf-8')
marker = '    // 0x29297c: 0x1093000d  beq         $a0, $s3, . + 4 + (0xD << 2)'
insert = '''    // GH3_FIXUP_TRACE: inspect mismatches without modifying guest state.
    if (getRegU32(ctx, 4) != 0u && getRegU32(ctx, 4) != getRegU32(ctx, 19)) {
        std::fprintf(stderr, "[GH3 fixup] node=%08x next=%08x expected=%08x base=%08x\\n",
                     getRegU32(ctx, 18), getRegU32(ctx, 4), getRegU32(ctx, 19), getRegU32(ctx, 16));
    }
'''
if 'GH3_FIXUP_TRACE' in s:
    print('Trace already present')
elif s.count(marker) != 1:
    raise SystemExit('Unexpected generated function; no changes made')
else:
    s = s.replace(marker, insert + marker)
    delay = '        SET_GPR_U64(ctx, 19, (uint64_t)GPR_U64(ctx, 2) + (uint64_t)GPR_U64(ctx, 0));'
    detail = '''
        if (getRegU32(ctx, 18) >= 0x00a54c40u && getRegU32(ctx, 18) <= 0x00a54cb0u)
            std::fprintf(stderr, "[GH3 chain] node=%08x next=%08x expected=%08x base=%08x\\n",
                         getRegU32(ctx, 18), getRegU32(ctx, 4), getRegU32(ctx, 19), getRegU32(ctx, 16));
'''
    if s.count(delay) != 1:
        raise SystemExit('Unexpected QB loop; no changes made')
    p.write_text('#include <cstdio>\n' + s.replace(delay, delay + detail), encoding='utf-8')
    print('Instrumented QB fixup comparison')
