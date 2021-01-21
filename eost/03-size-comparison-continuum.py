from scene import Scene
from mobject.tex_mobject import *
from topics.geometry import *
from topics.fixed_size_dot import *
from topics.icons import *
from topics.number_line import NumberLine
from constants import *
from mobject import Mobject, Group
from animation.simple_animations import *
from animation.transform import *
import helpers
from eost.matching import get_matching, MatchingAnimations
import eost.deterministic
from topics.common_scenes import OpeningTitle, OpeningQuote

class Chapter3OpeningTitle(OpeningTitle):
    CONFIG = {
        "chapter_str" : "Chapter 3\\\\ Set Size Comparison, \\\ Continuum",
    }

class Chapter3OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "Some infinities are", "bigger", "than other infinities."
        ],
        "highlighted_quote_terms" : {
            "bigger" : GREEN,
        },
        "author" : "John Green"
    }

class SubsetsSeqs(Scene):

    def construct(self):
        #self.force_skipping()

        naturals = ('0', '1', '2')
        primes = ('2', '3', '5')
        integers = ('0', '-3', '3')
        fractions = ('\\textstyle\\frac 32', '\\textstyle-\\frac17', '11')
        triangles = []
        left_pos = 1*UP + 5*LEFT
        right_pos = 1*UP + 5*RIGHT

        aleph_0 = TexMobject("\\aleph_0")
        aleph_0.scale(1.5)
        aleph_0.to_edge(UP)
        self.play(Write(aleph_0))
        self.wait_to(4)

        for color, alpha, data in zip(color_gradient([GREEN, ORANGE], 4),
                                      np.linspace(0, 1, 4),
                                      [naturals, primes, integers, fractions]):

            triangle = VGroup(*[TexMobject(x) for x in data])
            triangle[0].shift(UP)
            triangle[1].shift(0.6*LEFT)
            triangle[2].shift(0.6*RIGHT)
            triangle.scale(1.2)
            triangle.set_color(color)
            triangle.move_to((1-alpha)*left_pos + alpha*right_pos)

            for mobj in triangle:
                self.play(FadeIn(mobj), run_time = 0.3)
            #self.dither()
            triangles.append(triangle)
        triangles = VGroup(*triangles)

        zero = TexMobject('0')
        one = TexMobject('1')
        seq_len = 30
        sequences = VGroup(*[
            VGroup(*[
                [zero, one][random.randint(0,1)].copy()
                for i in range(seq_len)
            ]).arrange_submobjects()
            for _ in range(3)
        ])
        for seq, color in zip(sequences, color_gradient([WHITE, DARK_GREY], 3)):
            seq.set_color(color)
        sequences.arrange_submobjects(DOWN)
        sequences.to_corner(LEFT+DOWN)
        sequences[1].shift(2*RIGHT)
        sequences[2].shift(RIGHT)

        self.wait_to(8)
        self.play(FadeOut(aleph_0))
        for seq in sequences:
            self.play(ShowCreation(seq))
        
        self.wait_to(15)
        self.play(FadeOut(triangles))

        seq = sequences[0]
        seq_data = [x.tex_string == '1' for x in seq]
        set_el = VGroup(*[TexMobject(str(i))
                          for i in range(len(seq_data))])
        set_el.arrange_submobjects(buff = 0.4)
        set_rect = SurroundingRectangle(set_el, color = GREEN, buff = MED_SMALL_BUFF)
        set_complet = VGroup(set_rect, set_el)
        set_complet.to_edge(LEFT)

        seq_dest = seq.copy()
        for digit, num, b in zip(seq_dest, set_el, seq_data):
            digit.move_to(num)
            if b: digit.set_color(GREEN)
            else: digit.set_color(DARK_GREY)

        seq_dest.shift(DOWN)
        set_complet.shift(UP)

        #self.revert_to_original_skipping_status()

        self.wait_to(18.5)
        self.play(Transform(seq, seq_dest),
                  FadeOut(VGroup(*sequences[1:])))
        self.wait_to(22.5)
        self.play(FadeIn(set_complet))

        seq_ones = []
        seq_zeros = []
        set_ones = []
        set_zeros = []
        for digit, num, b in zip(seq, set_el, seq_data):
            if b:
                seq_ones.append(digit)
                set_ones.append(num)
            else:
                seq_zeros.append(digit)
                set_zeros.append(num)
        seq_ones = VGroup(*seq_ones)
        seq_zeros = VGroup(*seq_zeros)
        set_ones = VGroup(*set_ones)
        set_zeros = VGroup(*set_zeros)

        ones_dest = seq_ones.copy()
        ones_dest.set_fill(GREEN, opacity = 0)
        ones_dest.shift(2*UP)

        omega_label = TexMobject("\\omega")
        omega_label.set_color(GREEN)
        omega_label.next_to(set_complet, UP)
        omega_label.to_edge(LEFT)

        self.wait_to(27.5)
        self.play(Write(omega_label))
        set_complet.add(omega_label)
        
        self.wait_to(34)
        self.play(set_ones.highlight, GREEN,
                  ReplacementTransform(seq_ones.copy(), ones_dest))
        self.remove(ones_dest)

        self.wait_to(38)
        self.play(set_zeros.highlight, BLACK)

        matching_line = Line(0.5*DOWN, 0.5*UP, color = RED, stroke_width = 0)
        seq_set = VGroup(seq, set_complet, matching_line)

        set_title = TexMobject("|\\hbox{Subsets of }\\omega|")
        seq_title = TexMobject("=|\\hbox{Binary sequences}|")

        both_titles = VGroup(set_title, seq_title)
        both_titles.arrange_submobjects(DOWN, buff = 1)
        both_titles.to_edge(UP)

        set_title_part = VGroup(*set_title[1:-1])
        seq_title_part = VGroup(*seq_title[2:-1])
        both_titles_part = VGroup(set_title_part, seq_title_part)

        self.wait_to(51)
        self.play(seq_set.to_corner, LEFT+DOWN,
                  FadeIn(both_titles_part))
        self.wait_to(53.5)
        matching_line.set_stroke(width = DEFAULT_POINT_THICKNESS)
        self.play(ShowCreation(matching_line))

        title_matching_center = set_title_part.get_edge_center(DOWN)
        title_matching_center[1] += seq_title_part.get_edge_center(UP)[1]
        title_matching_center[1] /= 2

        title_matching = VGroup(*[matching_line.copy() for _ in range(14)])
        title_matching.arrange_submobjects()
        title_matching.move_to(title_matching_center)
        title_matching_even = VGroup(*title_matching[1::2])
        title_matching_even.scale_in_place(-1)

        self.wait_to(58)
        self.play(ShowCreation(title_matching),
                  submobject_mode = "lagged_start",
                  run_time = 2*DEFAULT_ANIMATION_RUN_TIME)
        self.wait_to(64.5)
        both_titles_rest = VGroup(set_title[0], set_title[-1],
                                  seq_title[0], seq_title[1], seq_title[-1])
        self.play(FadeOut(title_matching),
                  Write(both_titles_rest))
        self.wait_to(60 + 27.5)

