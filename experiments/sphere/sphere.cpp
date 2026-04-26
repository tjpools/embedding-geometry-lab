// Experiment 04 — Sphere Manifold
// C++ substrate: sphere volume via double-precision M_PI
// V = (4/3) * pi * r^3
//
// Epistemic status: M_PI is a compile-time double constant (~15-16 sig digits).
// The "true" volume is transcendental. This is an approximation with known,
// bounded error in the last ULP of the double representation.

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(int argc, char* argv[]) {
    if (argc < 2) {
        fprintf(stderr, "usage: sphere_cpp <radius>\n");
        return 1;
    }
    double r = atof(argv[1]);
    double v = (4.0 / 3.0) * M_PI * r * r * r;
    printf("%.10f\n", v);
    return 0;
}
