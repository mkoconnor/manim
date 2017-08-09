from scene import Scene
from topics.runners import *
from animation.transform import Transform

class RunnerTest(Scene):
    def construct(self):
        phase0 = RabbitPic(0)
        phase1 = RabbitPic(1)
        runner = phase0.copy()
        self.play(Transform(runner, phase1), run_time = 0.8)
        self.play(Transform(runner, phase0), run_time = 0.8)
        self.dither()