def make_inequalities():
    inequalities = VGroup(
        TexMobject("n","<","2^n"),
        TexMobject("1","<","2"),
        TexMobject("4","<","16"),
        TexMobject("10","<","1024"),
        TexMobject("\\vdots"),
        TexMobject("|\omega|","<","|\\mathcal P(\omega)|"),
        TexMobject("|X|","<","|\\mathcal P(X)|\,?"),
    )
    for ineq in inequalities:
        if len(ineq) > 1: ineq.shift(-ineq[1].get_center())
        else: ineq.center()

    for ineq in inequalities[-2:]:
        ineq[0][1].set_color(GREEN)
        ineq[2][3].set_color(GREEN)
        ineq[2][1].set_color(YELLOW)

    inequalities.arrange_submobjects(DOWN, coor_mask = UP)
    inequalities[0].shift(0.2*UP)
    inequalities.to_corner(UP+RIGHT)

    return inequalities

class FinitePowerSetScene(Scene):
    def construct(self):
        
        #self.force_skipping()
        elements_X = VGroup(*[
            TexMobject(str(n)) for n in range(3)
        ])
        elements_X.arrange_submobjects(RIGHT)

        self.X = VGroup(
            elements_X,
            SurroundingRectangle(elements_X, color = GREEN, buff = MED_SMALL_BUFF),
        )
        self.X.to_edge(LEFT)
        desc_X = TexMobject('X')
        desc_X.set_color(GREEN)
        desc_X.next_to(self.X, UP)

        self.add(self.X, desc_X)

        src0, dest0 = self.X_subsets([[]])
        src1, dest1 = self.X_subsets([[0],[1],[2]])
        src2, dest2 = self.X_subsets([[0,1],[1,2],[2,0]])
        src3, dest3 = self.X_subsets([[0,1,2]])
        elements_PX = VGroup(dest0, dest1, dest2, dest3)
        elements_PX.arrange_submobjects(LEFT)
        PX = VGroup(
            elements_PX,
            SurroundingRectangle(elements_PX, color = YELLOW, buff = MED_SMALL_BUFF)
        )
        PX.to_edge(RIGHT)

        self.wait_to(7.5)
        self.play(ReplacementTransform(src0, dest0))
        self.wait_to(8.7)
        self.play(ReplacementTransform(src1, dest1))
        self.wait_to(11.1)
        self.play(ReplacementTransform(src2, dest2))
        self.wait_to(13.3)
        self.play(ReplacementTransform(src3, dest3))
        self.wait_to(14.8)
        self.play(ShowCreation(PX[1]))

        arrow_P = Arrow(self.X.get_edge_center(RIGHT),
                        PX.get_edge_center(LEFT))

        desc_P = TextMobject("$\\mathcal P$owerset")
        desc_P[0].set_color(YELLOW)
        desc_P.next_to(arrow_P, UP)

        self.wait_to(18)
        self.play(
            Write(desc_P[0]),
            ShowCreation(arrow_P),
        )
        self.wait_to(21.5)
        self.play(Write(VGroup(*desc_P[1:])), run_time = 2)

        desc_size_PX = TexMobject("|\\mathcal P(X)|=8=2^3")
        desc_size_PX.next_to(PX, UP)
        desc_size_PX.shift(2*LEFT)
        desc_PX = VGroup(*desc_size_PX[1:5])
        desc_PX[0].set_color(YELLOW)
        desc_PX[2].set_color(GREEN)

        self.wait_to(23.7)
        self.play(
            ReplacementTransform(desc_P[0].copy(), desc_PX[0], path_arc = -np.pi/4),
            ReplacementTransform(desc_X.copy(), VGroup(*desc_PX[1:]), path_arc = -np.pi/3),
        )
        self.wait_to(29.7)
        self.play(FadeIn(VGroup(*[desc_size_PX[0]]+desc_size_PX[5:8])))
        self.wait_to(33.5)
        self.play(FadeIn(VGroup(*desc_size_PX[8:])))

        arrows_possib = VGroup()
        descs_possib = VGroup()
        for i in range(3):
            arrow_possib = Arrow(ORIGIN, UP)
            arrow_possib.next_to(elements_X[i], DOWN)
            desc_possib = TexMobject("2")
            desc_possib.next_to(arrow_possib, DOWN)

            if i == 0: self.wait_to(39)
            elif i == 1: self.wait_to(43.4)
            elif i == 2: self.wait_to(46.2)
            self.play(ShowCreation(arrow_possib))

            if i == 0: self.wait_to(42)
            self.play(FadeIn(desc_possib))

            arrows_possib.add(arrow_possib)
            descs_possib.add(desc_possib)

        cdots = VGroup()
        for i in range(2):
            cdot = TexMobject("\\cdot")
            cdot.move_to((descs_possib[i].get_edge_center(RIGHT) + descs_possib[i+1].get_edge_center(LEFT))/2)
            cdots.add(cdot)

        self.wait_to(48.5)
        self.play(FadeIn(cdots))
        desc_size_PX2 = TexMobject("2^3 = |\\mathcal P(X)|")
        desc_size_PX2[-3].set_color(GREEN)
        desc_size_PX2[-5].set_color(YELLOW)

        desc_size_PX2.shift(descs_possib.get_center() - desc_size_PX2[0].get_center() + DOWN)
        self.wait_to(52.2)
        self.play(ReplacementTransform(VGroup(descs_possib, cdots).copy(), VGroup(*desc_size_PX2[:2])))

        #self.revert_to_original_skipping_status()
        self.wait_to(54.5)
        self.play(*map(FadeOut, [PX, arrow_P, desc_P]))
        self.play(FadeOut(VGroup(*desc_size_PX[6:])),
                  FadeIn(desc_size_PX2[2]),
                  ReplacementTransform(VGroup(*desc_size_PX[:6]),
                                       VGroup(*desc_size_PX2[3:]))
                  )

        tmp_tex = TexMobject("1 \ldots n-1")
        tmp_tex.shift(elements_X[1].get_center() - tmp_tex[0].get_center())
        elements_X2 = elements_X.copy()
        elements_X2.remove(elements_X2[-1])
        elements_X2.add(*tmp_tex[1:])
        X2 = VGroup(
            elements_X2,
            SurroundingRectangle(elements_X2, color = GREEN, buff = MED_SMALL_BUFF),
        )
        arrow_shift = (elements_X2[-2].get_center() - elements_X[-1].get_center())*RIGHT
        cdots3 = VGroup(*tmp_tex[1:4]).copy()
        cdots3.move_to(cdots[1].get_center()+arrow_shift/2)

        tmp_tex = TexMobject("2^n")
        tmp_tex.shift(desc_size_PX2[0].get_center() - tmp_tex[0].get_center())
        general_exponent = tmp_tex[1]
        while len(elements_X) < len(elements_X2):
            elements_X.add(elements_X[-1].copy())
        self.play(
            ReplacementTransform(self.X, X2),
            VGroup(arrow_possib, desc_possib).shift, arrow_shift,
            Animation(arrows_possib),
            ReplacementTransform(cdots[1], cdots3),
            Transform(desc_size_PX2[1], general_exponent),
        )

        inequalities = make_inequalities()
        brace = Brace(VGroup(*inequalities[1:]), LEFT)
        brace_desc = TextMobject("All by Cantor's\\\\ diagonal argument")
        brace.put_at_tip(brace_desc)

        for i, ineq in enumerate(inequalities):
            if i == 0: self.wait_to(60 + 10.8)
            elif i == 1: self.wait_to(60 + 14.7)
            elif i == 2: self.wait_to(60 + 16)
            elif i == 3: self.wait_to(60 + 17.2)
            elif i == 5: self.wait_to(60 + 21)
            elif i == 6: self.wait_to(60 + 31)

            if i == 0 or i >= 5: self.play(Write(ineq))
            else: self.play(FadeIn(ineq))

        self.wait_to(60 + 37)
        self.play(
            GrowFromCenter(brace),
            FadeIn(brace_desc),
        )
        self.wait_to(60 + 50.5)

    def X_subsets(self, element_lists):
        source = VGroup(*[self.X_subset(elements) for elements in element_lists])
        dest = source.copy()
        dest.arrange_submobjects(DOWN)

        return source, dest
        
    def X_subset(self, elements):

        return VGroup(
            VGroup(*[self.X[0][el].copy() for el in elements]),
            self.X[1].copy(), # the same surrounding rectangle
        )

