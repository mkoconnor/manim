from scene import Scene
from mobject.tex_mobject import *
from topics.geometry import *
from constants import *
from mobject import Mobject, Group
from .widgets import *
from animation.simple_animations import *
from animation.transform import *
import helpers
from .matching import get_matching, MatchingAnimations
import deterministic

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

class Scene1(Scene):
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
        self.emphasize(apples[-1])

        buff = matching.buff
        matching = matching.matching
        for _ in range(2):
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
            matching = get_matching(Group(*permuted_pears), Group(*permuted_apples))
            self.play(ShowCreation(matching))
            self.dither()
            self.play(Transform(permuted_apples[-1],permuted_apples[-1].copy().center().to_edge(UP)))
            self.emphasize(permuted_apples[-1])

        self.play(Uncreate(matching))
        self.dither()

    # Emphasize an apple mobj by making it slightly bigger and white
    def emphasize(self,apple):
        orig = apple.copy()
        emphasized = Apple(color=WHITE)
        emphasized.shift(orig.get_center() - emphasized.get_center())
        emphasized.scale_in_place(1.1)
        self.play(Transform(apple,emphasized))
        self.play(Transform(apple,orig))

class NumberLine(Mobject):
    def __init__(self,mobj_creator,direction,n=10):
        unnumbered_mobjs = []
        numbered_mobjs = []

        def make_number_mobj(n):
            text = TextMobject(str(n))
            buff = Rectangle(color=BLACK,height=1, width=1.9)
            return Group(buff,text)

        for i in xrange(n):
            copy = mobj_creator(i)
            unnumbered_mobjs.append(copy)
            number_mobj = make_number_mobj(i)
            number_mobj.next_to(copy,direction=direction)
            numbered_mobjs.append(Group(copy,number_mobj))

        Mobject.__init__(self, *numbered_mobjs)
        self.arrange_submobjects()

def number_submobjects(mobj,direction):
    zero = TexMobject("0")
    zero.next_to(mobj.submobjects[0],direction=direction)
    submobjs = [zero]
    for i in xrange(1,len(mobj.submobjects)):
        submobj = TexMobject(str(i))
        submobj.next_to(submobjs[-1])
        submobj.shift((mobj.submobjects[i].get_center()[0]-submobj.get_center()[0],0,0))
        submobjs.append(submobj)
    dots = TexMobject("\\cdots").next_to(submobjs[-1])
    submobjs.append(dots)
    return Group(*submobjs)

class Scene2(Scene):
    def construct(self):
        apples = Group(*(Apple() for _ in xrange(60))).arrange_submobjects().shift((0,1.5,0))
        apples.shift((-SPACE_WIDTH*3/4 - apples.get_critical_point(LEFT)[0],0,0))
        apple_numbers = number_submobjects(apples,direction=UP)
        # l for "larger"
        def lpear():
            p = Pear()
            buff = Rectangle(
                height=p.get_height(),
                width=apples.submobjects[0].get_width(),
                color=BLACK
            ).center()
            return Group(buff,p)
        pears = Group(*(lpear() for _ in xrange(60))).arrange_submobjects().shift((0,-1.5,0))
        pears.shift((-SPACE_WIDTH*3/4 - pears.get_critical_point(LEFT)[0],0,0))
        pear_numbers = number_submobjects(pears,direction=DOWN)
        self.play(ShowCreation(apples),Write(apple_numbers))
        self.play(ShowCreation(pears),Write(pear_numbers))
        self.dither()
        apples.save_state()
        pears.save_state()
        all=Group(apples,pears,apple_numbers,pear_numbers)
        x0=all.get_critical_point(LEFT)[0]
        def perspective_shift((x,y,z)):
            camera_distance = 7.0
            ratio = camera_distance / (camera_distance - (x0 - x))
            return (x*ratio,y*ratio,0)
        perspective_shifted = all.copy()
        perspective_shifted.apply_function(perspective_shift)
        all.save_state()
        self.play(Transform(all,perspective_shifted))
        matching = get_matching(
            Group(*pears.submobjects[:-1]),
            Group(*apples.submobjects[:-1]),
        )
        self.play(ShowCreation(matching))
        self.dither()
        one_extra_apple = get_matching(
            Group(*pears.submobjects[:-1]),
            Group(*apples.submobjects[1:]),
        )
        self.play(Transform(matching,one_extra_apple))
        self.dither()
        one_extra_pear = get_matching(
            Group(*pears.submobjects[1:]),
            Group(*apples.submobjects[:-1]),
        )
        self.play(Transform(matching,one_extra_pear))
        self.dither()

        apple_def_box = SurroundingRectangle(apples, color=RED)
        apple_label = TexMobject("A",fill_color=RED).next_to(apple_def_box,direction=LEFT)
        self.play(
            FadeOut(apple_numbers),
            FadeOut(pear_numbers),
            ShowCreation(apple_def_box),
            Write(apple_label)
        )
        self.dither()
        pear_def_box = SurroundingRectangle(pears,color=YELLOW)
        pear_label = TexMobject("B",fill_color=YELLOW).next_to(pear_def_box,direction=LEFT)
        self.play(
            Uncreate(apple_def_box),
            ShowCreation(pear_def_box),
            Write(pear_label)
        )
        self.dither()
        bijection = get_matching(
            Group(*pears.submobjects[:-1]),
            Group(*apples.submobjects[:-1]),
        )
        self.play(Uncreate(pear_def_box))
        self.play(Transform(matching,bijection))
        self.dither()
        equality = TexMobject("\\lvert{}","A","{}\\rvert=\\lvert{}","B","{}\\rvert").next_to(apples,direction=UP)
        apple_label_copy = apple_label.copy()
        pear_label_copy = pear_label.copy()
        def transform_to_equality(equality):
            self.play(
                Transform(apple_label,apple_label.copy().replace(equality.get_part_by_tex("A"))),
                Transform(pear_label,pear_label.copy().replace(equality.get_part_by_tex("B"))),
                Write(equality.get_parts_by_tex("vert"))
            )
        transform_to_equality(equality)
        self.dither()
        self.play(
            Transform(apple_label,apple_label_copy),
            Transform(pear_label,pear_label_copy),
            Transform(apples,apples.saved_state),
            Transform(pears,pears.saved_state),
            Uncreate(equality.get_parts_by_tex("vert")),
            Uncreate(matching)
        )
        self.play(
            FadeOut(Group(*pears.submobjects[4:])),
        )
        pears.remove(*pears.submobjects[4:])
        def center_x(mobj):
            return mobj.copy().shift((-mobj.get_center()[0],0,0))
        self.play(
            Transform(pears,center_x(pears))
        )
        def attempt(*apple_indices):
            matching = get_matching(
                pears,
                Group(*(apples.submobjects[i] for i in apple_indices))
            )
            self.play(ShowCreation(matching))
            self.play(Uncreate(matching))

        attempt(0,1,2,3)
        attempt(0,2,4,6)
        attempt(1,3,0,6)
        inequality = TexMobject("\\lvert{}","A","{}\\rvert>\\lvert{}","B","{}\\rvert").center().to_edge(UP)
        transform_to_equality(inequality)
        self.dither()
