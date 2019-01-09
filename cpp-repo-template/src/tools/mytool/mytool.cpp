// Author: Yuan Li

#include <iostream>
#include <stdexcept>

#include <pbcopper/cli/CLI.h>

#include "MyToolSettings.h"
#include "MyToolWorkflow.h"

int main(int argc, char* argv[])
{
    try {
        return PacBio::CLI::Run(argc, argv, PacBio::MyTool::MikeSettings::CreateCLI(),
                                &PacBio::MyTool::MyToolWorkflow::Runner);
    } catch (const std::runtime_error& e) {
        PBLOG_FATAL << "ERROR: " << e.what();
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}