class CantorRevisited(Scene):
    def construct(self):
        self.inf_down = 7
        self.inf_right = 13
        column_el = VGroup(*[TexMobject(str(n)) for n in range(self.inf_down)])
        column_el.arrange_submobjects(DOWN, buff = 0.55)
        column_rect = SurroundingRectangle(column_el, color = GREEN, buff = MED_SMALL_BUFF)
        column_w = VGroup(column_rect, column_el)

        row_el = VGroup(*[TexMobject(str(n)) for n in range(self.inf_right)])
        row_el.arrange_submobjects(RIGHT, buff = 0.55)
        row_rect = SurroundingRectangle(row_el, color = GREEN, buff = SMALL_BUFF)
        row_w = VGroup(row_rect, row_el)

        missing_data = [True, False, False, True]
        missing_data += [random.randint(0,1) == 0 for x in range(4, self.inf_down)]
        missing = column_w.copy()
        missing[0].set_color(ORANGE)
        missing_desc = TexMobject("M")
        missing_desc.set_color(ORANGE)
        missing_desc.next_to(missing, UP)
        missing.add(missing_desc)

        missing[1].remove(*[missing.submobjects[1][i] for i in range(self.inf_down) if missing_data[i]])
        missing.to_corner(UP+LEFT)
        missing.shift(DOWN*MED_SMALL_BUFF)

        icon_shift = RIGHT
        column_w.shift(missing[0].get_center() - column_w[0].get_center() + 2*icon_shift)
        column_w_desc = TexMobject("\\omega")
        column_w_desc.set_color(GREEN)
        column_w_desc.next_to(column_w, UP)
        column_w.add(column_w_desc)

        icons = VGroup(*[
            (IconYes if missing_data[i] else IconNo)().scale(0.5).move_to(x)
            for i,x in enumerate(column_el)
        ])
        icons.shift(-icon_shift)

        rows = []
        connections = []
        for i,x in enumerate(column_el):
            for j,y in enumerate(row_el):
                if i == j: b = missing_data[i]
                else: b = random.randint(0,1) == 0
                if b: y.highlight(WHITE)
                else: y.highlight(BLACK)

            cur_row = row_w.copy()
            cur_row.shift(x.get_center() - cur_row[1][0].get_center())
            cur_row.shift(2*RIGHT)
            connection = Line(x.get_edge_center(RIGHT), cur_row.get_edge_center(LEFT), buff = 0.1)
            rows.append(cur_row)
            connections.append(connection)

        rows = VGroup(*rows)
        connections = VGroup(*connections)

        Pw_rect = SurroundingRectangle(rows, color = BLUE, buff = MED_SMALL_BUFF)
        Pw_desc = TexMobject("\\mathcal P(\\omega)")
        Pw_desc.set_color(BLUE)
        Pw_desc.next_to(Pw_rect, UP)

        self.draw_column(column_rect, Write(column_el))
        self.play(Write(column_w_desc))
        self.play(ShowCreation(Pw_rect), Write(Pw_desc))
        #self.wait_to(3)
        self.draw_rows(connections, rows)

        def highlight_diag(i):
            if missing_data[i]: color = YELLOW
            else: color = DARK_GREY

            x = rows[i][1][i]
            self.play(x.highlight, color,
                      x.scale_in_place, 1.5,
                      run_time = 0.5*DEFAULT_ANIMATION_RUN_TIME)
            self.play(x.scale_in_place, 1/1.5,
                      run_time = 0.5*DEFAULT_ANIMATION_RUN_TIME)
            self.play(ShowCreation(icons[i]), run_time = 0.5*DEFAULT_ANIMATION_RUN_TIME)

        self.wait_to(18)
        highlight_diag(0)
        self.wait_to(20.2)
        highlight_diag(3)

        self.wait_to(26)
        highlight_diag(1)
        self.wait_to(28.6)
        highlight_diag(2)

        animations = []
        for i,b in list(enumerate(missing_data))[4:]:
            animations.append(rows[i][1][i].highlight)
            if b: animations.append(YELLOW)
            else: animations.append(DARK_GREY)
            animations.append(FadeIn(icons[i]))

        self.wait_to(30.7)
        self.play(*animations)

        self.wait_to(33)
        self.draw_column(missing[0], ShowCreation(missing[1]))
        self.play(Write(missing_desc))

        def try_connect_M(i, end_time):
            point_r = column_el[i].get_edge_center(LEFT)
            point_l = missing.get_edge_center(RIGHT)
            point_l[1] = point_r[1]
            line = Line(point_r, point_l,
                        buff = 0.1,
                        color = ORANGE)

            icon = icons[i]
            icon_ori = icon.copy()
            icon_shifted = icon.copy()
            icon_shifted.next_to(line, UP, coor_mask = UP)

            self.play(
                Transform(icon, icon_shifted),
                ShowCreation(line),
            )
            self.wait_to(end_time-1)
            self.play(
                Transform(icon, icon_ori),
                Uncreate(line),
            )

        self.wait_to(38.1)
        try_connect_M(0, 46.5)
        try_connect_M(2, 55)

        M_in_Pw = Rectangle(height = 0.15, width = 5, color = ORANGE)
        M_in_Pw.shift((rows[3].get_center()+rows[4].get_center())/2 - M_in_Pw.get_edge_center(LEFT))

        self.play(GrowFromCenter(M_in_Pw))

        self.wait_to(60 + 16)
        self.play(*map(FadeOut, [Pw_rect, Pw_desc, rows, connections, M_in_Pw]))

        inequalities = make_inequalities()
        inequalities[-1][-1].remove(inequalities[-1][-1][-1])
        self.wait_to(60 + 25)
        self.play(Write(inequalities[-1]))
        self.wait_to(60 + 29)
        self.play(FadeIn(VGroup(*inequalities[:-1])))

        self.wait_to(60 + 49.5)

    def draw_column(self, rect, inner_animation):
        up_left, up_right, _, down_left, _ = rect.get_anchors()
        up = (up_left + up_right)/2
        left = [interpolate(up_left, down_left, alpha) for alpha in np.linspace(0,1,2*self.inf_right)]

        line_left = VMobject(color = rect.color,
                             stroke_width = rect.stroke_width)
        line_left.set_anchor_points([up]+left, mode="corners")
        line_right = line_left.copy()
        line_right.stretch_about_point(-1, 0, up)

        self.play(
            ShowCreation(line_left, run_time = inner_animation.run_time),
            ShowCreation(line_right, run_time = inner_animation.run_time),
            inner_animation,
        )
        self.remove(line_left, line_right)
        self.add(rect)

    def draw_rows(self, connections, rows):
        creating = []
        to_remove = []
        to_add = []

        for row, connection in zip(rows, connections):
            rect, numbers = row.submobjects
            up_left, up_right, _, down_left, _ = rect.get_anchors()
            left = (up_left + down_left)/2
            up = [interpolate(up_left, up_right, alpha) for alpha in np.linspace(0,1,2*self.inf_right)]

            line_up = VMobject(color = rect.color,
                               stroke_width = rect.stroke_width)
            line_up.set_anchor_points([left]+up, mode="corners")
            line_down = line_up.copy()
            line_down.stretch_about_point(-1, 1, left)

            to_remove += [line_up, line_down]
            creating.append(VGroup(connection, line_up, line_down, numbers))
            to_add.append(rect)

        self.play(
            ShowCreation(VGroup(*creating)),
            submobject_mode = "lagged_start",
            run_time = 2*DEFAULT_ANIMATION_RUN_TIME,
        )
        self.remove(*to_remove)
        self.add(*to_add)

