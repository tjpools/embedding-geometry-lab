// ------------------------------------------------------------
// easter.cpp -- C++ Manifold
// Implements Gauss's Easter algorithm for the Gregorian calendar.
// Variable names match the assembly source exactly.
//
// Usage:  ./easter_cpp <year>
// Output: <month> <day>   (e.g. "4 20")
// ------------------------------------------------------------

#include <cstdlib>
#include <cstdio>

// Returns true and sets month/day on success, false on invalid year.
static bool gauss_easter(int year, int &month, int &day)
{
    if (year < 1583 || year > 9999)
        return false;

    int a = year % 19;
    int b = year / 100;
    int c = year % 100;
    int d = b / 4;
    int e = b % 4;
    int f = (b + 8) / 25;
    int g = (b - f + 1) / 3;
    int h = (19 * a + b - d - g + 15) % 30;
    int i = c / 4;
    int k = c % 4;
    int l = (32 + 2 * e + 2 * i - h - k) % 7;
    int m = (a + 11 * h + 22 * l) / 451;

    month = (h + l - 7 * m + 114) / 31;
    day   = (h + l - 7 * m + 114) % 31 + 1;
    return true;
}

int main(int argc, char *argv[])
{
    int year = 1964;                          // default if no arg
    if (argc >= 2)
        year = std::atoi(argv[1]);

    int month, day;
    if (!gauss_easter(year, month, day)) {
        std::fprintf(stderr, "Gauss Easter is for years 1583 to 9999\n");
        return 1;
    }

    std::printf("%d %d\n", month, day);
    return 0;
}
