"""Install a bounded, opt-in cursor-write trace in the generated parser."""
from pathlib import Path
import re

path = Path(__file__).resolve().parent.parent / 'local/hybrid/func_0028AF38_0x28af38.cpp'
text = path.read_text(encoding='utf-8')
if 'GH3_CURSOR_WRITES' not in text:
    marker = 'void func_0028AF38_0x28af38(uint8_t* rdram, R5900Context* ctx, PS2Runtime *runtime) {'
    pattern = r'(?m)^([ \t]*)WRITE32\(ADD32\(GPR_U32\(ctx, 18\), 20\), (GPR_U32\(ctx, \d+\))\);'
    if text.count(marker) != 1 or len(re.findall(pattern, text)) != 19:
        raise ValueError('Unexpected generated parser; inspect revision before tracing')
    trace = '''
    // GH3_CURSOR_WRITES: pointer-only trace, disabled unless a guest object is selected.
    static const char *cursorFilter = std::getenv("GH3_TRACE_CURSOR_OBJECT");
    static const uint32_t cursorObject = cursorFilter ? static_cast<uint32_t>(std::strtoul(cursorFilter, nullptr, 0)) : 0;
    auto gh3CursorWrite = [&](uint32_t before, uint32_t value) {
        static thread_local uint64_t count = 0, decreases = 0;
        const uint64_t n = ++count;
        if (value < before) {
            const uint64_t d = ++decreases;
            if (d <= 16 || (d & (d - 1)) == 0)
                std::fprintf(stderr, "[GH3 cursor-decrease] count=%llu pc=%08x object=%08x before=%08x cursor=%08x\\n",
                             static_cast<unsigned long long>(d), ctx->pc, cursorObject, before, value);
        }
        if (n <= 16 || (n & (n - 1)) == 0)
            std::fprintf(stderr, "[GH3 cursor-write] count=%llu pc=%08x object=%08x cursor=%08x\\n",
                         static_cast<unsigned long long>(n), ctx->pc, cursorObject, value);
    };
'''
    text = '#include <cstdio>\n#include <cstdlib>\n' + text.replace(marker, marker + trace)
    def instrument(match):
        indent, value = match.group(1), match.group(2)
        write = f'WRITE32(ADD32(GPR_U32(ctx, 18), 20), {value});'
        return (f'{indent}if (cursorObject && getRegU32(ctx, 18) == cursorObject) {{\n'
                f'{indent}    const uint32_t before = READ32(ADD32(GPR_U32(ctx, 18), 20));\n'
                f'{indent}    {write}\n'
                f'{indent}    gh3CursorWrite(before, {value});\n'
                f'{indent}}} else {{\n{indent}    {write}\n{indent}}}')
    text = re.sub(pattern, instrument, text)
    path.write_text(text, encoding='utf-8')
    print('Installed bounded parser cursor tracing')
else:
    print('Parser cursor tracing already installed')
