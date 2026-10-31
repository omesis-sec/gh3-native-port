#pragma once

#include <cstdint>
#include <string>
#include <string_view>
#include <vector>
#include <unordered_map>

namespace ps2x::iop { class IopHost; }

namespace ps2x::iop::detail
{
    struct IopCpuState;
    class IopGuestExecutor;
    class IopMemory;

    class IopIoman
    {
    public:
        IopIoman(IopMemory &memory, IopHost &host) noexcept;
        ~IopIoman();

        void reset();
        [[nodiscard]] bool dispatchImport(uint16_t ordinal, IopCpuState &cpu, IopGuestExecutor &executor);

    private:
        struct Device
        {
            uint32_t address = 0u;
            uint32_t gp = 0u;
            std::string name;
        };

        struct OpenFile { uint64_t handle; uint64_t offset; uint64_t size; uint64_t base = 0u; bool trace = false; };
        struct ArchiveEntry { uint64_t offset; uint32_t size; };
        bool openGameArchive(std::string_view guestPath, OpenFile &file);
        bool loadGameArchiveIndex();
        IopMemory &m_memory;
        IopHost &m_host;
        std::unordered_map<uint32_t, OpenFile> m_files;
        std::unordered_map<std::string, ArchiveEntry> m_archiveEntries;
        bool m_archiveIndexLoaded = false;
        uint32_t m_nextFd = 3u;
        uint32_t m_traceCount = 0u;
        std::vector<Device> m_devices;
    };
}