class SubsetToReal(Scene):
    def construct(self):
        desc_R = TexMobject('\\mathfrak c=|\\mathbb R|')
        desc_R[-2].set_color(GREEN)
        desc_R.to_edge(RIGHT)
        numberline = NumberLine(unit_size = 3)
        numberline.shift(2*UP)
        desc_R.shift(2.6*UP)
        self.play(ShowCreation(numberline),
                  Write(desc_R[-2]))
        self.wait_to(10)
        self.play(Write(VGroup(*desc_R[:-2] + [desc_R[-1]])))

        seq_len = 30
        seq_data = [random.randint(0,1) for _ in range(seq_len)]
        set_el = VGroup(*[TexMobject(str(i))
                          for i in range(seq_len)])

        for x, b in zip(set_el, seq_data):
            x.set_color([BLACK, WHITE][b])

        set_el.arrange_submobjects(buff = 0.4)
        set_rect = SurroundingRectangle(set_el, color = RED, buff = MED_SMALL_BUFF)
        set_complet = VGroup(set_rect, set_el)
        set_complet.to_corner(LEFT+DOWN)

        self.wait_to(20)
        self.play(FadeIn(set_complet))

        zero = TexMobject('0').set_color(DARK_GREY)
        one = TexMobject('1').set_color(GREEN)
        seq = VGroup(*[[zero, one][b].copy() for b in seq_data])
        for (digit, num) in zip(seq, set_el):
            digit.move_to(num)

        seq.shift(2*UP)
        match_start = set_rect.get_edge_center(UP)
        match_end = seq.get_edge_center(DOWN)+0.1*DOWN
        match_start[0] = match_end[0] = 0
        match_line = Line(match_start, match_end, color = RED)
        self.wait_to(23)
        self.play(ReplacementTransform(set_el.copy(), seq), ShowCreation(match_line))

        num = seq_data[0]*.1 + seq_data[1]*.01 + seq_data[2]*.001 + seq_data[3]*.0001
        num_dot = Dot(numberline.number_to_point(num))

        zero_point = TexMobject("0.")
        zero_point.set_color(GREEN)
        num_seq = seq.copy()
        num_seq.highlight(GREEN)
        num_seq.arrange_submobjects(buff = 0.1)
        num_seq.next_to(num_dot, DOWN, aligned_edge = LEFT)

        match_line_dest = Line(match_start, num_seq.get_corner(LEFT+DOWN)+0.1*DOWN, color = RED)

        self.wait_to(27.5)
        self.play(ReplacementTransform(seq, num_seq),
                  Transform(match_line, match_line_dest))

        zero_point.next_to(num_seq, LEFT, buff = 0.1)
        self.wait_to(29.7)
        self.play(Write(zero_point), ShowCreation(num_dot))

        self.wait_to(33)
        nats_and_arrows = []
        for i,x in enumerate([-1.7, 1.2, num]):
            arrow_end = numberline.number_to_point(x)
            arrow = Arrow(arrow_end+UP, arrow_end)
            nat = TexMobject(str(i))
            nat.next_to(arrow, UP)
            nats_and_arrows += [arrow, nat]
            self.play(ShowCreation(arrow), FadeIn(nat))
            self.dither()

        nat_dest = nat.copy()
        nat_dest.next_to(match_end, UP)
        match_line_dest = Line(match_start, match_end, color = RED)
        self.wait_to(40)
        self.play(Transform(match_line, match_line_dest),
                  ReplacementTransform(nat.copy(), nat_dest, path_arc = np.pi/2))

        uncount = TexMobject("|\\mathbb R|\\geq", "|\\mathcal P(\\omega)| > \\aleph_0")
        uncount[0][1].set_color(GREEN)
        VGroup(*uncount[1][1:5]).set_color(RED)
        uncount.to_edge(RIGHT)
        self.wait_to(44)
        self.play(Write(uncount[1]))
        self.wait_to(47.3)
        self.play(Write(uncount[0]))

        strict_q = TexMobject("|\\mathbb R|>|\\mathcal P(\\omega)|?").to_edge(LEFT)
        strict_q[1].set_color(GREEN)
        VGroup(*strict_q[5:9]).set_color(RED)

        self.wait_to(52)
        self.play(Write(strict_q))
        self.play(*map(FadeOut, nats_and_arrows+[match_line, nat_dest]))

        brace = Brace(Line(*map(numberline.number_to_point, [0, 0.11111])), UP)
        #brace.shift(0.2*UP)
        self.play(GrowFromCenter(brace))
        simple_num_dot = Dot(numberline.number_to_point(-1.5))
        simple_num_desc = TexMobject("-1.5").next_to(simple_num_dot, DOWN)
        simple_num_desc.set_color(GREEN)

        self.wait_to(60 + 13.7)
        self.play(*(map(FadeOut, [set_complet, strict_q, zero_point, num_seq, uncount, brace]) +
                    [FadeIn(simple_num_desc), Transform(num_dot, simple_num_dot)]))
        self.wait_to(60 + 17)

