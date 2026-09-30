import base64
import shutil
import sys
import time
import zlib

ON, OFF = "1", "0"        # 想换成 "#" 和空格就改这里（必须是单个字符）
ANIMATE = "--animate" in sys.argv

# 同一幅画烤了 9 档分辨率，运行时自动挑塞得进终端窗口的最大一档。
# 每档是 (列数, 按位打包后 zlib + base64 的点阵)。
TIERS = [
    (155, "eNqtkrFu3DAMhilo0MgXKKTX6GBYr9RRBdycjBtuzBv0VaKDh455BRo3ZAyLWwTUMEvn0hQnr+Ei+5fE/xNJgF3Y0v3/6exibIHk8ocUxutMCRAYsylAm8Sp6/GLIY9rECenkexPtM+/haJM00TMKSXNzJU770qyNaF3jx4goXh3LIxO0FwyX7NmNpfCyZuZZr3nkcHQt+1D0bohPuFzXhQNV7ycKbnjn19P42sJAC4fYEk3fIavYOnuZR4cuNo8Vh+wwCeEZkJdzGaZ3rX6RkD9VqJ/1VNwgMEV+KC7rZg3suH92A8x/F3WcCjxNQtVPY9Se1xlkgWFD4KjlqWG01n3BjzSA9qZ1ak3XHuomFk3zBIwgyt9cCUY9gFqkPGqhtVNVC31dqKAZ/aKHHIdwoaW+i2VEUWTVVMjV7SyxFBiuaENIMFQfDnKYHlfi4e9FPJOirSTHH9CJ/xe2srtGi1BOx9vDRzuJTPXGBuqDh9Pa2OgTeobA0befO/RVqjt3EQKLRquOzR34UPeoTXjfB9/AYXizRQ="),
    (142, "eNqlkTFu5DAMRSmoYLMYXcAQr+HCsK/krXYKYayFC5c5Qq4iw4W77BGGRi6gRYooiGGtbOwEMx4kTdhYpqjHT36AfRyEuxx/AEMGkKuPyyP5ugbg4pJQPD33DqT1sY24ZAf41bWP4wIqDqiU1nkN+qALnUGhxJxndf7iEiasHC5ONf900xMIhue+d9L+HYZh7FoP2HYPiHCQY1QLzWhBY6As27rmkKjXogUn1f46Iy0CWfhOpLHXOVPrVd8aBkRqUtN6ubHTr3SAzqRzuZXgtj1a6yBsGWqc0U3szl69cxVK4ZvY++Z1ochN2low6negrg8Jo1o+KTn5El1J6BJGU8JU7eTT1xAYdEcjuVnwjzWp0AhPYvKq46AKEVTX+4TBlkuSTB7jvGImrzGGU2Ubu6ohqEZ3VG8czzDvp5Z+n7lbI949IvedReOdT+Vm8nUckzK+tfxiwgem4zneCNE4DvEWo5Y9hniHsZUtbx5pEf97+QVmPim/V0P82cj/AMyLtNA="),
    (121, "eNqdUL1OwzAQPmMJL1XMyBDZr8AYJCt5lT5CJjAiahJlyNaubDwKV2XIxiMgVx064kx4iDBpVGgiMfUkS/edT/f9AMyKlnjqlvHVAgiaE3TPTQBg0m9p/XpB+ujx0EPumk2oD2sIwqddC5HiLYvu34GxfrnFMND7OowegBZBujQBi7rDRkkgzUeYpte0fvlkmgNgxm/vjhwpLdhES0RQwiWlYbh6owY3oxkFrAAtAMhoRoyzYQPsseN5ufO+fcPcSac52xvrX6vOuj4WglPUOmOl0U4A53VplFIUrdKc+KotrBCCGC1iVu/xq8gk52AV57TZmqRIPKuLXLDKd95JFCvaoNxQXKWJYjjPfQ7lHHK8IAU1h/Ex0cnJ4WVnOCQ0bvzKaewqN3+QmCxL7Pnbyn6qXzNHzYSY9GSyLIgHNyEmHqfEVecSnBFz+5+dHwDJiAE="),
    (100, "eNqNj7FqwzAQhk8Ios0Zung4rFfwqEHgV0kpdE7IUmhJlGbw5ico5FUsMmgJ9AU61GjolqqbCwJVcZtYdCg90OmHT//dL4CxiG6Hm7GuAczl1eT6kTgjjyQcbl7un2Y0Wz4LzKvyFo9QVrnd6MOyWZiWwqKJIFSmF1CuCqsAKMzoZXQ5Ia/wZ5GWqtiARCsgCEAEkAP4TkZP4Xgv1mHnua/i7s7Wse2NmaLATMwRizvJPt42ra2J1mZr3rN5UZwACuncioR9TT51F0ygaRyZaKZGTR38u9KnfPjCCFj7o6fxPFyA57v+DKjtwnmz4z5xhMTBXArUCFIHs26txh1b/zvqFzr6afw="),
    (79, "eNpjYICBhAYQyWHBxHAYzP848wzjP7t6+40NydZ3D/P4HEs2Yzj4ybBNcuaZZxaMLceSGRiaFTcUMLCxARWzMTMeYMABHvAxCBxgsGBgACl52MBQwMDA/M/i/+d/9o//PG7nKzzYLvPwgMUxPpnHzDyWh/s/3pGzPMYmU3jc4uEH+8c9/AYP/9kfhBvO3ABj2TAQAh/gmh7ANDIDDZIHi7ED+XZgFj//wZ//wbJy7McP/4cYzv6fEaK9gv0HSDvIOPYP7GB3MD6Q/8APNa7+A9S45o8/7A9AjYOyYAAArI9Q+g=="),
    (65, "eNpjYIAAJgMgIfjkAOPMt/N8OCbnMPRuy5zC4mnE4HY7vYfJ5iYDA2MTHwMyEIBQBjyMPQwSDAzyx+qff/xTl8xnbJEseYzdsk1yhmHPYcve5h9nZI7Zzz3cAFHOeABCMx9gwAkqoHQNEBcAsRwQ/wBifqgYe/uDP/8PgMz48aP+AdDMB/Y/+EHmf+D/wA4yt4L5BzNQnMGG+R/jB5ABzP8bwAawP/5Q3wAxQP4B3D4ADPM8Mw=="),
    (51, "eNpjYAABpgQGBp5tB3Jf5iZMusW5du0MwVsODIpNDDDAwcHQwMHAuFF/Nr+Mi3GasVnS2bacY2lnbjzYMeFE30wZsCJ2BiyAvQFEMn4A4gMMckDmDwbmAwwM8gwMFXX85/8w8DM/fvi/gfGB/Q/+BgYb5j9AlewN9g12DAwf+H+wA7Uw/28Aajn444/8A5CWg/+gBgMA5yIyaw=="),
    (41, "eNpjYAACaQUXzhDefStbXh1gFmhggAAnTsYGBtWUaVcWiE329jYACRkwoIEPIOIHAwNzQw2QOGAHJD7I8x9+/o+/8fuBH+wH6g/YMD+QPyDH+IH/AT/DD/4/7A018vLML+zk2R/+A+mVgJgDAPN6IZs="),
    (31, "eNpjYGBg2OopvoIphQEEmEVXnGBbGbobyGRhgAILIC5gYG54wMDOeLzf/nDzHxl25gcWfOwPCmTkHzyw+PjxB0gZADbsEwk="),
]


def decode(cols, blob):
    """把打包的数据还原成一列列字符。"""
    bits = "".join(f"{b:08b}" for b in zlib.decompress(base64.b64decode(blob)))
    table = str.maketrans("01", OFF + ON)
    return [bits[i:i + cols].translate(table) for i in range(0, len(bits), cols)]


def main():
    # 读不到终端宽度时（管道、重定向）就当它有最宽那档那么宽
    width = shutil.get_terminal_size((156, 24)).columns - 1
    cols, blob = next((t for t in TIERS if t[0] <= width), TIERS[-1])
    for row in decode(cols, blob):
        print(row)
        if ANIMATE:
            sys.stdout.flush()
            time.sleep(0.05)


if __name__ == "__main__":
    main()
