from topics.geometry import Line
from constants import *
from animation.simple_animations import *
from animation.transform import *
from mobject.vectorized_mobject import VMobject, VGroup

def line(from_,to):
    buff = 0.1
    return Line(
        from_.get_critical_point(UP)+UP*buff,
        to.get_critical_point(DOWN)+DOWN*buff
    )

def get_matching(source,target):
    return VGroup(*(
        line(x,y) for (x,y) in
        zip(source.submobjects,target.submobjects)
    ))

class MatchingAnimations:
    def __init__(self,source,target):
        matching_line = Line(0.5*DOWN, 0.5*UP)
        def matched_objects(source,target):
            matched = VGroup(source.copy(),matching_line.copy(),target.copy())
            matched.arrange_submobjects(direction=DOWN)
            return matched
        final_mobj = VGroup(*(
            matched_objects(s,t)
            for (s,t) in zip(source.submobjects,target.submobjects)
        ))
        self.buff = 2*DEFAULT_MOBJECT_TO_MOBJECT_BUFFER
        final_mobj.arrange_submobjects(buff=self.buff)
        final_mobj.center()
        def match_animation(source,target,matched):
            return AnimationGroup(
                Transform(source,matched.submobjects[0]),
                ShowCreation(matched.submobjects[1]),
                Transform(target,matched.submobjects[2])
            )
        self.match_animations = [
            match_animation(s,t,m)
            for (s,t,m) in zip(
                    source.submobjects,
                    target.submobjects,
                    final_mobj.submobjects
            )
        ]
        self.matching = VGroup(*[mob[1] for mob in final_mobj])
        #self.remove_match_animation = AnimationGroup(*(
        #    Uncreate(mobj.submobjects[1]) for mobj in final_mobj.submobjects
        #))
