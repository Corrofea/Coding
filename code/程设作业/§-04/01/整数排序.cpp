#include <cstdio>
#include <utility>
#define MAXX 1005
using namespace std;
int n, num[MAXX];
int main() {
    scanf("%d", &n);
    for (int i = 1; i <= n; i++) {
        scanf("%d", &num[i]);
    }
    for (int i = n; i >= 2; i--) {
        for (int j = 1; j <= i - 1; j++) {
            if (num[j] > num[j + 1])
                swap(num[j], num[j + 1]);
        }
    }
    for (int i = 1; i <= n; i++) {
        printf("%d ", num[i]);
    }
    return 0;
}