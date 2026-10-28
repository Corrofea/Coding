#include <cstdio>
int num[50];
unsigned int n;
int main() {
    scanf("%d", &n);
    while (1) {
        if (n <= 9) {
            break;
        }
        unsigned int tmp = 0, x = 1;
        while (n != 0) {
            tmp = n % 10;
            if (tmp != 0)
                x *= tmp;
            n /= 10;
        }
        n = x;
    }
    printf("%d", n);
    return 0;
}