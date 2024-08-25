from typing import List
import numpy as np
from pyrep.objects.shape import Shape
from pyrep.objects.dummy import Dummy
from pyrep.objects.proximity_sensor import ProximitySensor
from rlbench.backend.task import Task
from rlbench.backend.conditions import DetectedCondition, ConditionSet, \
    GraspedCondition
from rlbench.backend.spawn_boundary import SpawnBoundary
from rlbench.const import colors


class PickAndLift(Task):


    def init_task(self) -> None:
        self.target_block = Shape('pick_and_lift_target')
        self.distractors = [
            Shape('stack_blocks_distractor%d' % i)
            for i in range(2)]
        self.register_graspable_objects([self.target_block])
        self.boundary = SpawnBoundary([Shape('pick_and_lift_boundary')])
        self.success_detector = ProximitySensor('pick_and_lift_success')
        self._target = ProximitySensor('success')
        self._waypoint_end = Dummy("waypoint3")

        # cond_set = ConditionSet([
        #     DetectedCondition(self.target_block, self.success_detector)
        # ])
        # self.register_success_conditions([cond_set])
        self.register_success_conditions([
            DetectedCondition(self.target_block, self._target, negated=True)
        ])
    
    def init_episode(self, index: int) -> List[str]:

        block_color_name, block_rgb = colors[index]
        self.target_block.set_color(block_rgb)

        color_choices = np.random.choice(
            list(range(index)) + list(range(index + 1, len(colors))),
            size=2, replace=False)
        for i, ob in enumerate(self.distractors):
            name, rgb = colors[color_choices[int(i)]]
            ob.set_color(rgb)

        self.boundary.clear()
        self.boundary.sample(self._target, min_distance=0.1)
        self.boundary.sample(
            self.success_detector, min_rotation=(0.0, 0.0, 0.0),
            max_rotation=(0.0, 0.0, 0.0))
        for block in [self.target_block] + self.distractors:
            self.boundary.sample(block, min_distance=0.1)
        target_pos = self.target_block.get_position()
        waypoint_pos = self._waypoint_end.get_position()
        waypoint_pos[0], waypoint_pos[1] = target_pos[0], target_pos[1]
        self._waypoint_end.set_position(waypoint_pos)
        self._waypoint_end.set_orientation(self.target_block.get_orientation())

        return ['pick up the %s block and lift it up to the target' %
                block_color_name,
                'grasp the %s block to the target' % block_color_name,
                'lift the %s block up to the target' % block_color_name]

    def variation_count(self) -> int:
        return 1
