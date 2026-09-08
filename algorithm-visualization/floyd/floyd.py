from manim import *

INF = "∞"

# —— 全局配色：粉紫 × 蓝绿渐变，科技风 ——
BG = "#120E24"            # 背景：深紫
PINK = "#F6A6D0"          # 粉（渐变起点）
PURPLE = "#A78BFA"        # 紫（渐变终点）
HOTPINK = "#F472B6"       # 待更新 / 落选
TEAL = "#2DD4BF"          # 蓝绿（渐变起点）
GREEN2 = "#34D399"        # 绿（渐变终点）
SUBTITLE_COLOR = "#E4DEF5"  # 字幕：淡紫白
CELL_FILL = "#1A1433"     # 格子底：深紫藏青
CELL_STROKE = "#6E63B8"   # 格子描边：紫灰
INDEX_COLOR = "#A99BC9"   # 行列编号：灰紫

# —— 字体体系 ——
KAITI = "Kaiti SC"        # 汉字：楷体
CODE_FONT = "Menlo"       # 代码相关：无衬线代码体
SERIF = "Times New Roman" # 其他英文：衬线


def mix_text(parts, font_size=28):
    """混排文本：parts = [(文本, 字体, 颜色), ...]，返回一行 VGroup"""
    return VGroup(*[
        Text(t, font=f, font_size=font_size, color=c)
        for t, f, c in parts
    ]).arrange(RIGHT, buff=0.06)


class FloydScene(Scene):
    """热身示例：一次松弛 d[2][0] 经中间点 k=1，从 9 更新为 5。
    图为无向图：邻接矩阵对称 d[i][j] = d[j][i]。"""

    def _build_grid(self, d):
        """把二维数组画成方格矩阵，返回 (整个 VGroup, 方块引用, 文字引用)"""
        n = len(d)
        rows, rects, labels = [], [], []
        for i in range(n):
            row_mobs, row_rects, row_labels = [], [], []
            for j in range(n):
                r = Square(side_length=0.8,
                           stroke_color=CELL_STROKE, stroke_width=1.5,
                           fill_color=CELL_FILL, fill_opacity=1)
                t = Text(str(d[i][j]), font_size=28)
                row_mobs.append(VGroup(r, t))   # 文字叠在方块中心
                row_rects.append(r)
                row_labels.append(t)
            rows.append(VGroup(*row_mobs).arrange(RIGHT, buff=0))
            rects.append(row_rects)
            labels.append(row_labels)
        grid = VGroup(*rows).arrange(DOWN, buff=0)
        return grid, rects, labels

    def construct(self):
        # 3x3 距离矩阵（无向图：三角 0-1=3, 1-2=2, 0-2=9）
        d = [
            [0, 3, 9],
            [3, 0, 2],
            [9, 2, 0],
        ]
        n = 3

        title = mix_text([
            ("Floyd-Warshall", SERIF, PINK),
            ("：松弛 ", KAITI, SUBTITLE_COLOR),
            ("d[2][0]", CODE_FONT, PINK),
            ("，中间点 ", KAITI, SUBTITLE_COLOR),
            ("k = 1", CODE_FONT, PINK),
        ], font_size=34)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))

        grid, rects, labels = self._build_grid(d)
        grid.next_to(title, DOWN, buff=0.8)
        self.play(Create(grid), run_time=1)

        hint = mix_text([
            ("方案：", KAITI, SUBTITLE_COLOR),
            ("2 + 3 = 5", CODE_FONT, TEAL),
            ("，比直连 9 更短，值得更新", KAITI, SUBTITLE_COLOR),
        ], font_size=26)
        hint.next_to(grid, DOWN, buff=0.7)
        self.play(FadeIn(hint), run_time=0.5)

        # 1) 高亮中间点 k=1 的整行整列（紫色十字）
        k = 1
        cross = [rects[k][j] for j in range(n)] + [rects[i][k] for i in range(n)]
        self.play(*[r.animate.set_fill(PURPLE, 0.25) for r in cross], run_time=0.8)

        # 2) 两段路径涂粉，待更新格子描 hot pink
        i, j = 2, 0
        self.play(
            rects[i][k].animate.set_fill(PINK, 0.7),
            rects[k][j].animate.set_fill(PINK, 0.7),
            rects[i][j].animate.set_stroke(HOTPINK, width=6),
        )

        # 3) 公式出场（粉紫渐变）
        formula = MathTex(r"d[2][1] + d[1][0] = 2 + 3 = 5")
        formula.set_color_by_gradient(PINK, PURPLE)
        formula.next_to(hint, DOWN, buff=0.5)
        self.play(Write(formula), run_time=1.2)

        # 4) 更新：9 → 5，格子变蓝绿
        new_label = Text("5", font_size=28)
        self.play(
            Transform(labels[i][j], new_label),
            rects[i][j].animate.set_fill(GREEN2, 0.5).set_stroke(GREEN2, width=4),
            formula.animate.set_color_by_gradient(TEAL, GREEN2),
        )
        self.wait(2)


