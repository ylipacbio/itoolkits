// Author: Armin Töpfer

#include <sys/resource.h>
#include <sys/time.h>
#include <sstream>

#include "Timer.h"

namespace PacBio {
Timer::Timer() { Restart(); }

float Timer::ElapsedMilliseconds() const
{
    if (frozen_) {
        return std::chrono::duration_cast<std::chrono::milliseconds>(tock_ - tick_).count();
    } else {
        auto tock = std::chrono::steady_clock::now();
        return std::chrono::duration_cast<std::chrono::milliseconds>(tock - tick_).count();
    }
}

float Timer::ElapsedSeconds() const { return ElapsedMilliseconds() / 1000; }

std::string Timer::ElapsedTime() const
{
    std::chrono::time_point<std::chrono::steady_clock> tock;
    if (frozen_)
        tock = tock_;
    else
        tock = std::chrono::steady_clock::now();
    auto t = std::chrono::duration_cast<std::chrono::nanoseconds>(tock - tick_).count();

    auto d = t / 10000 / 1000 / 1000 / 60 / 60 / 24;
    auto h = (t / 1000 / 1000 / 1000 / 60 / 60) % 24;
    auto m = (t / 1000 / 1000 / 1000 / 60) % 60;
    auto s = (t / 1000 / 1000 / 1000) % 60;
    auto ms = (t / 1000 / 1000) % 1000;
    auto us = (t / 1000) % 1000;
    auto ns = t % 1000;
    std::ostringstream ss;
    if (d > 0) ss << d << "d ";
    if (h > 0) ss << h << "h ";
    if (m > 0 && d == 0) ss << m << "m ";
    if (s > 0 && h == 0) ss << s << "s ";
    if (ms > 0 && m == 0) ss << ms << "ms ";
    if (us > 0 && s == 0) ss << us << "us ";
    if (ns > 0 && ms == 0) ss << ns << "ns ";
    return ss.str();
}

void Timer::Restart()
{
    tick_ = std::chrono::steady_clock::now();
    frozen_ = false;
}
void Timer::Freeze()
{
    tock_ = std::chrono::steady_clock::now();
    frozen_ = true;
}

double Timer::CpuTime()
{
    struct rusage r;
    getrusage(RUSAGE_SELF, &r);
    return r.ru_utime.tv_sec + r.ru_stime.tv_sec + 1e-6 * (r.ru_utime.tv_usec + r.ru_stime.tv_usec);
}

std::string Timer::ElapsedTimeFromSeconds(int64_t nanosecs)
{
    auto d = nanosecs / 1000 / 1000 / 1000 / 60 / 60 / 24;
    auto h = (nanosecs / 1000 / 1000 / 1000 / 60 / 60) % 24;
    auto m = (nanosecs / 1000 / 1000 / 1000 / 60) % 60;
    auto s = (nanosecs / 1000 / 1000 / 1000) % 60;
    auto ms = (nanosecs / 1000 / 1000) % 1000;
    auto us = (nanosecs / 1000) % 1000;
    auto ns = nanosecs % 1000;
    std::ostringstream ss;
    if (d > 0) ss << d << "d ";
    if (h > 0) ss << h << "h ";
    if (m > 0 && d == 0) ss << m << "m ";
    if (s > 0 && h == 0) ss << s << "s ";
    if (ms > 0 && m == 0) ss << ms << "ms ";
    if (us > 0 && s == 0) ss << us << "us ";
    if (ns > 0 && ms == 0) ss << ns << "ns ";
    return ss.str();
}
}  // namespace PacBio
