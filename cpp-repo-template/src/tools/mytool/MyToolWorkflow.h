// Author: Yuan Li

#pragma once

#include <pbcopper/cli/CLI.h>

namespace PacBio {
namespace MyTool {
struct MyToolWorkflow
{
    static int Runner(const PacBio::CLI::Results& options);
};
}  // namespace MyTool
}  // namespace PacBio
