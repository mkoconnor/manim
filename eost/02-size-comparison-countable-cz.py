#!/usr/bin/env python
# coding: utf-8

from scene import Scene
from mobject.tex_mobject import *
from topics.geometry import *
from constants import *
from mobject import Mobject, Group
from topics.fruit import *
from topics.objects import BraceDesc, BraceText
from animation.simple_animations import *
from animation.transform import *
import helpers
from eost.matching import get_matching, MatchingAnimations
from eost.ordinal import *
from topics.chat_bubbles import Conversation
import eost.deterministic
from topics.common_scenes import OpeningTitle, OpeningQuote

class Chapter2OpeningTitle(OpeningTitle):
    CONFIG = {
        "series_str" : "Esence teorie množin",
        "chapter_str" : "Kapitola 2\\\\ Porovnávání množin, spočetno",
    }

class Chapter2OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "Nekonečno!","Žádná jiná myšlenka nezapůsobila tak významně na mysl člověka; žádná jiná myšlenka tolik nepovzbudila jeho intelekt; přesto žádný jiný koncept nepotřebuje více","objasnit..."
        ],
        "highlighted_quote_terms" : {
            "Nekonečno!" : YELLOW,
            "objasnit..." : GREEN,
        },
        "author" : "David Hilbert",        
    }
def permute(l):
    ret = l[:]
    random.shuffle(ret)
    return ret

def permute_animations(mobj,move):
    mobjs = mobj.submobjects
    permuted_indices = np.random.permutation(len(mobjs))
    def path_along_arc(old_index,new_index):
        if ( (old_index < new_index and move == "down")
             or (new_index < old_index and move == "up")
             ):
            return helpers.path_along_arc(np.pi/4)
        else:
            return helpers.path_along_arc(-np.pi/4)
    return [
        Transform(mobjs[i],mobjs[i].copy().replace(mobjs[j]),
                  path_func=path_along_arc(i,j)
        )
        for (i,j) in enumerate(permuted_indices)
    ]

class GrowFromCenterGeneral(Transform):
    def __init__(self, mobject, **kwargs):
        target = mobject.copy()
        mobject.scale_in_place(0)
        Transform.__init__(self, mobject, target, **kwargs)

def random_small_angle():
    return random.uniform(-np.pi/40,np.pi/40)

def apple_pile():
    bottom_row = [Apple(i).rotate(random_small_angle()) for i in xrange(3)]
    top_row = [Apple(3).rotate(-np.pi/20),Apple(4).rotate(np.pi/20)]
    VGroup(*bottom_row).arrange_submobjects(buff=0.1)
    VGroup(*top_row).arrange_submobjects(buff=0.1)
    VGroup(*top_row).next_to(VGroup(*bottom_row),direction=UP,buff=0)
    return VGroup(*(bottom_row + top_row))

def pear_pile():
    bottom_two = [Pear(i).rotate(random_small_angle()) for i in xrange(2)]
    VGroup(*bottom_two).arrange_submobjects(buff=0.1)
    third_on_bottom = Pear(2).next_to(VGroup(*bottom_two),buff=0.1)
    top = (Pear(3)).rotate(-np.pi/20).next_to(VGroup(*bottom_two),direction=UP,buff=0)
    return VGroup(*(bottom_two + [third_on_bottom, top]))

class CountTransform():
    CONFIG = {
        'rate_func' : None
    }

    def __init__(self, mobject, target, direction):
        numbers=[]
        def transform(mobj,tgt,i):
            number = TextMobject(str(i+1)).next_to(tgt,direction=direction)
            numbers.append(number)
            return AnimationGroup(
                Write(number),
                Transform(mobj,tgt),
            )
        transforms = [
            transform(mobj,tgt,i)
            for (i,(mobj,tgt))
            in enumerate(zip(mobject.submobjects,target.submobjects))
        ]
        self.numbers = numbers
        self.transforms = transforms

    def play(self,scene, run_time):
        run_time = float(run_time) / len(self.transforms)
        for transform in self.transforms:
            scene.play(transform, run_time = run_time)

    def summarize(self):
        central_number = self.numbers[-1].copy()
        central_number.shift(
            VGroup(*self.numbers).get_center()
            - central_number.get_center()
        )
        return AnimationGroup(*(
            [FadeOut(i) for i in self.numbers[:-1]]
            + [Transform(self.numbers[-1],central_number)]
        ))

