#include "iop_ioman.h"

#include "../core/iop_cpu.h"
#include "../core/iop_memory.h"
#include "../services/iop_rpc.h"
#include "ps2x/iop/iop_host.h"

#include <algorithm>
#include <cctype>
#include <cstring>
#include <limits>
#include <vector>

namespace ps2x::iop::detail
{
    IopIoman::IopIoman(IopMemory &memory, IopHost &host) noexcept
        : m_memory(memory), m_host(host)
    {
    }

    IopIoman::~IopIoman() { reset(); }

    void IopIoman::reset()
    {
        for (const auto &[fd, file] : m_files)
            m_host.closeHostFile(file.handle);
        m_files.clear();
        m_nextFd = 3u;
        m_archiveEntries.clear();
        m_archiveIndexLoaded = false;
        m_devices.clear();
    }

    namespace
    {
        std::string archiveKey(std::string_view path)
        {
            const size_t colon = path.find(':');
            if (colon != std::string_view::npos) path.remove_prefix(colon + 1u);
            while (!path.empty() && (path.front() == '/' || path.front() == '\\')) path.remove_prefix(1u);
            std::string key;
            key.reserve(path.size());
            for (unsigned char c : path)
                key.push_back(c == '/' ? '\\' : static_cast<char>(std::tolower(c)));
            return key;
        }

        uint32_t readLittle32(const uint8_t *p)
        {
            return uint32_t(p[0]) | (uint32_t(p[1]) << 8u) | (uint32_t(p[2]) << 16u) | (uint32_t(p[3]) << 24u);
        }
    }

    bool IopIoman::loadGameArchiveIndex()
    {
        if (m_archiveIndexLoaded) return !m_archiveEntries.empty();
        m_archiveIndexLoaded = true;
        const std::string path = m_host.translateGuestPath("host0:DATAP.HED");
        const uint64_t handle = path.empty() ? 0u : m_host.openHostFile(path);
        if (!handle) return false;
        uint64_t size = 0u;
        if (!m_host.hostFileSize(handle, size) || size > 16u * 1024u * 1024u)
        { m_host.closeHostFile(handle); return false; }
        std::vector<uint8_t> data(static_cast<size_t>(size));
        size_t bytesRead = 0u;
        const bool ok = m_host.readHostFile(handle, 0u, data.data(), data.size(), bytesRead);
        m_host.closeHostFile(handle);
        if (!ok || bytesRead != data.size()) return false;
        size_t pos = 0u;
        while (pos + 8u <= data.size())
        {
            const uint32_t sector = readLittle32(data.data() + pos);
            const uint32_t length = readLittle32(data.data() + pos + 4u);
            pos += 8u;
            if (sector == 0xFFFFFFFFu) break;
            const size_t start = pos;
            while (pos < data.size() && data[pos] != 0u) ++pos;
            if (pos == data.size()) { m_archiveEntries.clear(); return false; }
            std::string_view name(reinterpret_cast<const char *>(data.data() + start), pos - start);
            const std::string key = archiveKey(name);
            if (!key.empty()) m_archiveEntries.emplace(key, ArchiveEntry{uint64_t(sector) * 2048u, length});
            pos = (pos + 4u) & ~size_t(3u);
        }
        return !m_archiveEntries.empty();
    }

    bool IopIoman::openGameArchive(std::string_view guestPath, OpenFile &file)
    {
        if (!loadGameArchiveIndex()) return false;
        const auto found = m_archiveEntries.find(archiveKey(guestPath));
        if (found == m_archiveEntries.end()) return false;
        const std::string path = m_host.translateGuestPath("host0:DATAP.WAD");
        const uint64_t handle = path.empty() ? 0u : m_host.openHostFile(path);
        uint64_t wadSize = 0u;
        if (!handle || !m_host.hostFileSize(handle, wadSize) ||
            found->second.offset > wadSize || found->second.size > wadSize - found->second.offset)
        {
            if (handle) m_host.closeHostFile(handle);
            return false;
        }
        file = OpenFile{handle, 0u, found->second.size, found->second.offset};
        return true;
    }

