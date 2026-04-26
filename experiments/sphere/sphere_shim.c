/* Experiment 04 — Sphere Manifold
 * C shim: parse argv[1] as double radius, call ASM SphereVolume, print result
 */
#include <stdio.h>
#include <stdlib.h>

extern double SphereVolume(double r);

int main(int argc, char* argv[]) {
    if (argc < 2) {
        fprintf(stderr, "usage: sphere_asm <radius>\n");
        return 1;
    }
    double r = atof(argv[1]);
    double v = SphereVolume(r);
    printf("%.10f\n", v);
    return 0;
}