class FiniteFruitScene(Scene):
    def construct(self):

        apples = apple_pile().center()
        pears = pear_pile().center().next_to(apples,direction=DOWN)
        VGroup(apples,pears).center()
        # Display the two lines of apples and pears
        self.play(Succession(*map(GrowFromCenterGeneral, apples.submobjects), rate_func=None, run_time = 1.5*DEFAULT_ANIMATION_RUN_TIME))
        self.play(Succession(*map(GrowFromCenterGeneral, pears.submobjects), rate_func=None, run_time = 1.5*DEFAULT_ANIMATION_RUN_TIME))
        counted_apples = [Apple(i) for i in xrange(5)]
        counted_pears = [Pear(i) for i in xrange(4)]
        counted_apple_group = VGroup(*counted_apples).arrange_submobjects().to_edge(UP)
        counted_pear_group = VGroup(*counted_pears).arrange_submobjects().to_edge(DOWN)
        apple_count = CountTransform(apples,counted_apple_group,direction=DOWN)
        self.wait_to(14.3)
        apple_count.play(self, run_time = 3.25)
        pear_count = CountTransform(pears,counted_pear_group,direction=UP)
        self.wait_to(20.1)
        pear_count.play(self, run_time = 2.6)
        self.wait_to(24)
        self.play(apple_count.summarize(),pear_count.summarize())
        inequality = TexMobject(
            apple_count.numbers[-1].args[0],
            ">",
            pear_count.numbers[-1].args[0]
        ).center()
        self.play(
            Transform(
                apple_count.numbers[-1],
                inequality.get_part_by_tex(apple_count.numbers[-1].args[0])
            ),
            Write(inequality.get_part_by_tex(">")),
            Transform(
                pear_count.numbers[-1],
                inequality.get_part_by_tex(pear_count.numbers[-1].args[0])
            )
        )

        self.wait_to(33.5)
        self.play(*map(FadeOut,[
            apple_count.numbers[-1],
            inequality,
            pear_count.numbers[-1]
        ]))
        # Show a matching
        matching = MatchingAnimations(VGroup(*apples),VGroup(*pears))
        self.wait_to(40.5)
        for anims in matching.match_animations:
            self.play(anims)
        self.wait_to(46.3)
        self.play(Transform(apples[-1],apples[-1].copy().center().to_edge(UP)))
        self.play(FocusOn2(apples[-1], highlight_color = WHITE))

        buff = matching.buff
        matching = matching.matching

        self.wait_to(51.5)
        for i in range(2):
            apples.submobjects.sort(key = lambda apple: apple.get_center()[0])
            apples_target = apples.copy()
            apples_target.arrange_submobjects(center = False, buff = buff)
            apples_target.shift(LEFT*apples_target.get_center()[0])
            self.play(Uncreate(matching)) # 52.5, 62.5
            self.play(Transform(apples, apples_target)) # 53.5, 63.5
            if i == 0: self.wait_to(55.5)
            # Permute them
            apple_permutations=permute_animations(apples,move="up")
            pear_permutations=permute_animations(pears,move="down")

            if i == 0: run_time = 1
            else: run_time = 0.5

            self.play(*(apple_permutations + pear_permutations), run_time = run_time) # 64
            # Show a different matching
            permuted_apples = permute(apples)
            permuted_pears = permute(pears)
            if i == 1: permuted_apples[0], permuted_apples[-1] = permuted_apples[-1], permuted_apples[0]
            matching = get_matching(VGroup(*permuted_pears), VGroup(*permuted_apples))
            self.play(ShowCreation(matching), run_time = run_time) # 56.5, 64.5
            if i == 0: self.wait_to(59.5)
            self.play(Transform(permuted_apples[-1],permuted_apples[-1].copy().center().to_edge(UP)),
                      run_time = run_time) # 60.5, 65
            self.play(FocusOn2(permuted_apples[-1], highlight_color = WHITE)) # 61.5, 66

        subtraction = TexMobject("5-4=1")
        subtraction[0].set_color(RED)
        subtraction[2].set_color(YELLOW)
        subtraction[4].set_color(RED)
        subtraction.to_edge(RIGHT)

        self.wait_to(75.75)
        self.play(Write(subtraction))
        self.wait_to(86.5)
        self.play(FadeOut(VGroup(matching, subtraction, *permuted_apples+permuted_pears)))


def number_submobjects(mobj,direction):
    zero = TexMobject("0")
    zero.next_to(mobj.submobjects[0],direction=direction)
    submobjs = [zero]
    for i in xrange(1,len(mobj.submobjects)):
        submobj = TexMobject(str(i))
        submobj.next_to(submobjs[-1])
        submobj.shift((mobj.submobjects[i].get_center()[0]-submobj.get_center()[0],0,0))
        submobjs.append(submobj)
    return VGroup(*submobjs)

