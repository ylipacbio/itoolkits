#include <sys/resource.h>
#include <sys/time.h>
#include <cstdint>

#include "MemoryConsumption.h"

namespace PacBio {
int64_t MemoryConsumption::PeakRss()
{
    struct rusage r;
    getrusage(RUSAGE_SELF, &r);
#ifdef __linux__
    return r.ru_maxrss * 1024;
#else
    return r.ru_maxrss;
#endif
}
}  // namespace PacBio
