/* Experiment 06 — Memory Manifold
 * C shim: calls MemProbe() N times, measures RSS before and after.
 * Demonstrates zero temporal curvature: N calls accumulate no memory.
 * The function is stateless — past calls leave no trace in the address space.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern int MemProbe(void);

static long read_rss_kb(void) {
    FILE* f = fopen("/proc/self/status", "r");
    if (!f) return -1;
    char line[256];
    long rss = -1;
    while (fgets(line, sizeof(line), f)) {
        if (strncmp(line, "VmRSS:", 6) == 0) {
            sscanf(line + 6, "%ld", &rss);
            break;
        }
    }
    fclose(f);
    return rss;
}

int main(int argc, char* argv[]) {
    int n_calls = (argc > 1) ? atoi(argv[1]) : 1;
    if (n_calls < 1) { fprintf(stderr, "n_calls must be >= 1\n"); return 1; }

    long rss0 = read_rss_kb();

    volatile int sink = 0;
    for (int i = 0; i < n_calls; i++)
        sink = MemProbe();

    long rss1 = read_rss_kb();

    printf("n_calls=%d  rss_before=%ld  rss_after=%ld  delta=%ld  probe=%d\n",
           n_calls, rss0, rss1, rss1 - rss0, (int)sink);
    return 0;
}