class InfiniteFruitScene(Scene):
    def construct(self):
        #self.force_skipping()

        self.fruit_num = 101
        apples = VGroup(*(Apple() for _ in xrange(self.fruit_num)))
        apples.arrange_submobjects(buff = 0.5)
        apples.to_edge(LEFT, buff = 2.5)

        pears = VGroup(*(
            Pear() for _ in xrange(self.fruit_num)
        ))
        for apple, pear in zip(apples, pears):
            pear.move_to(apple)

        apples.shift(1.5*UP)
        pears.shift(1.5*DOWN)

        apple_numbers = number_submobjects(apples,direction=UP)
        pear_numbers = number_submobjects(pears,direction=DOWN)

        self.play(ShowCreation(apples),Write(apple_numbers))
        self.wait_to(8)
        self.play(ShowCreation(pears),Write(pear_numbers))
        apples.submobjects.reverse()
        pears.submobjects.reverse()
        apple_numbers.submobjects.reverse()
        pear_numbers.submobjects.reverse()

        apples_ori = apples.copy()
        pears_ori  = pears.copy()
        apple_numbers_ori = apple_numbers.copy()
        pear_numbers_ori  = pear_numbers.copy()

        apples_persp = apples.copy()
        pears_persp  = pears.copy()
        apple_numbers_persp = apple_numbers.copy()
        pear_numbers_persp  = pear_numbers.copy()

        self.camera_distance = 12.0
        self.camera_point = apples[-1].get_center() * X_MASK
        vanishing_point = self.camera_point + self.camera_distance*RIGHT

        self.darken(apples_persp)
        self.darken(pears_persp)
        self.darken(apple_numbers_persp)
        self.darken(pear_numbers_persp)

        # perspective shift of numbers
        self.apply_perspective(apples_persp, objectwise = True)
        self.apply_perspective(pears_persp,  objectwise = True)
        self.apply_perspective(apple_numbers_persp, objectwise = False)
        self.apply_perspective(pear_numbers_persp,  objectwise = False)

        self.wait_to(15)
        self.play(
            ReplacementTransform(apples, apples_persp),
            ReplacementTransform(pears,  pears_persp),
            ReplacementTransform(apple_numbers, apple_numbers_persp),
            ReplacementTransform(pear_numbers,  pear_numbers_persp),
        )
        apples = apples_persp
        pears  = pears_persp
        apple_numbers = apple_numbers_persp
        pear_numbers  = pear_numbers_persp


        matching = make_ordinal_matching(
            Ordinal(*apples[1:]),
            Ordinal(*pears[1:]),
        )
        self.darken(matching)
        self.wait_to(18.7)
        self.play(ShowCreation(matching))
        matching_straight = matching.copy()

        self.revert_to_original_skipping_status()
        
        # Extra apple
        self.show_extra_fruit(apples, apples_ori, apple_numbers, apple_numbers_ori,
                              matching, apples[:-1], pears[1:], matching_straight) # 43

        # Extra pear
        self.show_extra_fruit(pears, pears_ori, pear_numbers, pear_numbers_ori,
                              matching, apples[1:], pears[:-1], matching_straight,
                              brief = True) # 51

        self.play(Transform(matching, matching_straight)) # 52

        definition = TextMobject("Definice:","$|A| = |B|$")
        definition.to_edge(UP)
        self.wait_to(54.3)
        self.play(Write(definition[0]))

        self.wait_to(57.7)
        apple_box, apple_label = self.pack_into_box(apples, apple_numbers, UP, 'A', RED,
                                                    matching, apples, pears) # 58.7
        pear_box, pear_label = self.pack_into_box(pears, pear_numbers, DOWN, 'B', YELLOW,
                                                  matching, apples, pears) # 59.7

        self.wait_to(60 + 11.5)
        self.move_labels_to_definition(apple_label, pear_label, definition[1])

        finite_pears = VGroup(*pears_ori[-3:])
        finite_pears.move_to(pear_box)
        pears_dest = VGroup(*[
            pears[0].copy()
            for _ in range(len(pears)-3)
        ])
        pears_dest.fade(0)
        pears_dest.add(*finite_pears.submobjects)

        self.wait_to(60+27)
        self.play(
            Uncreate(matching),
            FadeOut(definition[1]),
        ) # 1:28
        self.play(
            Transform(pears, pears_dest),
        ) # 1:29
        self.remove(pears)
        self.add(finite_pears)
        finite_pears.submobjects.reverse()
        pears = finite_pears

        def attempt(i0, i1, i2, remove = True):
            apple_indices = i0, i1, i2
            matching = get_matching(
                pears,
                VGroup(*(apples.submobjects[-1-i] for i in apple_indices))
            )
            self.play(ShowCreation(matching), submobject_mode = "all_at_once")
            self.dither()
            if remove: self.remove(matching)
            else: return matching

        self.wait_to(60 + 30.5)
        attempt(5,8,12) # 32.5
        attempt(0,10,19) # 34.5
        matching = attempt(7,1,0, remove = False) # 35.5

        def2 = TextMobject(":","$|A|>|B|$")
        def2.shift(definition[0][-1].get_center() - def2[0].get_center())

        self.wait_to(60 + 37)
        self.move_labels_to_definition(apple_label, pear_label, def2[1])
        self.wait_to(60+45.5)

    def perspective_ratio(self, point):
        return self.camera_distance / (self.camera_distance + point[0])

    def apply_perspective(self, mob, objectwise = True):
        if isinstance(mob, list): mob = VGroup(*mob)

        mob.shift(-self.camera_point)
        if objectwise:
            for submob in mob:
                ratio = self.perspective_ratio(submob.get_center())
                submob.scale(ratio)
                submob.set_stroke(width = ratio*submob.stroke_width)
        else:
            def perspective_shift(point):
                return point * self.perspective_ratio(point)
            for submob in mob.family_members_with_points():
                submob.points = np.apply_along_axis(perspective_shift, 1, submob.points)
        mob.shift(self.camera_point)

    def darken(self, row):
        for i, el in enumerate(reversed(row)):
            darkness = float(i)/(self.fruit_num-1)
            #print i, darkness
            el.fade(darkness)

    def show_extra_fruit(self, fruits, fruits_ori, fruit_numbers, fruit_numbers_ori,
                         matching, m1, m2, matching_straight, brief = False):

        matching_shifted = make_ordinal_matching(
            Ordinal(*m1), Ordinal(*m2),
        )
        self.darken(matching_shifted)

        if not brief: self.wait_to(26)
        self.play(Transform(matching, matching_shifted))

        if not brief:
            self.wait_to(28.4)
            self.play(FocusOn2(m2[-1], highlight_color = WHITE))
            self.play(FocusOn2(m1[-1], highlight_color = WHITE))
            self.play(FocusOn2(m2[-2], highlight_color = WHITE), run_time = 0.7)
            self.play(FocusOn2(m1[-2], highlight_color = WHITE))

        fruits_shifted = fruits_ori.copy()
        fruit_numbers_shifted = fruit_numbers_ori.copy()

        shift = fruits_shifted[-1].get_center() - fruits_shifted[-2].get_center()
        extra_fruit = []

        for row, objectwise in [(fruits_shifted, True), (fruit_numbers_shifted, False)]:
            row.shift(shift)
            extra_fruit += row[-1]
            persp_row = row[:-1]
            self.darken(persp_row)
            self.apply_perspective(persp_row, objectwise)

        extra_fruit = VGroup(*extra_fruit)
        extra_fruit.center()
        extra_fruit.to_edge(LEFT)

        fruits.save_state()
        fruit_numbers.save_state()
        if not brief: self.wait_to(33.6)
        self.play(
            Transform(fruits, fruits_shifted),
            Transform(fruit_numbers, fruit_numbers_shifted),
            Transform(matching, matching_straight),
        )
        if not brief: self.wait_to(35.7)
        self.play(FocusOn2(fruits[-1], highlight_color = WHITE))

        if not brief: self.wait_to(42)
        else: self.wait_to(50)

        self.play(
            fruits.restore,
            fruit_numbers.restore,
            Transform(matching, matching_shifted),
        ) # 43, 51

    def pack_into_box(self, fruits, numbers, shift_dir, set_name, color,
                      matching, m1, m2):
        fruits_dest = fruits.copy()
        fruits_dest.shift(0.2*shift_dir)

        if m1 == fruits: m1 = fruits_dest
        if m2 == fruits: m2 = fruits_dest
        matching_dest = make_ordinal_matching(
            Ordinal(*m1[1:]),
            Ordinal(*m2[1:]),
        )
        self.darken(matching_dest)

        box = SurroundingRectangle(fruits_dest, color=color)
        label = TexMobject(set_name)
        label.set_color(color)
        label.next_to(box,direction=LEFT, buff=0.5)
        self.play(
            FadeOut(numbers),
            Transform(fruits, fruits_dest),
            Transform(matching, matching_dest),
            ShowCreation(box),
            Write(label)
        )
        self.add_foreground_mobjects(box)

        return box, label

    def move_labels_to_definition(self, apple_label, pear_label, definition): # 2
        apple_label_dest = definition[1]
        pear_label_dest = definition[-2]
        apple_label_dest.set_color(RED)
        pear_label_dest.set_color(YELLOW)
        self.play(
            ReplacementTransform(apple_label[0].copy(), apple_label_dest),
            ReplacementTransform(pear_label[0].copy(), pear_label_dest),
        )
        definition_remaining = copy.copy(definition)
        definition_remaining.submobjects = copy.copy(definition_remaining.submobjects)
        definition_remaining.remove(apple_label_dest, pear_label_dest)
        self.play(Write(definition_remaining))
        self.dither()
        
