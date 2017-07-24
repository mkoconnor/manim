from scene import Scene
from mobject.tex_mobject import *
from topics.geometry import *
from constants import *
from mobject import Mobject, Group
from eost.widgets import *
from animation.simple_animations import *
from animation.transform import *
import helpers
from eost.matching import get_matching, MatchingAnimations
import eost.deterministic

class FinitePowerSetScene(Scene):
    def construct(self):
        
        #self.skip_animations = True
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

        self.dither()
        self.play(ReplacementTransform(src0, dest0))
        self.dither()
        self.play(ReplacementTransform(src1, dest1))
        self.dither()
        self.play(ReplacementTransform(src2, dest2))
        self.dither()
        self.play(ReplacementTransform(src3, dest3))
        self.dither()
        self.play(ShowCreation(PX[1]))
        self.dither()

        arrow_P = Arrow(self.X.get_edge_center(RIGHT),
                        PX.get_edge_center(LEFT))

        desc_P = TextMobject("$\\mathcal P$owerset")
        desc_P[0].set_color(YELLOW)
        desc_P.next_to(arrow_P, UP)

        self.play(
            Write(desc_P[0]),
            ShowCreation(arrow_P),
        )
        self.play(Write(VGroup(*desc_P[1:])))

        desc_size_PX = TexMobject("|\\mathcal P(X)|=8=2^3")
        desc_size_PX.next_to(PX, UP)
        desc_size_PX.shift(2*LEFT)
        desc_PX = VGroup(*desc_size_PX[1:5])
        desc_PX[0].set_color(YELLOW)
        desc_PX[2].set_color(GREEN)

        self.play(
            ReplacementTransform(desc_P[0].copy(), desc_PX[0], path_arc = -np.pi/4),
            ReplacementTransform(desc_X.copy(), VGroup(*desc_PX[1:]), path_arc = -np.pi/3),
        )
        self.dither()
        self.play(FadeIn(VGroup(*[desc_size_PX[0]]+desc_size_PX[5:8])))
        self.dither()
        self.play(FadeIn(VGroup(*desc_size_PX[8:])))
        self.dither()

        #self.skip_animations = False

        arrows_possib = VGroup()
        descs_possib = VGroup()
        for i in range(3):
            arrow_possib = Arrow(ORIGIN, UP)
            arrow_possib.next_to(elements_X[i], DOWN)
            desc_possib = TexMobject("2")
            desc_possib.next_to(arrow_possib, DOWN)
            self.play(ShowCreation(arrow_possib))
            self.dither()
            self.play(FadeIn(desc_possib))
            self.dither()
            arrows_possib.add(arrow_possib)
            descs_possib.add(desc_possib)

        cdots = VGroup()
        for i in range(2):
            cdot = TexMobject("\\cdot")
            cdot.move_to((descs_possib[i].get_edge_center(RIGHT) + descs_possib[i+1].get_edge_center(LEFT))/2)
            cdots.add(cdot)

        self.play(FadeIn(cdots))
        self.dither(4)

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

        #self.skip_animations = True
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

        self.nodes_up = VGroup(*[
            Dot(self.get_upper_point(i)) for i in range(-self.node_bound, self.node_bound+1)
        ])
        self.nodes_up.set_color(self.color_down)
        self.nodes_down = VGroup(*[
            Dot(self.get_lower_point(i)) for i in range(-self.node_bound, self.node_bound+1)
        ])
        self.nodes_down.set_color(self.color_up)

        edges_up = VGroup()
        edges_down = VGroup()
        for component in components:
            component.up_matching_mobj = self.construct_up_matching(component)
            component.down_matching_mobj = self.construct_down_matching(component)
            component.up_nodes_mobj = self.get_component_up_nodes(component)
            component.down_nodes_mobj = self.get_component_down_nodes(component)
            edges_up.add(component.up_matching_mobj)
            edges_down.add(component.down_matching_mobj)

        missed_up = VGroup(*[component.up_nodes_mobj[0] for component in one_sided_up])
        missed_down = VGroup(*[component.down_nodes_mobj[0] for component in one_sided_down])

        desc_PX = TexMobject('\\mathcal P(\\omega)')
        desc_R = TexMobject('\\mathbb R')
        desc_PX.to_edge(RIGHT).next_to(self.nodes_down, DOWN, coor_mask = UP)
        desc_R.to_edge(RIGHT).next_to(self.nodes_up, UP, coor_mask = UP)
        self.add(desc_PX, desc_R)
        self.add_foreground_mobjects(self.nodes_up, self.nodes_down)

        self.play(ShowCreation(edges_down, submobject_mode = "all_at_once"))
        self.highlight(missed_down, DOWN)
        self.play(edges_down.highlight, self.dark_down)

        self.play(ShowCreation(edges_up, submobject_mode = "all_at_once"))
        self.highlight(missed_up, UP)
        self.play(edges_up.highlight, self.dark_up)

        self.dither()
        #self.skip_animations = False

        seq = one_sided_up[2]

        dot = seq.up_nodes_mobj[0]
        descs = ["5", "\{5\}", "0.000001"]
        index = 0
        while True:
            if len(descs) > 0:
                desc = TexMobject(descs[0])
                desc.next_to(dot, UP)
                descs = descs[1:]
                self.highlight(dot, UP, keep_colored = True)
                self.play(FadeIn(desc))
                self.dither()

            if index >= len(seq.down_matching_mobj): break
            connection = seq.down_matching_mobj[index].copy()
            connection.highlight(self.color_down)
            if index < len(seq.down_nodes_mobj):
                dot = seq.down_nodes_mobj[index]
            self.play(ShowCreation(connection),
                      dot.highlight, YELLOW)

            if len(descs) > 0:
                desc = TexMobject(descs[0])
                desc.next_to(dot, DOWN)
                descs = descs[1:]
                self.highlight(dot, DOWN, keep_colored = True)
                self.play(FadeIn(desc))
                self.dither()

            connection_ori = seq.up_matching_mobj[index]
            connection = DashedLine(*connection_ori.get_start_and_end())
            connection.highlight(self.color_up)
            if index+1 < len(seq.up_nodes_mobj):
                dot = seq.up_nodes_mobj[index+1]
            self.play(ShowCreation(connection),
                      dot.highlight, YELLOW)

            index += 1
            if index >= len(seq.down_matching_mobj): break
            

    def highlight(self, mobj, direction = ORIGIN, keep_colored = False):
        target0 = mobj.copy()
        target = mobj.copy()

        if keep_colored: target0.highlight(YELLOW)
        target.highlight(YELLOW)

        target.shift(0.2*direction)
        self.play(Transform(mobj, target,
                            run_time = 0.5*DEFAULT_ANIMATION_RUN_TIME,
        ))
        self.play(Transform(mobj, target0,
                            run_time = 0.5*DEFAULT_ANIMATION_RUN_TIME,
        ))
        
    def get_upper_point(self, index):
        return UP + index*0.5*RIGHT

    def get_lower_point(self, index):
        return DOWN + index*0.5*RIGHT

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
        return VGroup(*[self.nodes_up[a+self.node_bound]
                        for a,b in component.matching_down
                        if a >= -self.node_bound and a <= self.node_bound])

    def get_component_down_nodes(self, component):
        return VGroup(*[self.nodes_down[a+self.node_bound]
                        for a,b in component.matching_up
                        if a >= -self.node_bound and a <= self.node_bound])