    bool IopIoman::dispatchImport(uint16_t ordinal, IopCpuState &cpu, IopGuestExecutor &executor)
    {
        constexpr size_t kMaxDevices = 16u;
        const uint32_t a0 = cpu.gpr[4];
        const auto setV0 = [&](uint32_t value)
        {
            cpu.gpr[2] = value;
        };

        switch (ordinal)
        {
        case 4: // open, read-only host and disc files
        {
            const std::string guest = m_memory.readString(a0, 1024u);
            const uint32_t flags = cpu.gpr[5];
            if (guest.empty() || (flags & 3u) != 1u || m_files.size() >= 256u)
            {
                setV0(0xFFFFFFFFu);
                return true;
            }
            const std::string path = m_host.translateGuestPath(guest);
            const uint64_t handle = path.empty() ? 0u : m_host.openHostFile(path);
            uint64_t size = 0;
            OpenFile file{};
            if (handle && m_host.hostFileSize(handle, size))
                file = OpenFile{handle, 0u, size, 0u};
            else
            {
                if (handle) m_host.closeHostFile(handle);
                if (!openGameArchive(guest, file))
                {
                    m_host.log(LogLevel::Warning, "[IOP:ioman] open failed: " + guest);
                    setV0(0xFFFFFFFFu);
                    return true;
                }
            }
            const uint32_t fd = m_nextFd++;
            m_files.emplace(fd, file);
            m_host.log(LogLevel::Info, "[IOP:ioman] open: " + guest + " fd=" + std::to_string(fd) + " size=" + std::to_string(file.size));
            setV0(fd);
            return true;
        }
        case 5: // close
        {
            auto it = m_files.find(a0);
            if (it == m_files.end()) { setV0(0xFFFFFFFFu); return true; }
            m_host.closeHostFile(it->second.handle);
            m_files.erase(it);
            setV0(0u);
            return true;
        }
        case 6: // read
        {
            auto it = m_files.find(a0);
            const uint32_t address = cpu.gpr[5], size = cpu.gpr[6];
            if (it == m_files.end() || size > IopMemory::RamSize)
            { setV0(0xFFFFFFFFu); return true; }
            const uint64_t remaining = it->second.offset < it->second.size ? it->second.size - it->second.offset : 0u;
            const size_t wanted = static_cast<size_t>(std::min<uint64_t>(size, remaining));
            std::vector<uint8_t> bytes(wanted);
            size_t read = 0;
            if ((wanted && !m_host.readHostFile(it->second.handle, it->second.base + it->second.offset, bytes.data(), bytes.size(), read)) ||
                (read && !m_memory.writeRam(address, bytes.data(), read)))
            { setV0(0xFFFFFFFFu); return true; }
            it->second.offset += read;
            setV0(static_cast<uint32_t>(read));
            return true;
        }
        case 8: // lseek
        {
            auto it = m_files.find(a0);
            if (it == m_files.end()) { setV0(0xFFFFFFFFu); return true; }
            const int64_t offset = static_cast<int32_t>(cpu.gpr[5]);
            const uint32_t whence = cpu.gpr[6];
            if (whence > 2u || it->second.offset > INT32_MAX || it->second.size > INT32_MAX)
            { setV0(0xFFFFFFFFu); return true; }
            const int64_t base = whence == 0u ? 0 : whence == 1u ? static_cast<int64_t>(it->second.offset) : static_cast<int64_t>(it->second.size);
            const int64_t position = base + offset;
            if (position < 0 || position > INT32_MAX) { setV0(0xFFFFFFFFu); return true; }
            it->second.offset = static_cast<uint64_t>(position);
            setV0(static_cast<uint32_t>(position));
            return true;
        }
        case 20: // AddDrv
        {
            if (a0 == 0u || m_devices.size() >= kMaxDevices)
            {
                setV0(0xFFFFFFFFu);
                return true;
            }

            const uint32_t nameAddress = m_memory.read32(a0);
            const uint32_t operations = m_memory.read32(a0 + 16u);
            const std::string name = m_memory.readString(nameAddress, 64u);
            if (nameAddress == 0u || operations == 0u || name.empty())
            {
                setV0(0xFFFFFFFFu);
                return true;
            }

            m_devices.push_back({a0, cpu.gpr[28], name});
            const uint32_t init = m_memory.read32(operations);
            if (init != 0u)
            {
                const int32_t result = static_cast<int32_t>(
                    executor.executeGuestFunction(init, a0, 0u, 0u, 0u, cpu.gpr[28]));
                if (result < 0)
                {
                    m_devices.pop_back();
                    setV0(0xFFFFFFFFu);
                    return true;
                }
            }

            setV0(0u);
            return true;
        }
        case 21: // DelDrv
        {
            const std::string name = m_memory.readString(a0, 64u);
            const auto device = std::find_if(
                m_devices.begin(), m_devices.end(),
                [&](const Device &candidate)
                { return candidate.name == name; });
            if (device == m_devices.end())
            {
                setV0(0xFFFFFFFFu);
                return true;
            }

            const uint32_t operations = m_memory.read32(device->address + 16u);
            const uint32_t deinit = operations != 0u ? m_memory.read32(operations + 4u) : 0u;
            if (deinit != 0u)
                (void)executor.executeGuestFunction(deinit, device->address, 0u, 0u, 0u, device->gp);
            m_devices.erase(device);
            setV0(0u);
            return true;
        }
        default:
            return false;
        }
    }
}
