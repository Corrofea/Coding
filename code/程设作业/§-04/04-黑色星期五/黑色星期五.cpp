#include <iostream>
#include <iomanip>
using namespace std;

bool isLeap(int year) {
    return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
}

int main() {
    int year;
    cin >> year;

    int days = 0;
    for (int y = 1998; y < year; y++) {
        if (isLeap(y))
            days += 366;
        else
            days += 365;
    }

    int current_weekday = (4 + days) % 7;

    int month_days[13] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    if (isLeap(year))
        month_days[2] = 29;

    for (int month = 1; month <= 12; month++) {
        int day13_weekday = (current_weekday + 12) % 7;

        if (day13_weekday == 5) {
            cout << year << "-"
                 << setfill('0') << setw(2) << month << "-13" << endl;
        }

        current_weekday = (current_weekday + month_days[month]) % 7;
    }

    return 0;
}