class RealToSubset(Scene):
    def construct(self):
        numberline = NumberLine(unit_size = 3)
        numberline.shift(2*UP)
        desc_R = TexMobject('\\mathfrak c=|\\mathbb R|')
        desc_R[-2].set_color(GREEN)
        desc_R.to_edge(RIGHT)
        desc_R.shift(2.6*UP)
        num_dot = Dot(numberline.number_to_point(-1.5))
        num_desc = TexMobject("-1.5").next_to(num_dot, DOWN)
        num_desc.set_color(GREEN)

        self.add(numberline, desc_R, num_dot, num_desc)

        encoding = map(str, list(range(10))) + ['-', '.']
        encoding = VGroup(*[
            TextMobject("``$"+c+"$''","$\\to$", str(i))
            for i,c in enumerate(encoding)
            ])
        for rule in encoding:
            rule.shift(encoding[0][1].get_center()-rule[1].get_center())

        encoding.arrange_submobjects(DOWN, coor_mask = UP)
        enc_part2 = VGroup(*encoding[6:])
        enc_part2.shift(encoding[0][1].get_center()
                        -enc_part2[0][1].get_center()
                        + 3*RIGHT)
        encoding.to_corner(LEFT+DOWN)

        #self.add(encoding)
        representation_data = [10, 1, 11, 5]
        representation = VGroup(*[encoding[i][0].copy() for i in representation_data])
        representation.arrange_submobjects(buff = 1)
        representation.to_corner(UP+LEFT)
        repr_body = VGroup(*[repr[1] for repr in representation])
        repr_quotes = VGroup(*[VGroup(repr[0],repr[2]) for repr in representation])

        self.wait_to(5)
        self.play(ReplacementTransform(num_desc.copy(), repr_body),
                  FadeIn(repr_quotes))

        self.wait_to(8)
        self.play(ShowCreation(VGroup(*[enc[0] for enc in encoding])))

        self.wait_to(14.5)
        self.play(ShowCreation(VGroup(*[VGroup(enc[1], enc[2]) for enc in encoding])))

        repr_num = VGroup(*[encoding[i][2].copy() for i in representation_data])
        for num, char in zip(repr_num, repr_body):
            center = char.get_center()
            center[1] = repr_body[0].get_center()[1]
            num.move_to(center)

        self.play(FadeOut(repr_quotes),
                  ReplacementTransform(repr_body, repr_num))

        self.wait_to(19)
        repr_rect = SurroundingRectangle(repr_num, color = RED, buff = MED_SMALL_BUFF)
        self.play(ShowCreation(repr_rect))

        self.wait_to(22)
        for _ in range(2):
            self.play(Swap(repr_num[1], repr_num[3]), Swap(num_desc[1], num_desc[3]))
            if i == 0: self.wait_to(27)

        info = []
        for i in range(1,4):
            cur_info = self.index_info(repr_num[i], 100*i+representation_data[i])

            if i == 1: self.wait_to(39)
            elif i == 2: self.wait_to(43)
            elif i == 3: self.wait_to(46.5)
            self.play(FadeIn(cur_info))
            info.append(cur_info)

        info = VGroup(*info)

        self.wait_to(51)
        self.play(*map(FadeOut, [repr_num, numberline, desc_R, info, repr_rect, num_dot, num_desc]))

        pi_str = "3.14159265358979323846265338327950288"
        pi_str_mobj = TexMobject(pi_str)
        pi_str_mobj.set_color(GREEN)
        pi_str_mobj.shift(1.5*UP+2*RIGHT)
        pi_str_mobj = VGroup(*[VGroup(c) for c in pi_str_mobj])
        self.play(FadeIn(pi_str_mobj))

        pi_num_list = [3, 111] + [200+100*i+int(c) for i,c in enumerate(pi_str[2:])]
        pi_num_list_mobj = VGroup(*[TexMobject(str(num)) for num in pi_num_list])
        pi_num_list_mobj.arrange_submobjects(buff = 0.25)
        pi_rect = SurroundingRectangle(pi_num_list_mobj, color = RED, buff = MED_SMALL_BUFF)
        VGroup(pi_num_list_mobj, pi_rect).to_corner(LEFT+UP)

        self.wait_to(56)
        self.play(FadeIn(pi_rect),
                  ReplacementTransform(pi_str_mobj.copy(), pi_num_list_mobj))
        match_start = pi_str_mobj.get_edge_center(UP)+0.1*UP
        match_end = pi_rect.get_edge_center(DOWN)
        match_start[0] = match_end[0] = 0
        match_line = Line(match_start, match_end, color = GREEN)

        self.wait_to(59)
        self.play(ShowCreation(match_line))

        question = TexMobject("|", "\\mathbb R", "| = |", "\\mathcal P(\\omega)", "|?")
        question[1].highlight(GREEN)
        question[-2].highlight(RED)
        note = TextMobject("Just a shortcut for\\\\a perfect matching")

        q_point = encoding.get_corner(UP+RIGHT)
        q_point[0] = (q_point[0] + SPACE_WIDTH)/2
        question.shift(q_point - question.get_edge_center(UP))

        self.wait_to(60 + 18.5)
        self.play(Write(question))

        arrow = Arrow(ORIGIN, UP)
        arrow.next_to(question[2][1], DOWN)
        note.next_to(arrow, DOWN)

        self.wait_to(60 + 32)
        self.play(ShowCreation(arrow), FadeIn(note))

        self.wait_to(60 + 59)

    def index_info(self, mobj, value):
        result = TexMobject(str(value))
        result.shift(mobj[-1].get_center() - result[-1].get_center())
        result = VMobject(*result[:-len(mobj)])
        return result

