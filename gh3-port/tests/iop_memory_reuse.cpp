#include "emulator/core/iop_memory.h"

#include <cstdint>
#include <iostream>

using ps2x::iop::detail::IopMemory;

int main()
{
    IopMemory memory;
    const auto originalFree = memory.maxFreeMemory();
    const auto first = memory.allocate(112, 16);
    const auto second = memory.allocate(256, 16);
    if (!first || !second || !memory.freeAllocation(first)) return 1;
    if (memory.allocate(112, 16) != first) return 2;

    for (int i = 0; i < 50000; ++i)
    {
        const auto address = memory.allocate(112, 16);
        if (!address || !memory.freeAllocation(address)) return 3;
    }

    if (!memory.freeAllocation(first) || !memory.freeAllocation(second)) return 4;
    if (memory.maxFreeMemory() != originalFree) return 5;
    std::cout << "IOP memory reuse and free-space accounting passed\n";
    return 0;
}
