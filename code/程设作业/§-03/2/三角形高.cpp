#include <cstdio>
#include <cmath>
#include <utility>
using namespace std;
int main() {
    double a, b, c, p, S, h;
    scanf("%lf%lf%lf", &a, &b, &c);
    if (c < b)
        swap(b, c);
    if (b < a)
        swap(a, b);
    if (c < b)
        swap(b, c);
    if (a + b <= c)
        printf("NO");
    else {
        p = (a + b + c) / 2;
        S = sqrt(p * (p - a) * (p - b) * (p - c));
        h = 2 * S / c;
        printf("%lf", h);
    }
    return 0;
}