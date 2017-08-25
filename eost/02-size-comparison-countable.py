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
    Group(*bottom_row).arrange_submobjects(buff=0.1)
    Group(*top_row).arrange_submobjects(buff=0.1)
    Group(*top_row).next_to(Group(*bottom_row),direction=UP,buff=0)
    return Group(*(bottom_row + top_row))

def pear_pile():
    bottom_two = [Pear(i).rotate(random_small_angle()) for i in xrange(2)]
    Group(*bottom_two).arrange_submobjects(buff=0.1)
    third_on_bottom = Pear(2).next_to(Group(*bottom_two),buff=0.1)
    top = (Pear(3)).rotate(-np.pi/20).next_to(Group(*bottom_two),direction=UP,buff=0)
    return Group(*(bottom_two + [third_on_bottom, top]))

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

    def play(self,scene):
        for transform in self.transforms:
            scene.play(transform)

    def summarize(self):
        central_number = self.numbers[-1].copy()
        central_number.shift(
            Group(*self.numbers).get_center()
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
        Group(apples,pears).center()
        # Display the two lines of apples and pears
        self.play(Succession(*map(GrowFromCenterGeneral, apples.submobjects), rate_func=None, run_time = 1.5*DEFAULT_ANIMATION_RUN_TIME))
        self.play(Succession(*map(GrowFromCenterGeneral, pears.submobjects), rate_func=None, run_time = 1.5*DEFAULT_ANIMATION_RUN_TIME))
        self.dither()
        counted_apples = [Apple(i) for i in xrange(5)]
        counted_pears = [Pear(i) for i in xrange(4)]
        counted_apple_group = Group(*counted_apples).arrange_submobjects().to_edge(UP)
        counted_pear_group = Group(*counted_pears).arrange_submobjects().to_edge(DOWN)
        apple_count = CountTransform(apples,counted_apple_group,direction=DOWN)
        apple_count.play(self)
        pear_count = CountTransform(pears,counted_pear_group,direction=UP)
        pear_count.play(self)
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
        self.dither()
        self.play(*map(FadeOut,[
            apple_count.numbers[-1],
            inequality,
            pear_count.numbers[-1]
        ]))
        # Show a matching
        matching = MatchingAnimations(Group(*apples),Group(*pears))
        for anims in matching.match_animations:
            self.play(anims)
        self.play(Transform(apples[-1],apples[-1].copy().center().to_edge(UP)))
        self.play(FocusOn2(apples[-1], highlight_color = WHITE))

        buff = matching.buff
        matching = matching.matching
        for i in range(2):
            apples.submobjects.sort(key = lambda apple: apple.get_center()[0])
            apples_target = apples.copy()
            apples_target.arrange_submobjects(center = False, buff = buff)
            apples_target.shift(LEFT*apples_target.get_center()[0])
            self.play(Uncreate(matching))
            self.play(Transform(apples, apples_target))
            self.dither()
            # Permute them
            apple_permutations=permute_animations(apples,move="up")
            pear_permutations=permute_animations(pears,move="down")
            self.play(*(apple_permutations + pear_permutations))
            # Show a different matching
            permuted_apples = permute(apples)
            permuted_pears = permute(pears)
            if i == 1: permuted_apples[0], permuted_apples[-1] = permuted_apples[-1], permuted_apples[0]
            matching = get_matching(Group(*permuted_pears), Group(*permuted_apples))
            self.play(ShowCreation(matching))
            self.dither()
            self.play(Transform(permuted_apples[-1],permuted_apples[-1].copy().center().to_edge(UP)))
            self.play(FocusOn2(permuted_apples[-1], highlight_color = WHITE))

        self.dither()

def number_submobjects(mobj,direction):
    zero = TexMobject("0")
    zero.next_to(mobj.submobjects[0],direction=direction)
    submobjs = [zero]
    for i in xrange(1,len(mobj.submobjects)):
        submobj = TexMobject(str(i))
        submobj.next_to(submobjs[-1])
        submobj.shift((mobj.submobjects[i].get_center()[0]-submobj.get_center()[0],0,0))
        submobjs.append(submobj)
    return Group(*submobjs)

class InfiniteFruitScene(Scene):
    def construct(self):
        #self.force_skipping()

        self.fruit_num = 101
        apples = Group(*(Apple() for _ in xrange(self.fruit_num)))
        apples.arrange_submobjects(buff = 0.5)
        apples.to_edge(LEFT, buff = 2.5)

        pears = Group(*(
            Pear() for _ in xrange(self.fruit_num)
        ))
        for apple, pear in zip(apples, pears):
            pear.move_to(apple)

        apples.shift(1.5*UP)
        pears.shift(1.5*DOWN)

        apple_numbers = number_submobjects(apples,direction=UP)
        pear_numbers = number_submobjects(pears,direction=DOWN)

        self.play(ShowCreation(apples),Write(apple_numbers))
        self.play(ShowCreation(pears),Write(pear_numbers))
        self.dither()
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

        self.dither()

        matching = make_ordinal_matching(
            Ordinal(*apples[1:]),
            Ordinal(*pears[1:]),
        )
        self.darken(matching)
        self.play(ShowCreation(matching))
        self.dither()
        matching_straight = matching.copy()

        # Extra apple
        self.show_extra_fruit(apples, apples_ori, apple_numbers, apple_numbers_ori,
                              matching, apples[:-1], pears[1:], matching_straight)

        # Extra pear
        self.show_extra_fruit(pears, pears_ori, pear_numbers, pear_numbers_ori,
                              matching, apples[1:], pears[:-1], matching_straight)

        self.play(Transform(matching, matching_straight))

        definition = TextMobject("Definition:","$|A| = |B|$")
        definition.to_edge(UP)
        self.play(Write(definition[0]))

        apple_box, apple_label = self.pack_into_box(apples, apple_numbers, UP, 'A', RED,
                                                    matching, apples, pears)
        self.dither()

        pear_box, pear_label = self.pack_into_box(pears, pear_numbers, DOWN, 'B', YELLOW,
                                                  matching, apples, pears)
        self.dither()

        self.move_labels_to_definition(apple_label, pear_label, definition[1])

        finite_pears = VGroup(*pears_ori[-3:])
        finite_pears.move_to(pear_box)
        pears_dest = VGroup(*[
            pears[0].copy()
            for _ in range(len(pears)-3)
        ])
        pears_dest.fade(0)
        pears_dest.add(*finite_pears.submobjects)

        self.play(
            Uncreate(matching),
            FadeOut(definition[1]),
        )
        self.play(
            Transform(pears, pears_dest),
        )
        self.remove(pears)
        self.add(finite_pears)
        finite_pears.submobjects.reverse()
        pears = finite_pears
        self.revert_to_original_skipping_status()
        self.dither()

        def attempt(i0, i1, i2, remove = True):
            apple_indices = i0, i1, i2
            matching = get_matching(
                pears,
                Group(*(apples.submobjects[-1-i] for i in apple_indices))
            )
            self.play(ShowCreation(matching), submobject_mode = "all_at_once")
            self.dither()
            if remove: self.remove(matching)
            else: return matching

        attempt(5,8,12)
        attempt(0,10,19)
        matching = attempt(7,1,0, remove = False)

        def2 = TextMobject(":","$|A|>|B|$")
        def2.shift(definition[0][-1].get_center() - def2[0].get_center())

        self.move_labels_to_definition(apple_label, pear_label, def2[1])
        self.dither()

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
                         matching, m1, m2, matching_straight):

        matching_shifted = make_ordinal_matching(
            Ordinal(*m1), Ordinal(*m2),
        )
        self.darken(matching_shifted)

        self.play(Transform(matching, matching_shifted))
        self.dither()
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
        self.play(
            Transform(fruits, fruits_shifted),
            Transform(fruit_numbers, fruit_numbers_shifted),
            Transform(matching, matching_straight),
        )
        self.play(FocusOn2(fruits[-1], highlight_color = WHITE))
        self.dither()

        self.play(
            fruits.restore,
            fruit_numbers.restore,
            Transform(matching, matching_shifted),
        )
        self.dither()

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

    def move_labels_to_definition(self, apple_label, pear_label, definition):
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
        self.numbers = Group(*(self.number_tex(i) for i in xrange(15)))

        self.number_text = TextMobject("Natural Numbers").to_edge(UP)
        self.play(ShowCreation(self.numbers),Write(self.number_text))

        self.show_matching(lambda n: 2*n, "Even", gradual_creation = True)
        self.dither()

        self.show_matching(lambda n: n ** 2, "Square")
        self.dither()

        small_primes = [
            2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,
            71,73,79,83,89,97,101,103,107,109,113
        ]
        self.show_matching(small_primes, "Prime")

    def number_pos(self, number, direction = UP):
        return LEFT_SIDE + (1.3*number + 2)*RIGHT + direction

    def number_tex(self, i):
        mobj = TexMobject(str(i))
        mobj.move_to(self.number_pos(i))
        mobj.number = i
        return mobj

    def cardinality_tex(self, number_type):
        result = TexMobject("|","\\text{Natural Numbers}","|=|","\\text{" + number_type + " Numbers}","|").to_edge(UP)
        result[-2].set_color(RED)
        return result

    def show_matching(self, subset, set_description, gradual_creation = False):
        if callable(subset):
            subset = [subset(i) for i in range(len(self.numbers))]
        subset = VGroup(*[self.number_tex(i) for i in subset])

        # shift down
        subset_dest = subset.copy()
        for num in subset_dest: num.move_to(self.number_pos(num.number, DOWN))
        self.play(Transform(subset, subset_dest))

        # compactize
        subset_dest = subset.copy()
        subset_dest.highlight(RED)
        for i, num in enumerate(subset_dest): num.move_to(self.number_pos(i, DOWN))
        self.play(Transform(subset, subset_dest))

        matching = get_matching(subset, self.numbers)
        matching.stretch(-1, 1)
        number_text_dest = self.cardinality_tex(set_description)
        if gradual_creation:
            for i in range(3):
                self.play(ShowCreation(matching[i]))
                self.dither()
            self.play(ShowCreation(VGroup(*matching[i+1:])))
            self.play(ReplacementTransform(self.number_text, number_text_dest))

        else:
            self.play(
                ShowCreation(matching),
                ReplacementTransform(self.number_text, number_text_dest),
            )
        self.number_text = number_text_dest
        self.dither()
        self.play(Uncreate(matching),Uncreate(subset))

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
        self.dither()
        self.play(self.finite_brace.creation_anim())
        self.play(Write(self.sizes[0]))
        self.dither()
        self.play(Write(self.subtitle))
        self.dither()
        self.play(self.infinite_brace.creation_anim())
        self.play(FadeIn(numbers), GrowFromCenter(aleph0_brace))
        self.dither()
        self.play(ReplacementTransform(aleph0_brace.copy(), self.sizes[1]))
        self.dither()

        def number_pos(n):
            return numbers[0].get_center() + n*(numbers[1].get_center() - numbers[0].get_center())

        subset = VGroup(*(TexMobject(str(2*n)) for n in xrange(15)))
        for n, mob in enumerate(subset): mob.move_to(number_pos(2*n))
        subset2 = subset.copy()
        subset3 = subset2.copy()
        for n, mob in enumerate(subset3): mob.move_to(number_pos(n))
        VGroup(subset2, subset3).shift(DOWN)
        subset3.highlight(RED)

        self.play(Transform(subset, subset2))
        self.play(Transform(subset, subset3))
        self.dither()
        self.play(FocusOn2(self.sizes[1][1]))
        self.dither()
        self.play(FadeOut(VGroup(subset, numbers, aleph0_brace)))
        self.play(self.countable_brace.creation_anim())
        self.dither()

    def prepare_overall_picture(self):
        self.title = TextMobject("Notation").scale(1.3).to_edge(UP)
        self.subtitle = TextMobject("Cardinal Numbers").next_to(self.title, DOWN, buff = 0.5)

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

        self.finite_brace = BraceText(VGroup(self.sizes[0], sizes0_ori), "finite sizes", UP)
        self.infinite_brace = BraceText(VGroup(self.sizes[1], sizes1_behind), "infinite sizes", UP)
        self.countable_brace = BraceText(self.sizes, "countable sizes", DOWN)
        self.uncountable_brace = BraceText(VGroup(sizes1_next, sizes1_behind), "uncountable sizes", DOWN)
        self.uncountable_brace.desc.shift(0.5*LEFT)

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
        self.dither()

        self.play(Transform(odd, odd_spaced))
        VGroup(odd_ori, odd_spaced, odd_arranged).highlight(YELLOW)
        self.play(Transform(odd, odd_arranged))
        self.dither()

        brace = BraceDesc(odd, "\\aleph_0")
        self.play(brace.creation_anim())
        self.dither()

        self.play(
            Transform(even, even_spaced),
            Transform(odd, odd_spaced),
        )
        self.play(
            Transform(even, even_ori),
            Transform(odd, odd_ori),
        )
        self.remove(self.numbers)

        self.dither()
        self.play(
            Transform(even, even_spaced),
            Transform(odd, odd_spaced),
        )
        self.play(
            Transform(even, even_arranged),
            Transform(odd, odd_arranged),
        )
        self.dither()

        even_abstr = VGroup(*[Dot(num.get_center(), color = RED)    for num in even])
        odd_abstr  = VGroup(*[Dot(num.get_center(), color = YELLOW) for num in odd])
        self.play(
            Transform(even, even_abstr),
            Transform(odd, odd_abstr),
        )
        self.dither()

        apples_shrinked, apples, apples_spaced, apples_in_set \
            = self.make_fruit_set(Apple().scale(0.6),
                                  even_arranged, even_spaced, even_ori)
        pears_shrinked, pears, pears_spaced, pears_in_set \
            = self.make_fruit_set(Pear().scale(0.6),
                                  odd_arranged, odd_spaced, odd_ori)
        self.play(
            ReplacementTransform(apples_shrinked, apples),
            ReplacementTransform(pears_shrinked, pears),
        )
        self.remove(even, odd)
        self.dither()

        self.play(
            Transform(apples, apples_spaced),
            Transform(pears, pears_spaced),
        )
        self.play(
            Transform(apples, apples_in_set),
            Transform(pears, pears_in_set),
        )
        self.dither()

        sum_formula = TexMobject('\\aleph_0','+','\\aleph_0',"=\\aleph_0")
        sum_formula[0].highlight(RED)
        sum_formula[2].highlight(YELLOW)
        sum_formula.shift(BOTTOM/2)
        self.play(Write(sum_formula))
        self.dither()

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
        self.play(neg_brace.creation_anim())
        self.dither()

        self.play(ShowCreation(positives))
        self.play(pos_brace.creation_anim())
        self.dither()

        self.play(
            positives.shift, UP,
            pos_brace.shift, UP,
        )
        self.remove(positives[0])
        self.play(
            FadeOut(pos_brace),
            neg_brace.shift_brace, VGroup(negatives, negatives[-1].copy().move_to(positives[-1])),
        )
        self.dither()

        conversation = Conversation(self)
        conversation.add_bubble("Hey, what happened to the merged zero?")
        self.dither()
        conversation.add_bubble("The size is still countable infinite.")
        self.dither()

    def number_tex(self, n):
        return TexMobject(str(n)).move_to(n*RIGHT)