class DoubleMatching():
    def __init__(self):
        self.matching_up = list()
        self.matching_down = list()
        self.finished = False

class MatchingCycle(DoubleMatching):
    def __init__(self, max_len = 4, min_jump = 3, max_jump = 12):
        DoubleMatching.__init__(self)
        self.max_len = max_len
        self.min_jump = min_jump
        self.max_jump = max_jump

    def add_one(self, src):
        if self.finished: return
        if len(self.matching_down) == 0:
            x,y = random.choice(sorted(src.items())[:len(src)/2])
            self.first_x = x;
        else:
            possibilities = [(x,y) for (x,y) in src.items()
                             if x+y - self.last_sum >= self.min_jump and x+y - self.last_sum <= self.max_jump]
            if len(possibilities) == 0:
                self.finish()
                return

            x,y = random.choice(possibilities)
            self.matching_up.append((self.last_y, x))

        del src[x]
        self.matching_down.append((x, y))
        self.last_y = y
        self.last_sum = x+y

        if len(self.matching_down) >= self.max_len: self.finish()

    def finish(self):
        self.matching_up.append((self.last_y, self.first_x))
        self.finished = True

class MatchingOneSided(DoubleMatching):
    def __init__(self, start_down = False, start_right = False, final_jump = 14, max_nice_jump = 4):
        DoubleMatching.__init__(self)
        self.start_down = start_down
        self.start_right = start_right
        self.final_jump = final_jump
        self.max_nice_jump = max_nice_jump

    def add_one(self, src):
        if self.finished: return
        normed = [self.real_to_normed(pair) for pair in src.items()]
        normed = filter(lambda (x,y): x <= y, normed)
        normed.sort()

        if len(self.matching_down) == 0:
            x,y = random.choice(filter(lambda (x,y): x < 0 and x > -14, normed))
        else:
            normed = filter(lambda (x,y): x >= self.last_y, normed)
            if len(normed) == 0:
                self.finish()
                return
            if normed[0][0] - self.last_y > self.max_nice_jump:
                x,y = normed[0]
            else:
                x,y = random.choice(filter(lambda (x,y): x - self.last_y <= self.max_nice_jump, normed))

            self.matching_up.append((self.last_y, x))

        self.matching_down.append((x, y))
        self.last_y = y

        real_x, real_y = self.normed_to_real((x,y))
        del src[real_x]

    def finish(self):
        self.matching_up.append((self.last_y, self.last_y+self.final_jump))
        if self.start_down: self.matching_up, self.matching_down = self.matching_down, self.matching_up
        if self.start_right:
            self.matching_up = [(-x,-y) for (x,y) in self.matching_up]
            self.matching_down = [(-x,-y) for (x,y) in self.matching_down]
        self.finished = True

    def real_to_normed(self, (x,y)):
        if self.start_down: x,y = y,x
        if self.start_right: x,y = -x,-y
        return x,y
    def normed_to_real(self, (x,y)):
        return self.real_to_normed((x,y))

class MatchingBothSided(DoubleMatching):
    def __init__(self, final_jump = 14):
        DoubleMatching.__init__(self)
        self.final_jump = final_jump

    def add_one(self, src):
        if self.finished: return
        if len(src) == 0:
            self.finish()
            return
        x,y = min(src.items())
        del src[x]
        if len(self.matching_down) == 0:
            self.last_y = x - self.final_jump
        self.matching_up.append((self.last_y, x))
        self.matching_down.append((x, y))
        self.last_y = y

    def finish(self):
        self.matching_up.append((self.last_y, self.last_y + self.final_jump))
        self.finished = True

class FinalMatching(DoubleMatching):
    def __init__(self, node_bound, max_step = 3):
        DoubleMatching.__init__(self)
        remaining_up = list(range(-node_bound, node_bound+1))
        remaining_down = list(range(-node_bound, node_bound+1))

        for _ in range(-node_bound, node_bound+1):
            if remaining_down[0] < remaining_up[0]:
                remaining_up, remaining_down = remaining_down, remaining_up
                self.matching_up, self.matching_down = self.matching_down, self.matching_up
            x = remaining_up[0]
            y = random.choice([y for y in remaining_down if y-x <= max_step])
            self.matching_down.append((x, y))
            self.matching_up.append((y, x))
            remaining_up.remove(x)
            remaining_down.remove(y)

        self.dict_up = dict(self.matching_up)
        self.dict_down = dict(self.matching_down)

