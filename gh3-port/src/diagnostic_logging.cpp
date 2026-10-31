#include <iostream>

// Keep the last diagnostic messages visible if the early prototype is stopped.
namespace {
struct FlushDiagnostics {
    FlushDiagnostics() {
        std::cout.setf(std::ios::unitbuf);
        std::cerr.setf(std::ios::unitbuf);
    }
} flush_diagnostics;
}
