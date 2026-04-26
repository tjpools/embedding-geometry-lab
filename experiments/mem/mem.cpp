// Experiment 06 — Memory Manifold
// C++ substrate: measures RSS as a function of "context" size.
//
// A stateless computation costs the same regardless of call count.
// Adding explicit state (malloc'd context) grows RSS linearly — slope = 1.
// This is the baseline: memory cost equals data cost. No architectural overhead.
//
// Contrast: transformer KV cache grows at ~22 KB/token, not 1 byte/byte.
// The architecture imposes a curvature tax on every token of past.

#include <cstdio>
#include <cstdlib>
#include <cstring>

static long read_rss_kb() {
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
    int context_kb = (argc > 1) ? atoi(argv[1]) : 0;
    if (context_kb < 0) { fprintf(stderr, "context_kb must be >= 0\n"); return 1; }

    long rss0 = read_rss_kb();

    // Allocate "context" — simulated past; touch every page to commit RSS
    volatile char* ctx = nullptr;
    if (context_kb > 0) {
        ctx = (volatile char*)malloc((size_t)context_kb * 1024);
        if (!ctx) { fprintf(stderr, "malloc failed\n"); return 1; }
        for (size_t i = 0; i < (size_t)context_kb * 1024; i += 4096)
            ctx[i] = (char)(i & 0xFF);
    }

    long rss1 = read_rss_kb();

    printf("context_kb=%d  rss_before=%ld  rss_after=%ld  delta=%ld\n",
           context_kb, rss0, rss1, rss1 - rss0);

    if (ctx) free((void*)ctx);
    return 0;
}
