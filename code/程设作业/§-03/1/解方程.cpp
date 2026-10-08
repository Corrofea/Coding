#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <math.h>
double deal(double tmp) {
    if (tmp == 0)
        return 0.0;
    if (tmp < 0 && fabs(tmp) < 1e-6)
        return -tmp;
    else
        return tmp;
}
int main() {
    double a, b, c, d, x, y, z;
    scanf("%lf %lf %lf", &a, &b, &c);
    d = (b * b) - (4 * a * c);
    if (fabs(d) < 1e-9)
        d = 0.0;
    if (d >= 0) {
        x = (-b + sqrt(d)) / (2 * a);
        y = (-b - sqrt(d)) / (2 * a);
    }
    if (d < 0) {
        printf("Error");
    } else if (d == 0 || fabs(x - y) < 1e-6) {
        x = deal(x);
        printf("%.6lf", x);
    } else {
        x = deal(x);
        y = deal(y);
        if (x > y) {
            printf("%.6lf\n%.6lf", x, y);
        } else
            printf("%.6lf\n%.6lf", y, x);
    }
    return 0;
}
