#include <cstdio>
int main() {
    char ch[5];
    int num = 0;
    for (int i = 1; i <= 3; i++) {
        scanf("%c", &ch[i]);
        int tmp;
        if (ch[i] <= 64)
            tmp = ch[i] - '0';
        else
            tmp = ch[i] - 55;
        for (int j = 1; j <= 3 - i; j++)
            tmp *= 15;
        num += tmp;
    }
    ch[1] = '0';
    for (int i = 1; i <= 4; i++) {
        int tmp = num % 7;
        ch[5 - i] = tmp + '0';
        num /= 7;
    }
    for (int i = 1; i <= 4; i++)
        printf("%c", ch[i]);
    return 0;
}