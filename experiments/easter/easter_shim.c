/* ------------------------------------------------------------
 * easter_shim.c -- Linux orchestration wrapper
 * Calls the pure-assembly EasterDate(year) and prints result.
 *
 * EasterDate returns EAX = month * 100 + day  (standard C int).
 *
 * Usage:  ./easter_asm <year>
 * Output: <month> <day>   (e.g. "4 20")
 * ------------------------------------------------------------ */

#include <stdio.h>
#include <stdlib.h>

/* EasterDate(int year) -> int (month * 100 + day)
 * Defined in easter_linux.asm, System V x86-64 ABI. */
extern int EasterDate(int year);

int main(int argc, char *argv[])
{
    int year = 1964;
    if (argc >= 2)
        year = atoi(argv[1]);

    if (year < 1583 || year > 9999) {
        fprintf(stderr, "Gauss Easter is for years 1583 to 9999\n");
        return 1;
    }

    int packed = EasterDate(year);
    int month  = packed / 100;
    int day    = packed % 100;

    printf("%d %d\n", month, day);
    return 0;
}