class NaturalsSubsets(Scene):
    def construct(self):
        self.numbers = VGroup(*(self.number_tex(i) for i in xrange(15)))

        self.number_text = TextMobject("P","řiroz","en","á čísl","a", arg_separator = '').to_edge(UP)
        self.play(ShowCreation(self.numbers),Write(self.number_text))

        self.wait_to(3.5)
        self.show_matching(lambda n: 2*n, "Sudá čísla", gradual_creation = True)
        self.dither()

        to_remove = self.show_matching(lambda n: n ** 2, "Druhé mocniny", end_mode = 'keep')
        self.wait_to(48.3)
        self.remove(to_remove)

        small_primes = [
            2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,
            71,73,79,83,89,97,101,103,107,109,113
        ]
        self.show_matching(small_primes, "Prvočísla", end_mode = 'keep')
        self.wait_to(60)

    def number_pos(self, number, direction = UP):
        return LEFT_SIDE + (1.3*number + 2)*RIGHT + direction

    def number_tex(self, i):
        mobj = TexMobject(str(i))
        mobj.move_to(self.number_pos(i))
        mobj.number = i
        return mobj

    def cardinality_tex(self, number_type):
        result = TexMobject("|","\\text{Přirozená čísla}","|=|","\\text{" + number_type + "}","|").to_edge(UP)
        result[-2].set_color(RED)
        return result

    def show_matching(self, subset, set_description, gradual_creation = False, end_mode = 'uncreate'):
        if callable(subset):
            subset = [subset(i) for i in range(len(self.numbers))]
        subset = VGroup(*[self.number_tex(i) for i in subset])

        # shift down
        subset_dest = subset.copy()
        for num in subset_dest: num.move_to(self.number_pos(num.number, DOWN))
        self.play(Transform(subset, subset_dest)) # 46

        # compactize
        subset_dest = subset.copy()
        subset_dest.highlight(RED)
        for i, num in enumerate(subset_dest): num.move_to(self.number_pos(i, DOWN))
        if gradual_creation: self.wait_to(16.7)
        self.play(Transform(subset, subset_dest)) # 47

        matching = get_matching(subset, self.numbers)
        matching.stretch(-1, 1)
        number_text_dest = self.cardinality_tex(set_description)
        if gradual_creation:
            self.wait_to(25.8)
            for i in range(3):
                self.play(ShowCreation(matching[i]), run_time = 1.1)
            self.play(ShowCreation(VGroup(*matching[i+1:])))

            self.wait_to(31.6)
            self.play(ReplacementTransform(self.number_text, number_text_dest))

        else:
            self.play(
                ShowCreation(matching),
                ReplacementTransform(self.number_text, number_text_dest),
            ) # 48

        self.number_text = number_text_dest
        if gradual_creation: self.wait_to(41)

        if end_mode == 'uncreate': self.play(Uncreate(matching),Uncreate(subset))
        elif end_mode == 'remove': self.remove(matching, subset)
        elif end_mode == 'keep': return VGroup(matching, subset)

class NotationScene(Scene):

    def construct(self):

        self.prepare_overall_picture()

        numbers = VGroup(*(TexMobject(str(i)) for i in xrange(15)))
        for i, num in enumerate(numbers): num.move_to(i*RIGHT)
        aleph0_brace = Brace(numbers, UP)
        aleph0_brace.highlight(GREEN)
        VGroup(aleph0_brace, numbers).shift(self.sizes[1].get_edge_center(DOWN) + 0.2*DOWN
                                            - aleph0_brace.get_tip())


        self.play(Write(self.title))
        self.wait_to(3.2)
        self.play(self.finite_brace.creation_anim())
        self.wait_to(7.5)
        self.play(Write(self.sizes[0]))
        self.wait_to(10.5)
        self.play(Write(self.subtitle))
        self.wait_to(18)
        self.play(self.infinite_brace.creation_anim())
        self.wait_to(19.5)
        self.play(FadeIn(numbers), GrowFromCenter(aleph0_brace))
        self.wait_to(24.5)
        self.play(ReplacementTransform(aleph0_brace.copy(), self.sizes[1]))

        def number_pos(n):
            return numbers[0].get_center() + n*(numbers[1].get_center() - numbers[0].get_center())

        subset = VGroup(*(TexMobject(str(2*n)) for n in xrange(15)))
        for n, mob in enumerate(subset): mob.move_to(number_pos(2*n))
        subset2 = subset.copy()
        subset3 = subset2.copy()
        for n, mob in enumerate(subset3): mob.move_to(number_pos(n))
        VGroup(subset2, subset3).shift(DOWN)
        subset3.highlight(RED)

        self.wait_to(48)
        self.play(Transform(subset, subset2))
        self.play(Transform(subset, subset3))
        self.wait_to(56.5)
        self.play(FocusOn2(self.sizes[1][1]))
        self.wait_to(58)
        self.play(FadeOut(VGroup(subset, numbers, aleph0_brace)))
        self.play(self.countable_brace.creation_anim())
        self.wait_to(60 + 19.5)

    def prepare_overall_picture(self):
        self.title = TextMobject("Značení").scale(1.3).to_edge(UP)
        self.subtitle = TextMobject("Kardinální čísla").next_to(self.title, DOWN, buff = 0.5)

        self.sizes = TexMobject("0,1,2,\ldots", "\\aleph_0")
        self.sizes.highlight(GREEN)
        self.sizes.shift(DOWN)
        sizes0_ori = self.sizes[0].copy()
        self.sizes[0].shift(3*LEFT)
        sizes1_behind = self.sizes[1].copy()
        sizes1_behind.behind_edge(RIGHT)
        sizes1_next = self.sizes[0].copy()
        sizes1_next.next_to(
            self.sizes[1],
            buff = (self.sizes[1].get_edge_center(LEFT) - sizes0_ori.get_edge_center(RIGHT))[0],
            coor_mask = X_MASK,
        )

        self.finite_brace = BraceText(VGroup(self.sizes[0], sizes0_ori), "konečné mohutnosti", UP)
        self.infinite_brace = BraceText(VGroup(self.sizes[1], sizes1_behind), "nekonečné", UP)
        self.countable_brace = BraceText(self.sizes, "spočetné mohutnosti", DOWN)
        self.uncountable_brace = BraceText(VGroup(sizes1_next, sizes1_behind), "nespočetné", DOWN)
        self.uncountable_brace.desc.shift(0.5*LEFT)
        self.overall_picture = VGroup(
            self.sizes,
            self.finite_brace, self.infinite_brace,
            self.countable_brace, self.uncountable_brace,
        )

