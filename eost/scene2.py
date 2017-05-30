from scene import Scene
from mobject.tex_mobject import *
from topics.geometry import *
from constants import *
from mobject import Mobject, Group
from .widgets import *
from animation.simple_animations import *
from animation.transform import *
from .matching import get_matching
import deterministic

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