class InfiniteTable(InftyPlusInfty):

    def construct(self):
        #self.force_skipping()

        self.cur_color = WHITE
        self.number_mul = 1
        self.make_numbers(num_num = 13)
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
        self.play(
            Transform(even, even_arranged),
            Transform(odd,  odd_arranged),
        )
        self.dither()

        colors = color_gradient([YELLOW, GREEN, BLUE], 6)
        ori_numbers = self.numbers
        self.numbers = even
        self.number_mul = 2
        self.cur_color = RED

        for index, color in enumerate(colors[1:]):
            subodd, _, _, subodd_arranged \
                = self.make_subset(lambda n: 2*n+1, 0)
            subeven, _, subeven_spaced, subeven_arranged \
                = self.make_subset(lambda n: 2*n, 1)
            self.remove(self.numbers)
            self.add(subodd, subeven)
            subodd_arranged.highlight(color)

            self.play(Transform(subeven, subeven_spaced))
            if index < 2:
                self.play(Transform(subeven, subeven_arranged))
                self.dither()
                self.play(Transform(subodd, subodd_arranged))
                self.dither()
            else:
                self.play(
                    Transform(subeven, subeven_arranged),
                    Transform(subodd, subodd_arranged),
                )

            self.number_mul *= 2
            self.numbers = subeven

        self.revert_to_original_skipping_status()

        missing_zero = ori_numbers[0].copy().highlight(RED)
        self.play(Write(missing_zero))
        self.remove(ori_numbers[0])
        ori_numbers.remove(ori_numbers[0])
        self.play(missing_zero.behind_edge, DOWN)
        self.dither()

        h_brace = BraceDesc(odd, "\\aleph_0", UP)
        v_brace = BraceDesc(VGroup(odd, subeven), "\\aleph_0", LEFT)
        v_brace.shift(0.2*LEFT)
        self.play(
            FadeOut(ori_numbers),
            h_brace.creation_anim(),
        )
        self.dither()
        self.play(v_brace.creation_anim())

        self.dither()

        prod_formula = TexMobject("\\aleph_0\\cdot\\aleph_0 = \\aleph_0")
        prod_formula.to_corner(LEFT+UP)
        self.play(Write(prod_formula))
        self.dither()

    def number_tex(self, n):
        result = TexMobject(str(n*self.number_mul))
        result.move_to(self.number_pos(n))
        if n*self.number_mul >= 100: result.scale_in_place(0.7)
        result.highlight(self.cur_color)
        return result
