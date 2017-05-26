from mobject import Group
from topics.geometry import Line
from constants import *

def line(from_,to):
    buff = (0,0.1,0)
    return Line(
        from_.get_critical_point(DOWN)-buff,
        to.get_critical_point(UP)+buff
    )

def get_matching(source,target):
    return Group(*(
        line(x,y) for (x,y) in
        zip(source.submobjects,target.submobjects)
    ))