class InftyPlusInfty(Scene):

    def construct(self):

        #self.force_skipping()

        self.make_numbers()
        self.numbers.to_corner(UP+LEFT)

        even, even_ori, even_spaced, even_arranged = self.make_subset(lambda n: 2*n, 2)
        odd,  odd_ori,  odd_spaced,  odd_arranged  = self.make_subset(lambda n: 2*n+1, 3)

        self.add(self.numbers)

        self.play(Transform(even, even_spaced))
        VGroup(even_ori, even_spaced, even_arranged).highlight(RED)
        self.play(Transform(even, even_arranged))
        self.wait_to(9.5)

        self.play(Transform(odd, odd_spaced))
        VGroup(odd_ori, odd_spaced, odd_arranged).highlight(YELLOW)
        self.play(Transform(odd, odd_arranged))

        brace = BraceDesc(odd, "\\aleph_0")
        self.play(brace.creation_anim())

        self.wait_to(16.5)
        self.play(
            Transform(even, even_spaced),
            Transform(odd, odd_spaced),
        )
        self.play(
            Transform(even, even_ori),
            Transform(odd, odd_ori),
        )
        self.remove(self.numbers)

        self.wait_to(21)
        self.play(
            Transform(even, even_spaced),
            Transform(odd, odd_spaced),
        ) # 22
        self.play(
            Transform(even, even_arranged),
            Transform(odd, odd_arranged),
        ) # 23

        even_abstr = VGroup(*[Dot(num.get_center(), color = RED)    for num in even])
        odd_abstr  = VGroup(*[Dot(num.get_center(), color = YELLOW) for num in odd])
        self.wait_to(37)
        self.play(
            Transform(even, even_abstr),
            Transform(odd, odd_abstr),
        )

        apples_shrinked, apples, apples_spaced, apples_in_set \
            = self.make_fruit_set(Apple().scale(0.6),
                                  even_arranged, even_spaced, even_ori)
        pears_shrinked, pears, pears_spaced, pears_in_set \
            = self.make_fruit_set(Pear().scale(0.6),
                                  odd_arranged, odd_spaced, odd_ori)
        self.wait_to(44)
        self.play(
            ReplacementTransform(apples_shrinked, apples),
            ReplacementTransform(pears_shrinked, pears),
        )
        self.remove(even, odd)
        self.wait_to(50)

        self.play(
            Transform(apples, apples_spaced),
            Transform(pears, pears_spaced),
        )
        self.play(
            Transform(apples, apples_in_set),
            Transform(pears, pears_in_set),
        )

        sum_formula = TexMobject('\\aleph_0','+','\\aleph_0',"=\\aleph_0")
        sum_formula[0].highlight(RED)
        sum_formula[2].highlight(YELLOW)
        sum_formula.shift(BOTTOM/2)
        self.wait_to(55)
        self.play(Write(sum_formula))
        self.wait_to(60 + 10)
        self.play(FadeOut(VGroup(sum_formula, apples, pears, brace)))

    def make_numbers(self, num_num = 15):
        self.numbers = VGroup(*(TexMobject(str(i)) for i in xrange(num_num)))
        for i, num in enumerate(self.numbers): num.move_to(i*RIGHT)

    def make_subset(self, subset, down_shift):
        if callable(subset):
            subset = [subset(n) for n in range(len(self.numbers))]
        subset = VGroup(*[self.number_tex(n) for n in subset])
        subset_ori = subset.copy()
        subset_spaced = subset.copy()
        subset_arranged = subset.copy()
        for i, num in enumerate(subset_arranged): num.move_to(self.number_pos(i))
        VGroup(subset_spaced, subset_arranged).shift(down_shift * DOWN)

        return subset, subset_ori, subset_spaced, subset_arranged

    def number_pos(self, n):
        return self.numbers[0].get_center() + n*(self.numbers[1].get_center()
                                                 - self.numbers[0].get_center())

    def number_tex(self, n):
        return TexMobject(str(n)).move_to(self.number_pos(n))

    def make_fruit_set(self, fruit_example, num_arranged, num_spaced, num_ori):

        fruits = VGroup(*[
            fruit_example.copy().move_to(num.get_center())
            for num in num_arranged
        ])
        shrinked = fruits.copy()
        spaced = fruits.copy()
        in_set = fruits.copy()

        for fruit in shrinked:
            fruit.scale_in_place(0)
            fruit.highlight(num_arranged.fill_color)

        for fruit, num in zip(spaced, num_spaced): fruit.move_to(num)
        for fruit, num in zip(in_set, num_ori):    fruit.move_to(num)

        return shrinked, fruits, spaced, in_set

class IntegersScene(Scene):

    def construct(self):

        negatives = VGroup(*[
            self.number_tex(-n) for n in range(9)
        ])
        positives = VGroup(*[
            self.number_tex(n) for n in range(9)
        ])
        negatives.shift(UP)

        neg_brace = BraceDesc(negatives, "\\aleph_0", UP)
        pos_brace = BraceDesc(positives, "\\aleph_0", DOWN)

        self.play(ShowCreation(negatives))
        self.wait_to(6.3)
        self.play(neg_brace.creation_anim())

        self.wait_to(12.3)
        self.play(ShowCreation(positives))
        self.play(pos_brace.creation_anim())
        self.wait_to(16)

        self.play(
            positives.shift, UP,
            pos_brace.shift, UP,
        )

        self.wait_to(17.2)
        self.remove(positives[0])
        self.play(
            FadeOut(pos_brace),
            neg_brace.shift_brace, VGroup(negatives, negatives[-1].copy().move_to(positives[-1])),
        )

        self.wait_to(21)
        conversation = Conversation(self)
        conversation.add_bubble("A co ta sloučená nula?")

        self.wait_to(27.1)
        conversation.add_bubble("Mohutnost je stále nekonečná spočetná.")

        self.wait_to(36)

    def number_tex(self, n):
        return TexMobject(str(n)).move_to(n*RIGHT)

