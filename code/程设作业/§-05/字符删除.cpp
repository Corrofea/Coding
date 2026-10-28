#include <string.h>
#include <stdio.h>
int main() // 第二行输入单独的一个字符ch。要求程序把字符串str当中所有的ch字符都删除，从而得到一个新的字符串，输出新的字符串。
{
    char str[20];
    fgets(str, 20, stdin);
    int length = strlen(str);
    char ch;
    scanf("%c", &ch);
    int i;
    i = 0;
    while (i < length - 1) {
        if (str[i] != ch) {
            printf("%c", str[i]);
        }
        i++;
    }
    return 0;
}