class CantorBernsteinScene(Scene):

    def construct(self):

        #self.force_skipping()

        self.side_scale = 0.4
        self.node_bound = 14
        self.color_up = RED
        self.color_down = GREEN
        self.dark_up = "#551111"
        self.dark_down = "#115511"

        self.final_data = FinalMatching(self.node_bound)
        self.final_matching = self.construct_down_matching(self.final_data, color = YELLOW)

        matching_src = self.final_data.dict_down.copy()
        components = [
            MatchingCycle(),
            MatchingOneSided(start_down = False),
            MatchingOneSided(start_down = True),
            MatchingOneSided(start_down = False),
            MatchingOneSided(start_down = True),
            MatchingOneSided(start_down = False),
            MatchingBothSided(),
            MatchingBothSided(),
        ]
        cycles = filter(lambda x: isinstance(x, MatchingCycle), components)
        one_sided = filter(lambda x: isinstance(x, MatchingOneSided), components)
        both_sided = filter(lambda x: isinstance(x, MatchingBothSided), components)
        one_sided_up = filter(lambda x: x.start_down == False, one_sided)
        one_sided_down = filter(lambda x: x.start_down == True, one_sided)

        for component in components:
            component.last_y = -20

        unfinished = list(components)
        while len(unfinished) > 0:
            first_comp = min(unfinished, key = lambda c: c.last_y)
            first_comp.add_one(matching_src)
            if first_comp.finished: unfinished.remove(first_comp)

        self.nodes_up = VGroupPS(*[
            FixedSizeDot(self.get_upper_point(i), radius = 0.05)
            for i in range(-self.node_bound, self.node_bound+1)
        ])
        self.nodes_up.set_color(self.color_down)
        self.nodes_down = VGroupPS(*[
            FixedSizeDot(self.get_lower_point(i), radius = 0.05)
            for i in range(-self.node_bound, self.node_bound+1)
        ])
        self.nodes_down.set_color(self.color_up)

        edges_up = VGroup()
        edges_down = VGroup()
        for component in components:
            component.down_matching_mobj = self.construct_down_matching(component)
            component.up_matching_mobj = self.construct_up_matching(component)
            component.down_nodes_mobj = self.get_component_down_nodes(component)
            component.up_nodes_mobj = self.get_component_up_nodes(component)
            component.mobj = VGroupPS(component.down_matching_mobj,
                                    component.up_matching_mobj,
                                    component.down_nodes_mobj,
                                    component.up_nodes_mobj)
            edges_up.add(component.up_matching_mobj)
            edges_down.add(component.down_matching_mobj)

        missed_up = VGroupPS(*[component.up_nodes_mobj[0] for component in one_sided_up])
        missed_down = VGroupPS(*[component.down_nodes_mobj[0] for component in one_sided_down])

        desc_PX = TexMobject('\\mathcal P(\\omega)')
        desc_PX.set_color(RED)
        desc_R = TexMobject('\\mathbb R')
        desc_R.set_color(GREEN)
        desc_PX.to_edge(RIGHT).next_to(self.nodes_down, DOWN, coor_mask = UP)
        desc_R.to_edge(RIGHT).next_to(self.nodes_up, UP, coor_mask = UP)
        self.add(desc_PX, desc_R)
        self.add_foreground_mobjects(self.nodes_up, self.nodes_down)

        self.play(ShowCreation(edges_down, submobject_mode = "all_at_once"))
        self.wait_to(3)
        self.highlight_point(missed_down, DOWN)
        self.wait_to(4.8)
        self.play(edges_down.highlight, self.dark_down)

        self.play(ShowCreation(edges_up, submobject_mode = "all_at_once"))
        self.wait_to(9)
        self.highlight_point(missed_up, UP)
        self.play(edges_up.highlight, self.dark_up)

        self.play(self.nodes_up.highlight, self.dark_down,
                  self.nodes_down.highlight, self.dark_up)

        comp_rearranged = one_sided_down+cycles+both_sided+one_sided_up
        for i, comp in enumerate(comp_rearranged):
            comp.comp_index = i

        seq = one_sided_up[-1]
        descs_group = self.gradually_connect(
            seq, descs=("5", "\{5\}", "0.000001"),
            waits = (24.5, 32, 34.5, 39, 45, 49, 56)
        )
        self.wait_to(60 + 8.5)
        self.play(FadeOut(descs_group))
        self.play(self.to_side(seq))

        seq = one_sided_down[0]
        self.gradually_connect(one_sided_down[0], waits = (60 + 28,))
        self.play(self.to_side(seq))

        self.wait_to(60 + 34)
        self.play(*map(FadeOut, [desc_R, desc_PX]))

        for seq in [one_sided_up[1], one_sided_down[1], one_sided_up[0]]:
            self.simultaneously_connect(seq)
            self.dither()
            self.play(self.to_side(seq))

        self.wait_to(2*60 + 4-8)
        self.gradually_connect(cycles[0])
        self.play(self.to_side(cycles[0]))
        self.play(*map(self.to_side, both_sided))

        for seq in both_sided:
            self.simultaneously_connect(seq)

        self.wait_to(2*60 + 20)
        self.play(*(self.unhighlight_seqs(one_sided_down+both_sided+cycles)))
        self.wait_to(2*60 + 23)
        self.play(*(self.unhighlight_seqs(one_sided_up) +
                    self.highlight_seqs(one_sided_down)))
        self.wait_to(2*60 + 26.5)
        self.play(*(self.unhighlight_seqs(one_sided_down) +
                    self.highlight_seqs(both_sided+cycles)))

        self.wait_to(2*60 + 31.5)
        self.play(*(self.unhighlight_seqs(both_sided+cycles) +
                    self.highlight_seqs(one_sided_up)))
        self.remove_matching(one_sided_up)

        self.wait_to(2*60 + 34)
        self.play(*(self.unhighlight_seqs(one_sided_up) +
                    self.highlight_seqs(one_sided_down)))
        self.remove_matching(one_sided_down)

        self.wait_to(2*60 + 36.5)
        self.play(*(self.unhighlight_seqs(one_sided_up) +
                    self.highlight_seqs(both_sided+cycles)))
        self.wait_to(2*60 + 38)
        self.remove_matching(both_sided+cycles)

        self.wait_to(2*60 + 40)
        self.play(*self.highlight_seqs(one_sided))
        to_center_anim = []
        for seq in components:
            to_center_anim.append(self.to_center(seq))
        self.play(*to_center_anim)

        self.wait_to(2*60 + 50.5)
        title = TextMobject("Cantor-Bernstein Theorem")
        title.scale(1.3)
        title.to_edge(UP)
        self.play(Write(title))
        
        self.wait_to(3*60 + 5.5)

        #self.revert_to_original_skipping_status()

    def gradually_connect(self, seq, descs = (), waits = ()):

        self.remove(seq.mobj)
        self.add(seq.mobj)

        wait_index = 0

        forward = True
        dir = UP
        colorA = self.color_down
        colorB = self.color_up
        nodesA = seq.down_nodes_mobj
        nodesB = seq.up_nodes_mobj
        matchingA = seq.down_matching_mobj.submobjects
        matchingB = seq.up_matching_mobj.submobjects

        both_sided = isinstance(seq, MatchingBothSided)
        if (isinstance(seq, MatchingOneSided) and seq.start_down) or both_sided:
            dir = -dir
            colorA, colorB = colorB, colorA
            nodesA, nodesB = nodesB, nodesA
            matchingA, matchingB = matchingB, matchingA

        descs_group = VGroup()
        index = 0

        if not both_sided:
            dot = nodesB[0]
            if len(waits) > 0: self.wait_to(waits[0]-1)
            self.highlight_point(dot, dir, keep_colored = True, color = colorA)

        else: forward = False

        while index < len(matchingA):
            if len(descs) > 0 and dot is not None:
                desc = TexMobject(descs[0])
                descs_group.add(desc)
                desc.next_to(dot, dir)
                descs = descs[1:]
                if wait_index < len(waits):
                    self.wait_to(waits[wait_index])
                    wait_index += 1
                self.play(FadeIn(desc))

            connection_ori = matchingA[index]
            if forward: connection = connection_ori.copy()
            else: connection = DashedLine(*connection_ori.get_start_and_end())
            connection.highlight(colorA)

            if forward or both_sided: dot_index = index
            else: dot_index = index+1
            
            if dot_index < len(nodesA): dot = nodesA[dot_index]
            else: dot = None

            animations = [ShowCreation(connection)]
            if not forward: animations.append(FadeOut(connection_ori))
            if dot is not None: animations += [dot.highlight, colorB]

            if wait_index < len(waits):
                self.wait_to(waits[wait_index])
                wait_index += 1
            self.play(*animations)

            self.remove(connection_ori)
            matchingA[index] = connection

            dir = -dir
            colorA, colorB = colorB, colorA
            nodesA, nodesB = nodesB, nodesA
            matchingA, matchingB = matchingB, matchingA
            forward = not forward

            if both_sided:
                if not forward: index += 1
            else:
                if forward: index += 1

        return descs_group

    def simultaneously_connect(self, seq):

        nodes = VGroup(seq.up_nodes_mobj, seq.down_nodes_mobj)

        colorA = self.color_down
        colorB = self.color_up
        matchingA = seq.down_matching_mobj
        matchingB = seq.up_matching_mobj
        if isinstance(seq, MatchingOneSided) and seq.start_down:
            colorA, colorB = colorB, colorA
            matchingA, matchingB = matchingB, matchingA

        dashed_matching = VGroup(*[
            DashedLine(*connection.get_start_and_end())
            for connection in matchingB
        ])
        dashed_matching.highlight(colorB)
        self.play(FadeOut(matchingB),
                  matchingA.highlight, colorA,
                  FadeIn(dashed_matching),
                  seq.up_nodes_mobj.highlight, self.color_down,
                  seq.down_nodes_mobj.highlight, self.color_up)
        for i, connection in enumerate(dashed_matching):
            matchingB.submobjects[i] = connection

    
    def to_side(self, seq):
        dest = seq.mobj.copy()
        dest.stretch(self.side_scale, 1)
        dest.shift(DOWN*(seq.comp_index - 3.5))
        return Transform(seq.mobj, dest)

    def to_center(self, seq):
        dest = seq.mobj.copy()
        dest.shift(UP*(seq.comp_index - 3.5))
        dest.stretch(1/self.side_scale, 1)
        return Transform(seq.mobj, dest)

    def remove_matching(self, seq_list):
        removed = []
        for seq in seq_list:
            if isinstance(seq, MatchingOneSided) and seq.start_down:
                removed.append(seq.down_matching_mobj)
            else:
                removed.append(seq.up_matching_mobj)
        removed = VGroup(*removed)
            
        self.play(FadeOut(removed))
        removed.set_stroke(width = 0)

    def highlight_seqs(self, seq_list):
        result = []
        for seq in seq_list:
            result += [
                seq.up_nodes_mobj.highlight, self.color_down,
                seq.down_nodes_mobj.highlight, self.color_up,
                seq.up_matching_mobj.highlight, self.color_up,
                seq.down_matching_mobj.highlight, self.color_down,
            ]
        return result

    def unhighlight_seqs(self, seq_list):
        result = []
        for seq in seq_list:
            result += [
                seq.up_nodes_mobj.highlight, self.dark_down,
                seq.down_nodes_mobj.highlight, self.dark_up,
                seq.up_matching_mobj.highlight, self.dark_up,
                seq.down_matching_mobj.highlight, self.dark_down,
            ]
        return result

    def highlight_point(self, mobj, direction = ORIGIN, keep_colored = False, color = YELLOW):
        target0 = mobj.copy()
        target = mobj.copy()

        if keep_colored: target0.highlight(color)
        target.highlight(color)

        target.shift(0.2*direction)
        self.play(Transform(mobj, target,
                            run_time = 0.5*DEFAULT_ANIMATION_RUN_TIME,
        ))
        self.play(Transform(mobj, target0,
                            run_time = 0.5*DEFAULT_ANIMATION_RUN_TIME,
        ))
        
    def get_upper_point(self, index):
        return 0.9*UP + index*0.48*RIGHT

    def get_lower_point(self, index):
        return 0.9*DOWN + index*0.48*RIGHT

    def construct_down_matching(self, matching_data, color = None):
        if color is None: color = self.color_down
        return VGroup(*[
            Line(self.get_upper_point(x), self.get_lower_point(y), color = color)
            for x,y in matching_data.matching_down
        ])

    def construct_up_matching(self, matching_data, color = None):
        if color is None: color = self.color_up
        return VGroup(*[
            Line(self.get_lower_point(x), self.get_upper_point(y), color = color)
            for x,y in matching_data.matching_up
        ])

    def get_component_up_nodes(self, component):
        return VGroupPS(*[self.nodes_up[a+self.node_bound]
                        for a,b in component.matching_down
                        if a >= -self.node_bound and a <= self.node_bound])

    def get_component_down_nodes(self, component):
        return VGroupPS(*[self.nodes_down[a+self.node_bound]
                        for a,b in component.matching_up
                        if a >= -self.node_bound and a <= self.node_bound])

