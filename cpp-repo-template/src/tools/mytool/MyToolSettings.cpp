// Author: Yuan Li

#include <ctype.h>
#include <tools/PlainOption.h>

#include "MyToolVersion.h"
#include "MyToolSettings.h"

namespace PacBio {
namespace MyTool {
namespace OptionNames {
using PlainOption = Data::PlainOption;
// clang-format off
static const CLI::Option HelpOption{
    "help",
    {"h","help"},
    "Output this help.",
    CLI::Option::BoolType()
};
static const CLI::Option VersionOption{
    "version",
    {"version"},
    "Output version information.",
    CLI::Option::BoolType()
};
static const CLI::Option LogLevelOption{
    "log_level",
    {"log-level"},
    R"(Set log level: "TRACE", "DEBUG", "INFO", "WARN", "FATAL".)",
    CLI::Option::StringType("WARN"),
    {"TRACE", "DEBUG", "INFO", "WARN", "FATAL"}
};
const PlainOption LogFile{
    "log_file",
    { "log-file" },
    "Log to a File",
    "Log to a file, instead of stderr.",
    CLI::Option::StringType("")
};
/*const PlainOption AbsoluteCoverageJoined{
    "sl3_abs_joined_coverage",
    { "call-min-reads-all-samples" },
    "Minimum Reads that Support Variant (total over all samples)",
    "Ignore calls supported by < N reads total across samples.",
    CLI::Option::IntType(2)
};*/
// clang-format on
}  // namespace OptionNames

MyToolSettings::MyToolSettings(const PacBio::CLI::Results& options)
    : CLI(options.InputCommandLine())
    , InputFiles(options.PositionalArguments())
    , LogFile{options[OptionNames::LogFile].get<decltype(LogFile)>()}
    , LogLevel{options.LogLevel()}
{
}

PacBio::CLI::Interface MyToolSettings::CreateCLI()
{
    const auto version = PacBio::MyToolVersion() + " (commit " + PacBio::MyToolGitSha1() + ")";

    PacBio::CLI::Interface i{"mytool",
                             "MyTool transcripts based on genomic mapping.",
                             version};

    // clang-format off
    i.AddPositionalArguments({
        { "in.file", "my input", "<myinput.bam>" },
        { "out.file", "my output", "<out.fastq>" }
    });

    i.AddGroup("Basic Options", {
        OptionNames::HelpOption,
        OptionNames::VersionOption,
        OptionNames::LogFile,
        OptionNames::LogLevelOption,
    });
    // clang-format on

    return i;
}
}  // namespace MyTool
}  // namespace PacBio
