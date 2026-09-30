#include <cstdio>
int main() {
    double sale, rate, tax;
    scanf("%lf%lf", &sale, &rate);
    tax = sale * rate;
    printf("%.2lf", tax);
    return 0;
}