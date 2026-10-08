#include <cstdio>
using namespace std;
int num[10000], cnt;
int main() {
    while ((num[++cnt] = getchar()) != '\n') {
    };
    for (int i = cnt; i >= 1; i--)
        printf("%c", num[i]);
    return 0;
}