class InfiniteTable(InftyPlusInfty):

    def construct(self):
        #self.force_skipping()

        self.cur_color = WHITE
        self.number_mul = 1
        self.make_numbers(num_num = 14)
        self.numbers.to_corner(UP+LEFT)
        self.numbers.shift(1.5*RIGHT)
        self.add(self.numbers)

        even, _, even_spaced, even_arranged = self.make_subset(lambda n: 2*n, 3)
        odd,  _, odd_spaced,  odd_arranged  = self.make_subset(lambda n: 2*n+1, 2)

        odd_arranged.highlight(YELLOW)
        even_arranged.highlight(RED)

        self.play(
            Transform(even, even_spaced),
            Transform(odd,  odd_spaced),
        )
        self.wait_to(7)
        self.play(
            Transform(even, even_arranged),
            Transform(odd,  odd_arranged),
        )
        
        colors = color_gradient([YELLOW, GREEN, BLUE], 6)
        ori_numbers = self.numbers
        self.numbers = even
        self.number_mul = 2
        self.cur_color = RED

        table = [odd]

        self.wait_to(11.2)
        for index, color in enumerate(colors[1:]):
            if index <= 2: run_time = 1
            else: run_time = 0.5

            subodd, _, _, subodd_arranged \
                = self.make_subset(lambda n: 2*n+1, 0)
            table += [subodd]
            subeven, _, subeven_spaced, subeven_arranged \
                = self.make_subset(lambda n: 2*n, 1)
            self.remove(self.numbers)
            self.add(subodd, subeven)
            subodd_arranged.highlight(color)

            self.play(Transform(subeven, subeven_spaced), run_time = run_time)
            if index < 2: self.dither()
            self.play(
                Transform(subeven, subeven_arranged),
                Transform(subodd, subodd_arranged),
                run_time = run_time,
            )
            if index == 0: self.wait_to(18.5)

            self.number_mul *= 2
            self.numbers = subeven

        missing_zero = ori_numbers[0].copy().highlight(RED)

        self.wait_to(33.3)
        self.play(Write(missing_zero))
        self.remove(ori_numbers[0])
        ori_numbers.save_state()
        ori_numbers.remove(ori_numbers[0])
        self.play(missing_zero.behind_edge, DOWN)

        h_brace = BraceDesc(odd, "\\aleph_0", UP)
        h_brace.desc.highlight(YELLOW)
        v_brace = BraceDesc(VGroup(odd, subeven), "\\aleph_0", LEFT)
        v_brace.desc.highlight(BLUE)
        v_brace.shift(0.2*LEFT)

        self.wait_to(37.8)
        self.play(
            FadeOut(ori_numbers),
            h_brace.creation_anim(),
        )
        self.wait_to(41.5)
        self.play(v_brace.creation_anim())

        prod_formula = TexMobject("\\aleph_0","\\cdot","\\aleph_0"," = \\aleph_0")
        prod_formula[0].highlight(BLUE)
        prod_formula[2].highlight(YELLOW)
        prod_formula.to_corner(LEFT+UP)

        self.wait_to(45)
        self.play(
            ReplacementTransform(v_brace.desc[0].copy(), prod_formula[0]),
            ReplacementTransform(h_brace.desc[0].copy(), prod_formula[2]),
        )
        self.play(Write(VGroup(prod_formula[1], prod_formula[3])))

        table_but_first_column = VGroup(*[VGroup(*row[1:]) for row in table])
        self.wait_to(60 + 6.5)
        self.play(
            FadeOut(VGroup(h_brace, v_brace, prod_formula)),
            table_but_first_column.set_fill, None, 0.4,
        )

        formula_r_ori = None
        self.wait_to(60 + 10.5)
        for i, row in enumerate(table[:4]):
            formula_r = TexMobject("2^{"+str(i)+"}=")
            formula_r.highlight(rgb_to_color(row[0].family_members_with_points()[0].fill_rgb))
            formula_r.next_to(row[0], LEFT, buff = 0.3, aligned_edge = DOWN)

            if formula_r_ori is None: self.play(Write(formula_r), run_time = 1.3)
            else: self.play(ReplacementTransform(formula_r_ori, formula_r), run_time = 0.8)

            formula_r_ori = formula_r

        formula_r = TexMobject("2^r=")
        formula_r.shift(formula_r_ori[0].get_center() - formula_r[0].get_center())
        formula_r.highlight(BLUE)
        formula_r[-1].set_fill(opacity = 0)
        formula_r.to_edge(DOWN)
        self.wait_to(60 + 14.5)
        self.play(ReplacementTransform(formula_r_ori, formula_r))

        self.wait_to(60 + 20)
        self.play(table_but_first_column.set_fill, None, 1)
        table_but_first_row = VGroup(*table[1:])
        self.play(table_but_first_row.set_fill, None, 0.4)

        formula_c = TexMobject("(2c+1)")
        formula_c.to_edge(UP)
        formula_c.highlight(YELLOW)

        self.wait_to(60 + 24.5)
        self.play(Write(formula_c))

        self.wait_to(60 + 30.8)
        self.play(table_but_first_row.set_fill, None, 1)

        show_r = 3
        show_c = 5

        show_circ = Circle(radius = 0.45)
        show_circ.highlight(GREEN)
        show_circ.move_to(table[show_r][show_c])

        show_r_circ = show_circ.copy()
        show_r_circ.move_to(table[show_r][0], coor_mask = X_MASK)
        show_r_circ.highlight(BLUE)

        show_c_circ = show_circ.copy()
        show_c_circ.move_to(table[0][show_c], coor_mask = Y_MASK)
        show_c_circ.highlight(YELLOW)

        # 31.8
        self.play(ShowCreation(show_circ))
        self.wait_to(60 + 33.8)
        self.play(ShowCreation(show_c_circ))
        self.play(ShowCreation(show_r_circ))

        formula_prod = TexMobject("2^r",'\\cdot',"(2c+1)", "-1")
        formula_prod.to_corner(UP+LEFT)
        formula_prod[0].highlight(BLUE)
        formula_prod[2].highlight(YELLOW)

        self.dither()
        self.play(
            FadeIn(formula_prod[1]),
            ReplacementTransform(formula_r.copy(), formula_prod[0]),
            ReplacementTransform(formula_c.copy(), formula_prod[2]),
        )

        self.wait_to(60 + 46) 
        self.play(FadeOut(VGroup(formula_r, formula_c, show_circ, show_c_circ, show_r_circ)))

        pairs_table = VGroup(*[
            VGroup(*[
                self.pair_tex(r, c, mob)
                for c, mob in enumerate(row)
            ])
            for r, row in enumerate(table)
        ])
        table = VGroup(*table)

        for row in table:
            for num in row:
                num.submobjects = [VGroup(digit) for digit in num.submobjects]

        self.revert_to_original_skipping_status()
        self.wait_to(60 + 48)
        self.play(ReplacementTransform(table, pairs_table))

        self.wait_to(60 + 52.5)
        h_shift = RIGHT*(table[0][1].get_center() - table[0][0].get_center())
        table = pairs_table
        table_dest = table.copy()
        for r, row in enumerate(table_dest):
            for c, num in enumerate(row):
                num.shift(h_shift * ((2**r)*(2*c+1)-1 -c))
        self.play(Transform(table, table_dest))

        table_dest = table.copy()
        for row in table_dest:
            for num in row: num.move_to(2*DOWN, coor_mask = Y_MASK)
        self.play(Transform(table, table_dest))

        pairs_row = VGroup(*it.chain(*table))
        pairs_row.submobjects.sort(key = lambda mob: mob.get_center()[0])

        ori_numbers.restore()
        ori_numbers.shift(pairs_row[0].get_center() - ori_numbers[1].get_center())
        ori_numbers.shift(2*UP)
        matching = VGroup(*[
            Line(num.get_edge_center(DOWN), pair.get_edge_center(UP), buff = 0.2)
            for num, pair in zip(ori_numbers[1:], pairs_row)
        ])
        self.wait_to(60 + 55)
        self.play(
            ShowCreation(ori_numbers),
            ShowCreation(matching),
        )

        matching.add(matching[-1].copy())
        matching[-1].shift(h_shift)

        general_pair = TexMobject("r,c")
        general_pair[0].highlight(BLUE)
        general_pair[2].highlight(YELLOW)
        visible_formula_prod = VGroup(*formula_prod[:3])
        general_pair.move_to(visible_formula_prod)
        general_pair.shift(2*DOWN)
        general_matching = Line(general_pair.get_edge_center(UP),
                                visible_formula_prod.get_edge_center(DOWN),
                                buff = 0.2)
        self.wait_to(60 + 57)
        self.play(FadeIn(general_pair))
        self.play(ShowCreation(general_matching))

        self.wait_to(2*60 + 10)
        self.play(Write(formula_prod[-1]))
        self.play(VGroup(matching, pairs_row).shift, -h_shift)
        self.wait_to(2*60 + 26)

    def number_tex(self, n):
        result = TexMobject(str(n*self.number_mul))
        result.move_to(self.number_pos(n))
        if n*self.number_mul >= 100: result.scale_in_place(0.7)
        result.highlight(self.cur_color)
        return result

    def pair_tex(self, r, c, position):
        result = TexMobject(str(r),'{,}',str(c))
        result[0].highlight(BLUE)
        result[2].highlight(YELLOW)
        if c < 10: result.scale(0.8)
        else: result.scale(0.7)
        result.move_to(position)
        return result

