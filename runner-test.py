from scene import Scene
from topics.runners import *
from topics.geometry import *
from animation.simple_animations import *
from animation.transform import Transform
from eost.ordinal import *

class RunnerTest(Scene):
    def construct(self):
        #phase_gen = TurtlePic
        #phase_gen = RabbitPic
        phase_gen = AchilesPic
        #phase_gen = AchilesStickmanPic
        phase0 = phase_gen(0)
        phase1 = phase_gen(1)
        runner = phase0.copy()
        self.play(
            #Transform(runner, phase1, rate_func = there_and_back),
            Transform(runner, phase1),
            #MoveAlongPath(runner, Line(ORIGIN, 0.5*RIGHT)),
            #run_time = 1.5,
        )
        self.play(Transform(runner, phase0))

class RunnerTest2(Scene):
    def construct(self):
        ordinal = OrdinalOmega()
        turtle = Runner(phase_gen = TurtlePic, pointer_pos = DOWN, color = YELLOW)
        rabbit = Runner(phase_gen = RabbitPic, pointer_pos = UP)
        achiles = Runner(phase_gen = AchilesPic, pointer_pos = UP)
        turtle.move_to(ordinal[0])
        #rabbit.move_to(ordinal[0])
        achiles.move_to(ordinal[0])
        self.add(ordinal)
        self.play(turtle.run_in())
        self.play(achiles.run_in())
        self.dither()
        ordinal2 = ordinal.copy().next_to(achiles, DOWN, coor_mask = UP)
        self.add(ordinal2)
        VGroup(*self.mobjects).to_edge(UP)
        self.dither()