class RemainingQuestions(Scene):
    def construct(self):
        comparable = TextMobject("Are every two sets comparable?")
        continuum = TextMobject("Is continuum the smallest uncountable size?")
        questions = VGroup(comparable, continuum)
        questions.arrange_submobjects(DOWN, aligned_edge = LEFT, buff = 1)
        self.play(Write(comparable))
        self.wait_to(10.5)
        self.play(Write(continuum))
        icon_yes = IconYes().next_to(comparable, buff = 0.5)

        self.wait_to(22.5)
        self.play(ShowCreation(icon_yes))

        continuum_ans = TextMobject("Forever open...")
        continuum_ans.set_color(YELLOW)
        continuum_ans.next_to(continuum, DOWN, buff = 0.5)
        self.wait_to(35.5)
        self.play(Write(continuum_ans))

        stamp_text = TextMobject("Proven")
        stamp_rect = SurroundingRectangle(stamp_text, buff = 0.2)
        stamp_bg = BackgroundRectangle(stamp_rect)
        stamp = VGroup(stamp_bg, stamp_rect, stamp_text)
        stamp.set_color(RED)
        stamp.rotate(np.pi/6)
        stamp.next_to(continuum_ans)
        stamp.shift(1.3*LEFT + 0.25*DOWN)

        self.wait_to(53)
        self.play(FadeInZoomOut(stamp, about_point = stamp.get_center()))

        self.wait_to(60+4)
