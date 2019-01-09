// Author: Armin Töpfer

#include <algorithm>
#include <fstream>
#include <string>
#include <cstring>
#include <tuple>
#include <vector>

#include <iostream>
#include <stdio.h>

namespace PacBio {
namespace MyTool {

struct BuildVersion
{
    BuildVersion(std::string versionStr)
    {
        sscanf(versionStr.c_str(), "%d.%d.%d", &major, &minor, &revision);
    }

    bool operator<(const BuildVersion& otherVersion)
    {
        if (major < otherVersion.major) return true;
        if (minor < otherVersion.minor) return true;
        if (revision < otherVersion.revision) return true;
        return false;
    }

    int major, minor, revision;
};

int MyToolWorkflow::Runner(const PacBio::CLI::Results& options)
{
    const Timer startTime;

    std::ofstream logStream;
    {
        const std::string logFile = options["log_file"];
        const Logging::LogLevel logLevel(options["log_level"].get<std::string>());

        using Logger = PacBio::Logging::Logger;

        Logger* logger;
        if (!logFile.empty()) {
            logStream.open(logFile);
            logger = &Logger::Default(new Logger(logStream, logLevel));
        } else {
            logger = &Logger::Default(new Logger(std::cerr, logLevel));
        }
        PacBio::Logging::InstallSignalHandlers(*logger);
    }

    auto settings = std::make_shared<MyToolSettings>(options);
    if (options.PositionalArguments().empty()) {
        PBLOG_FATAL << "ERROR: No input file!";
        return EXIT_FAILURE;
    }

    PBLOG_INFO << "Run Time: " << startTime.ElapsedTime();
    PBLOG_INFO << "CPU Time: "
               << Timer::ElapsedTimeFromSeconds(
                      static_cast<int64_t>(Timer::CpuTime() * 1000 * 1000 * 1000));
    PBLOG_INFO << "Peak RSS: " << (MemoryConsumption::PeakRss() / 1024.0 / 1024.0 / 1024.0)
               << " GB";

    return EXIT_SUCCESS;
}

}  // namespace MyTool
}  // namespace PacBio