class Act1_3DArray(ThreeDScene):
    """幕1：Floyd 本质是三维动态规划（约 40s）。
    真 3D 斜视角看三层堆叠的 f[0]/f[1]/f[2]，再抽出 k-1、k 两片，
    分步慢放演示递推，旁配三节点图论示意图（2—1—0）。"""

    def _grid(self, d, cell=0.8, font=26):
        """方格矩阵（z=0 平面），带行列编号，返回 (grid, 方块引用, 文字引用)"""
        n = len(d)
        rows, rects, labels = [], [], []
        for i in range(n):
            row_mobs, row_rects, row_labels = [], [], []
            for j in range(n):
                r = Square(
                    side_length=cell,
                    stroke_color=CELL_STROKE, stroke_width=1.5,
                    fill_color=CELL_FILL, fill_opacity=1,
                )
                t = Text(str(d[i][j]), font_size=font)
                row_mobs.append(VGroup(r, t))
                row_rects.append(r)
                row_labels.append(t)
            rows.append(VGroup(*row_mobs).arrange(RIGHT, buff=0))
            rects.append(row_rects)
            labels.append(row_labels)
        grid = VGroup(*rows).arrange(DOWN, buff=0)
        # 行列编号（行 = 起点 i，列 = 终点 j）
        for i, row in enumerate(rows):
            grid.add(Text(str(i), font_size=18, color=INDEX_COLOR)
                     .next_to(row, LEFT, buff=0.3))
        for j in range(n):
            grid.add(Text(str(j), font_size=18, color=INDEX_COLOR)
                     .next_to(rows[0][j], UP, buff=0.3))
        return grid, rects, labels

    def _graph(self, a, m, b):
        """三节点无向图：a—m—b 路径（粉紫渐变边，权重 2/3）+ a—b 红虚线直连（9）。
        返回 (图组, 引用字典)。"""
        pos = {a: [-1.5, 0, 0], m: [0, 0, 0], b: [1.5, 0, 0]}
        nodes = {
            v: Circle(radius=0.3, color=CELL_STROKE, fill_color=CELL_FILL,
                      fill_opacity=1, stroke_width=1.5).move_to(pos[v])
            for v in (a, m, b)
        }
        node_labels = {v: Text(str(v), font_size=24, font=CODE_FONT)
                       .move_to(nodes[v]) for v in (a, m, b)}
        e1 = Line(nodes[a].get_center(), nodes[m].get_center(), buff=0.3, stroke_width=5)
        e2 = Line(nodes[m].get_center(), nodes[b].get_center(), buff=0.3, stroke_width=5)
        e1.set_color_by_gradient(PINK, PURPLE)
        e2.set_color_by_gradient(PINK, PURPLE)
        w1 = Text("2", font_size=22, font=CODE_FONT, color=PINK).next_to(e1, UP, buff=0.15)
        w2 = Text("3", font_size=22, font=CODE_FONT, color=PINK).next_to(e2, UP, buff=0.15)
        # 虚线直连：标签放在弧顶点（几何中心会压在中间节点上）
        base_arc = ArcBetweenPoints(nodes[a].get_center(), nodes[b].get_center(), angle=0.9)
        arc = DashedVMobject(base_arc, num_dashes=20).set_color(HOTPINK)
        arc_label = Text("9", font_size=22, font=CODE_FONT, color=HOTPINK).move_to(
            base_arc.point_from_proportion(0.5) + UP * 0.25)
        group = VGroup(*nodes.values(), *node_labels.values(), e1, e2, w1, w2, arc, arc_label)
        refs = dict(nodes=nodes, edges=(e1, e2), weights=(w1, w2), arc=arc, arc_label=arc_label)
        return group, refs

    def _caption(self, parts, font_size=26):
        """屏幕钉住的解说字幕（混排字体），位于标题下方，返回 VGroup"""
        cap = mix_text(parts, font_size=font_size)
        cap.next_to(self.title, DOWN, buff=0.35)
        self.add_fixed_in_frame_mobjects(cap)
        return cap

    def construct(self):
        self.camera.background_color = BG

        # 无向图：三角 0-1=3, 1-2=2, 0-2=9，邻接矩阵对称
        d0 = [
            [0, 3, 9],
            [3, 0, 2],
            [9, 2, 0],
        ]
        # k=1 轮后的切片 f[1]：(2,0) 与 (0,2) 由 9 更新为 5
        d1 = [
            [0, 3, 9],
            [3, 0, 2],
            [5, 2, 0],
        ]
        # k=2 轮后的切片 f[2]（此图上与 f[1] 相同）
        d2 = [
            [0, 3, 9],
            [3, 0, 2],
            [5, 2, 0],
        ]

        self.set_camera_orientation(phi=55 * DEGREES, theta=-45 * DEGREES, zoom=0.95)

        # 镜头1：标题（粉紫渐变，混排字体）
        self.title = mix_text([
            ("Floyd", SERIF, PINK),
            (" 的本质：三维动态规划 ", KAITI, SUBTITLE_COLOR),
            ("f[k][i][j]", CODE_FONT, PINK),
        ], font_size=30)
        self.title.set_color_by_gradient(PINK, PURPLE)
        self.title.to_edge(UP, buff=0.35)
        self.add_fixed_in_frame_mobjects(self.title)
        self.play(Write(self.title))
        self.wait(0.5)

        # 镜头2：三层沿 z 方向依次入场（真 3D，斜 55° 视角）
        planes, plane_rects, plane_labels = [], [], []
        for k, d in enumerate([d0, d1, d2]):
            g, rects, labels = self._grid(d)
            g.shift(OUT * 2.4 * k + DOWN * 1.2)
            cap = Text(f"f[{k}]", font_size=28, font=CODE_FONT)
            cap.set_color_by_gradient(PINK, PURPLE)
            cap.next_to(g, LEFT, buff=0.4)
            g.add(cap)          # 标签并入该片，随片移动
            planes.append(g)
            plane_rects.append(rects)
            plane_labels.append(labels)
        for p in planes:
            self.play(FadeIn(p), run_time=0.8)
            self.wait(0.3)
        stack_cap = mix_text([
            ("三维数组 ", KAITI, INDEX_COLOR),
            ("f[k][i][j]", CODE_FONT, INDEX_COLOR),
            ("：沿 ", KAITI, INDEX_COLOR),
            ("k", CODE_FONT, INDEX_COLOR),
            (" 方向堆叠", KAITI, INDEX_COLOR),
        ], font_size=22).move_to([0, -3.0, 0])
        self.add_fixed_in_frame_mobjects(stack_cap)
        self.play(Write(stack_cap), run_time=0.6)

        # 缓慢环绕，展示厚度（看清这是三维结构）
        self.move_camera(theta=-15 * DEGREES, run_time=4)
        self.wait(0.8)

        # 镜头3：取出两片的字幕
        cap2 = self._caption([
            ("取出第 ", KAITI, SUBTITLE_COLOR),
            ("k-1", CODE_FONT, PINK),
            (" 片和第 ", KAITI, SUBTITLE_COLOR),
            ("k", CODE_FONT, PINK),
            (" 片（", KAITI, SUBTITLE_COLOR),
            ("k = 1", CODE_FONT, PINK),
            ("）", KAITI, SUBTITLE_COLOR),
        ])
        self.play(FadeIn(cap2), run_time=0.8)
        self.wait(0.6)

        # 镜头4：飞至正前方，f[0]、f[1] 左右滑开，f[2] 淡出
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.05, run_time=2.5)
        self.play(
            FadeOut(planes[2]), FadeOut(stack_cap),
            planes[0].animate.move_to([-3.4, -0.35, 0]),
            planes[1].animate.move_to([3.4, -0.35, 0]),
            run_time=1.5,
        )
        self.wait(0.5)

        # 镜头5：读入的两格涂粉 —— 配解说，放慢
        k, i, j = 1, 2, 0
        capA = self._caption([
            ("两段已知最短路：", KAITI, SUBTITLE_COLOR),
            ("f[0][2][1] = 2", CODE_FONT, PINK),
            ("，", KAITI, SUBTITLE_COLOR),
            ("f[0][1][0] = 3", CODE_FONT, PURPLE),
        ])
        self.play(FadeOut(cap2), FadeIn(capA), run_time=0.6)
        self.play(
            plane_rects[0][i][k].animate.set_fill(PINK, 0.7),
            plane_rects[0][k][j].animate.set_fill(PINK, 0.7),
            run_time=0.8,
        )
        self.wait(1.2)

        # 镜头6：图论示意图（两片之间上方）
        graph, refs = self._graph(i, k, j)
        graph.move_to([0, 1.85, 0])
        self.play(FadeIn(graph), run_time=1)
        self.wait(0.8)

        # 镜头7：目标格描 hot pink —— 配解说
        capB = self._caption([
            ("待更新：", KAITI, SUBTITLE_COLOR),
            ("f[1][2][0]", CODE_FONT, HOTPINK),
            ("，当前直连 ", KAITI, SUBTITLE_COLOR),
            ("9", CODE_FONT, HOTPINK),
        ])
        self.play(FadeOut(capA), FadeIn(capB), run_time=0.6)
        self.play(plane_rects[1][i][j].animate.set_stroke(HOTPINK, width=6), run_time=0.5)
        self.wait(1.2)

        # 镜头8：两支箭头逐个生长，带上数值标签
        arrow_a = Arrow(
            plane_rects[0][i][k].get_center(),
            plane_rects[1][i][j].get_center(),
            buff=0.3,
        )
        arrow_b = Arrow(
            plane_rects[0][k][j].get_center(),
            plane_rects[1][i][j].get_center(),
            buff=0.3,
        )
        arrow_a.set_color_by_gradient(PINK, PURPLE)
        arrow_b.set_color_by_gradient(PINK, PURPLE)
        tag_a = Text("2", font_size=22, font=CODE_FONT, color=PINK).move_to(
            arrow_a.get_start() + UP * 0.35)
        tag_b = Text("3", font_size=22, font=CODE_FONT, color=PURPLE).move_to(
            arrow_b.get_start() + UP * 0.35)
        self.play(GrowArrow(arrow_a), FadeIn(tag_a), run_time=0.8)
        self.wait(0.6)
        self.play(GrowArrow(arrow_b), FadeIn(tag_b), run_time=0.8)
        self.wait(0.6)

        capC = self._caption([
            ("两段相加 ", KAITI, SUBTITLE_COLOR),
            ("2 + 3 = 5", CODE_FONT, TEAL),
            ("，比直连 9 更短 → 更新！", KAITI, SUBTITLE_COLOR),
        ])
        self.play(FadeOut(capB), FadeIn(capC), run_time=0.6)
        self.wait(1.5)

        # 镜头9：代入公式（三段依次出现）
        formula = VGroup(
            MathTex(r"f[1][2][0]=\min\big(f[0][2][0],\, f[0][2][1]+f[0][1][0]\big)"),
            MathTex(r"=\min(9,\, 2+3)="),
            MathTex("5"),
        ).arrange(RIGHT, buff=0.15).scale(0.8)
        formula.to_edge(DOWN, buff=1.5)
        for piece in formula:
            self.play(FadeIn(piece), run_time=0.8)
            self.wait(0.4)
        self.wait(1)

        # 镜头10：更新 9 → 5，格子与图上路径同步转蓝绿
        new_label = Text("5", font_size=26).move_to(plane_labels[1][i][j])
        self.play(
            Transform(plane_labels[1][i][j], new_label),
            plane_rects[1][i][j].animate.set_fill(GREEN2, 0.5).set_stroke(GREEN2, width=4),
            formula[2].animate.set_color(TEAL),
            FadeOut(refs["arc"]), FadeOut(refs["arc_label"]),
            refs["edges"][0].animate.set_color_by_gradient(TEAL, GREEN2),
            refs["edges"][1].animate.set_color_by_gradient(TEAL, GREEN2),
            refs["weights"][0].animate.set_color(TEAL),
            refs["weights"][1].animate.set_color(TEAL),
            refs["nodes"][i].animate.set_fill(GREEN2, 0.5),
            refs["nodes"][j].animate.set_fill(GREEN2, 0.5),
            run_time=1.2,
        )
        self.wait(1.5)

        # 镜头11：通式压轴
        general = MathTex(
            r"f[k][i][j]=\min\big(f[k-1][i][j],\, f[k-1][i][k]+f[k-1][k][j]\big)"
        ).scale(0.85)
        general.set_color_by_gradient(PINK, PURPLE)
        general.next_to(formula, DOWN, buff=0.4)
        self.play(Write(general), run_time=1.5)
        self.wait(2.5)