class RationalsScene(NotationScene):

    def construct(self):

        self.h_space = 2
        self.colors = color_gradient([YELLOW, GREEN, BLUE, DARK_BLUE, DARK_GRAY], 20)

        numbers = self.make_numbers()
        self.play(
            ShowCreation(numbers[0]),
            ShowCreation(numbers[1]),
        )
        brace = BraceDesc(numbers[0], "\\aleph_0", DOWN)
        brace.next_to(numbers[1], DOWN, coor_mask = Y_MASK, buff = 0.3)

        self.wait_to(6)
        self.play(brace.creation_anim())

        skip = False
        denominator = 2
        parts = []
        while True:
            if denominator < 4: run_time = 1
            else: run_time = 0.5

            parts.append(numbers[0].copy())

            if denominator == 2: self.wait_to(9.5)
            elif denominator == 3: self.wait_to(13.5)
            self.add(parts[-1])
            self.play(VGroup(numbers, brace).shift, 0.9*DOWN, run_time = run_time)

            if denominator == 2: self.wait_to(12)
            elif denominator == 3: self.wait_to(14.7)
            self.remove(numbers)
            if denominator == 6: break
            numbers = self.make_numbers(denominator, numbers)
            ori_numbers = self.make_numbers(denominator-1, numbers)
            if skip:
                offset = (len(ori_numbers[1])//2+1) %2
                for label in ori_numbers[1][offset::2]:
                    label.set_fill(opacity = 0)
            if denominator == 4: skip = True
            if skip:
                offset = (len(numbers[1])//2+1) %2
                for label in numbers[1][offset::2]:
                    label.set_fill(opacity = 0)

            self.play(ReplacementTransform(ori_numbers, numbers), run_time = run_time)
            denominator += 1

        self.remove(brace, numbers)

        while denominator < len(self.colors)+1:
            part = self.make_dots(denominator)
            part.move_to(parts[-1])
            part.shift(0.5*DOWN)
            parts.append(part)
            denominator += 1

        parts.reverse()
        parts = VGroup(*parts)
        parts_dest = parts.copy()
        for part in parts_dest: part.center()
        self.wait_to(20.5)
        self.play(Transform(parts, parts_dest), run_time = 2)

        rationals = TexMobject('|',"\\text{Racionální čísla}","| = \\aleph_0")
        rationals.shift(0.5*DOWN - rationals[1].get_edge_center(UP))
        self.wait_to(26.5)
        self.play(Write(rationals[1]))

        dots7 = self.make_dots(7)
        dots7.shift(2*DOWN)
        center = len(dots7)//2
        pi_dot = dots7[center+22]
        pi_label = TexMobject("\\frac{22}{7}")
        pi_label.next_to(pi_dot, DOWN)
        self.wait_to(30)
        self.play(Write(pi_label))

        self.wait_to(36)
        self.play(ShowCreation(dots7))
        self.play(FocusOn2(pi_dot, scale = 3))
        dots7.remove(pi_dot)
        self.play(FadeOut(dots7))
        self.play(VGroup(pi_dot, pi_label).shift, 2*UP)

        self.wait_to(41)
        self.play(FadeOut(VGroup(pi_dot, pi_label)))
        self.play(Write(VGroup(rationals[0], rationals[2])))

        conversation1 = Conversation(self)
        self.wait_to(60)
        conversation1.add_bubble("Takže jsou všechny množiny spočetné?")
        self.wait_to(60 + 6)
        conversation1.add_bubble("Jasně, že ne ;-)")
        #self.dither()
        #conversation2 = Conversation(self, start_answer = True)
        #conversation2.add_bubble("Of course not.")

        self.prepare_overall_picture()
        self.overall_picture.to_edge(UP, buff = 0.4)
        self.overall_picture.remove(self.uncountable_brace)
        self.wait_to(60 + 11.5)
        self.play(FadeIn(self.overall_picture))
        self.wait_to(60 + 13)
        self.play(self.uncountable_brace.creation_anim())

        self.wait_to(60 + 26)
        real_size = TexMobject("|\\mathbb R|")
        real_size.set_color(GREEN)
        real_size.next_to(self.sizes, buff = 1)
        self.play(Write(real_size))
        self.wait_to(60 + 45.5)

    def make_numbers(self, denominator = 1, template = None):
        if template is not None:
            min_num = len(template[0])//2
        else: min_num = 0

        dots = self.make_dots(denominator, min_num)
        max_num = len(dots)//2
        labels = []
        for n, dot in zip(range(-max_num, max_num+1), dots):
            if denominator == 1:
                tex = str(n)
            else:
                tex = "\\textstyle\\frac{"+str(n)+"}{"+str(denominator)+"}"
            label = TexMobject(tex)
            label.next_to(dot, DOWN)
            labels.append(label)

        labels = VGroup(*labels)
        labels.highlight(dots.color)
        result = VGroup(dots, labels)
        result.highlight(self.colors[denominator-1])
        if template is not None:
            dest_center = template[0][len(template[0])//2].get_center()
            result.shift(dest_center)

        return result

    def make_dots(self, denominator = 1, min_num = 0):
        
        max_num = max(int(np.ceil((SPACE_WIDTH/self.h_space+1)*denominator)), min_num)
        dots = []
        for n in range(-max_num, max_num+1):
            dot = Dot(float(n)/denominator * self.h_space*RIGHT)
            dot.scale_in_place(4.0/(4.0+denominator-1))
            dots.append(dot)
        dots = VGroup(*dots)
        dots.set_color(self.colors[denominator-1])
        return dots

class CantorDiagonal(Scene):

    def construct(self):

        self.zero = TexMobject('0')
        self.one = TexMobject('1')
        self.h_shift = 0.6*RIGHT
        self.v_shift = 0.8*DOWN
        self.diag_dir = self.h_shift + self.v_shift

        self.sequences = VGroup(*[
            self.make_seq()
            for _ in range(3)
        ])
        for seq, color in zip(self.sequences, color_gradient([WHITE, DARK_GREY], 3)):
            seq.set_color(color)
        self.sequences.arrange_submobjects(DOWN)
        self.sequences.to_edge(LEFT, buff = 3)
        self.sequences[1].shift(2*RIGHT)
        self.sequences[2].shift(RIGHT)

        for seq in self.sequences:
            self.play(ShowCreation(seq))

        column = VGroup(*[
            TexMobject(str(n)) for n in range(10)
        ])
        for i, num in enumerate(column):
            num.move_to(i*self.v_shift)

        column.to_corner(UP+LEFT)
        column.shift(DOWN)
        column.highlight(GREEN)

        self.matching_l_buff = 0.2
        self.matching_r_buff = 0.7
        self.wait_to(7.5)
        self.play(ShowCreation(column))
        matching = []
        for num in column:
            start = num.get_edge_center(RIGHT)+self.matching_l_buff*RIGHT
            end = copy.copy(start)
            end[0] = -SPACE_WIDTH+2.5
            matching.append(Line(start, end))

        for line, seq in zip(matching, self.sequences):
            seq_dest = seq.copy()
            seq_dest.highlight(WHITE)
            self.seq_to_match_line(seq_dest, line)
            self.play(
                Transform(seq, seq_dest),
                ShowCreation(line),
            )

        for line in matching[3:]:
            seq = self.make_seq()
            self.seq_to_match_line(seq, line)
            self.sequences.submobjects.append(seq)

        self.play(
            ShowCreation(VGroup(*matching[3:])),
            ShowCreation(VGroup(*self.sequences[3:])),
        )

        self.wait_to(18)
        missing_seq = self.apply_diag_argument()

        attempt_indices = [2, 6, 3]
        attempt = attempt_indices[0]

        self.wait_to(33)
        rect_ori = None
        for attempt in attempt_indices:
            rect = SurroundingRectangle(self.sequences[attempt], color = WHITE)
            if rect_ori is None: self.play(FadeIn(rect))
            else: self.play(ReplacementTransform(rect_ori, rect))
            self.play(FocusOn2(missing_seq[attempt]))
            self.dither()
            rect_ori = rect

        self.play(FadeOut(rect))
        self.sequences.add_to_back(missing_seq)
        sequences_dest = self.sequences.copy()
        sequences_dest.highlight(WHITE)

        for seq, line in zip(sequences_dest, matching):
            self.seq_to_match_line(seq, line)
        sequences_dest[-1].shift(DOWN)
        self.wait_to(48.5)
        self.play(Transform(self.sequences, sequences_dest))

        self.wait_to(51)
        missing_seq = self.apply_diag_argument(brief = True)

        self.wait_to(64)
        self.play(FadeOut(missing_seq))

        title = TextMobject("Cantorův diagonální argument")
        title.to_edge(UP)
        self.play(Write(title))
        self.wait_to()

    def seq_to_match_line(self, seq, line):
        seq.shift(line.get_end() - seq[0].get_center() + self.matching_r_buff*RIGHT)
        
    def random_digit(self):
        return [self.zero, self.one][random.randint(0,1)].copy()

    def make_seq(self, seq_len = 20):
        
        result = VGroup(*[
            self.random_digit()
            for i in range(seq_len)
        ])
        for i, digit in enumerate(result): digit.move_to(i*self.h_shift)
        return result

    def apply_diag_argument(self, brief = False):
        
        diag = []
        out_of_diag = []
        for i, seq in enumerate(self.sequences):
            diag.append(seq[i])
            out_of_diag += seq[:i]
            out_of_diag += seq[i+1:]

        diag_start = diag[0].get_center()
        arrow = Arrow(diag_start - 2*self.diag_dir,
                      diag_start - 0.5*self.diag_dir)

        diag = VGroup(*diag)
        out_of_diag = VGroup(*out_of_diag)
        if not brief: self.play(ShowCreation(arrow))
        self.play(
            diag.highlight, YELLOW,
            out_of_diag.highlight, DARK_GREY,
        )
        if not brief:
            self.play(FadeOut(arrow))
            self.wait_to(26)

        while len(diag) < len(self.sequences[0]):
            next_el = self.random_digit()
            next_el.highlight(YELLOW)
            next_el.move_to(diag[0])
            next_el.shift(len(diag)*self.diag_dir)
            diag.submobjects.append(next_el)
        self.add(diag)

        diag_extracted = diag.copy()
        for num in diag_extracted:
            num.to_edge(UP)

        self.play(ReplacementTransform(diag.copy(), diag_extracted))
        missing_seq = []
        for num in diag_extracted:
            inverted = TexMobject(str(1-int(num.tex_string)))
            inverted.highlight(RED)
            inverted.move_to(num)
            missing_seq.append(inverted)
        missing_seq = VGroup(*missing_seq)

        if not brief: self.wait_to(29)
        self.play(ReplacementTransform(diag_extracted, missing_seq))
        return missing_seq
