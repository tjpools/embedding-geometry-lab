/* Experiment 05 — Base Manifold
 * C shim: calls ASM BaseAdd(), applies frame (base) annotation, prints result.
 * The ASM knows only the quantity (7). This layer knows the coordinate system.
 */
#include <stdio.h>
#include <stdlib.h>

extern int BaseAdd(void);

static void to_base(int n, int base, char* buf) {
    const char* digits = "0123456789ABCDEF";
    char tmp[64];
    int i = 0;
    if (n == 0) { buf[0] = '0'; buf[1] = '\0'; return; }
    while (n > 0) {
        tmp[i++] = digits[n % base];
        n /= base;
    }
    for (int j = 0; j < i; j++) buf[j] = tmp[i - 1 - j];
    buf[i] = '\0';
}

int main(int argc, char* argv[]) {
    int base = (argc > 1) ? atoi(argv[1]) : 10;
    if (base < 2 || base > 16) {
        fprintf(stderr, "base must be 2-16\n");
        return 1;
    }
    int result = BaseAdd();   /* quantity from ASM: 7 */
    char buf[64];
    to_base(result, base, buf);
    printf("%s\n", buf);
    return 0;
}
