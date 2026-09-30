"""点阵画生成器 —— 自己留着改文案，别把这个文件发给对方。

把文字渲染成 0/1 点阵，烤成好几档分辨率，打包（zlib + base64）写进成品脚本里。
成品脚本里只有乱码数据，看不到文字、字体，也不需要 Pillow。

    python3 banner_gen.py            # 生成成品
    python3 banner_gen.py -          # 打到屏幕上看一眼（不写文件）
"""

import base64
import sys
import zlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ------------------------- 可以改的配置 -------------------------
LINES = [
    "Happy 19th",
    "birthday",
    "lxt",
]
LINE_ROWS = 20       # 每行文字（含上下留白）占几行点阵，越大越细腻
LINE_GAP = 0         # 行与行之间额外空几行
FRAME = True         # 是否给整幅画加一圈边框
OUT_PATH = "2026.09.23.py"   # 成品写到哪

# 烤这些宽度档位（实际列数会小于等于它），运行时挑塞得进终端的那档。
# 列数多就一定看得清，但要自己试：加了档等于给窄终端也多留一手。
TIER_CAPS = [160, 140, 120, 100, 82, 66, 52, 40, 30]
# ---------------------------------------------------------------

CELL_ASPECT = 0.5    # 终端字符格大概 1 宽 2 高，缩图时抵消掉
ON, OFF = "1", "0"   # 打包时用的原始字符，成品里会被翻译成它自己的 ON/OFF
RENDER_SIZE = 200    # 先按这个字号渲染大图，再缩小
FONT_PATHS = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Black.ttf",
    "/System/Library/Fonts/Supplemental/Verdana Bold.ttf",
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]


def load_font(size=RENDER_SIZE):
    for path in FONT_PATHS:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    try:
        return ImageFont.load_default(size)
    except TypeError:             # 老版本 Pillow 的 load_default 不接受字号
        return ImageFont.load_default()


def render_line(text, font, height):
    """把一行文字画到固定高度的画布上（顶边对齐，基线自然一致），
    只裁掉左右空白 —— 上下不裁，各行才能共用同一套缩放。"""
    left, _, right, _ = ImageDraw.Draw(Image.new("L", (1, 1))).textbbox(
        (0, 0), text, font=font)
    img = Image.new("L", (max(right - left, 1), height), 255)
    ImageDraw.Draw(img).text((-left, 0), text, font=font, fill=0)
    return img


def to_bitmap(text, font, rows, height, cols_cap):
    """一行文字 -> 若干字符串，每格是 ON 或 OFF。"""
    img = render_line(text, font, height)
    cols = max(1, round(img.width * rows / (height * CELL_ASPECT)))
    while cols > cols_cap:        # 太宽就整体降分辨率，别折行
        rows = max(1, rows * cols_cap // cols)
        cols = max(1, round(img.width * rows / (height * CELL_ASPECT)))
    px = img.resize((cols, rows), Image.LANCZOS).load()
    return ["".join(ON if px[x, y] < 128 else OFF for x in range(cols))
            for y in range(rows)]


def build(font, cols_cap):
    """多行文字竖着拼起来，左右补 OFF 居中对齐。"""
    ascent, descent = font.getmetrics()
    height = ascent + descent         # 所有行共用这个高度，缩放才一致
    blocks = [to_bitmap(line, font, LINE_ROWS, height, cols_cap)
              for line in LINES]
    width = max(len(row) for block in blocks for row in block)
    gap = [OFF * width] * LINE_GAP
    art = []
    for i, block in enumerate(blocks):
        art += [row.center(width, OFF) for row in block]
        if i < len(blocks) - 1:
            art += gap
    return trim_blank(art)


def trim_blank(bitmap):
    """去掉上下多余的全空行。"""
    blank = OFF * len(bitmap[0])
    while len(bitmap) > 1 and bitmap[0] == blank:
        bitmap = bitmap[1:]
    while len(bitmap) > 1 and bitmap[-1] == blank:
        bitmap = bitmap[:-1]
    return bitmap


def add_frame(bitmap):
    width = len(bitmap[0])
    return ([OFF * (width + 2)]
            + [OFF + row + OFF for row in bitmap]
            + [OFF * (width + 2)])


def pack(bitmap):
    """点阵按位打包（每个字节 8 个像素），再 zlib + base64 成一行文本。"""
    bits = "".join(bitmap)
    bits += "0" * (-len(bits) % 8)            # 补齐到整字节
    raw = bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8))
    return base64.b64encode(zlib.compress(raw, 9)).decode()


TEMPLATE = '''\
"""__TITLE__ —— 用 0/1 打印一幅画。

直接跑就行：python3 __NAME__

只用到 Python 自带库，不用装任何东西。加 --animate 会一行行刷出来。
"""

import base64
import shutil
import sys
import time
import zlib

ON, OFF = "1", "0"        # 想换成 "#" 和空格就改这里（必须是单个字符）
ANIMATE = "--animate" in sys.argv

# 同一幅画烤了 __NTIERS__ 档分辨率，运行时自动挑塞得进终端窗口的最大一档。
# 每档是 (列数, 按位打包后 zlib + base64 的点阵)。
TIERS = [
__TIERS__
]


def decode(cols, blob):
    """把打包的数据还原成一列列字符。"""
    bits = "".join(f"{b:08b}" for b in zlib.decompress(base64.b64decode(blob)))
    table = str.maketrans("01", OFF + ON)
    return [bits[i:i + cols].translate(table) for i in range(0, len(bits), cols)]


def main():
    # 读不到终端宽度时（管道、重定向）就当它有最宽那档那么宽
    width = shutil.get_terminal_size((__FALLBACK__, 24)).columns - 1
    cols, blob = next((t for t in TIERS if t[0] <= width), TIERS[-1])
    for row in decode(cols, blob):
        print(row)
        if ANIMATE:
            sys.stdout.flush()
            time.sleep(0.05)


if __name__ == "__main__":
    main()
'''


def make_tiers(cols_caps=TIER_CAPS):
    font = load_font()
    tiers = []
    for cap in cols_caps:
        art = build(font, cap)
        if FRAME:
            art = add_frame(art)
        tiers.append((len(art[0]), pack(art)))
    return tiers


def render_source(title, name, tiers):
    rows = "\n".join(f'    ({cols}, "{blob}"),' for cols, blob in tiers)
    return (TEMPLATE
            .replace("__TITLE__", title)
            .replace("__NAME__", name)
            .replace("__NTIERS__", str(len(tiers)))
            .replace("__FALLBACK__", str(max(cols for cols, _ in tiers) + 1))
            .replace("__TIERS__", rows))


def main():
    to_stdout = "-" in sys.argv[1:]
    name = Path(OUT_PATH).name
    title = Path(OUT_PATH).stem
    tiers = make_tiers()
    source = render_source(title, name, tiers)

    if to_stdout:
        print(source)
        return
    Path(OUT_PATH).write_text(source, encoding="utf-8")
    print(f"已写入 {OUT_PATH}（{len(tiers)} 档，"
          f"{sum(len(b) for _, b in tiers) // 1000} KB 数据，"
          f"最宽 {max(c for c, _ in tiers)} 列）")


if __name__ == "__main__":
    main()
