#include <cstdio>
#define MAXX 17
int n, num[MAXX];
int main() {
    num[0] = 1;
    num[1] = 3;
    scanf("%d", &n);
    if (n != 0 || n != 1)
        for (int i = 2; i <= n; i++) {
            num[i] = 4 * num[i - 1] - num[i - 2];
        }
    printf("%d", num[n]);
    return 0;
}