// Author: Armin Töpfer

#pragma once

#include <string>
#include <vector>

#include <pbcopper/cli/CLI.h>

namespace PacBio {
namespace MyTool {
/// Contains user provided CLI configuration
struct MyToolSettings
{
    const std::string CLI;
    const std::vector<std::string> InputFiles;
    std::string LogFile;
    Logging::LogLevel LogLevel;

    /// Parses the provided CLI::Results and retrieves a defined set of options.
    MyToolSettings(const PacBio::CLI::Results& options);

    /// Given the description of the tool and its version, create all
    /// necessary CLI::Options for the ccs executable.
    static PacBio::CLI::Interface CreateCLI();
};
}  // namespace MyTool
}  // namespace PacBio
