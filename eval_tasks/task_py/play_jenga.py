from typing import List, Tuple
import numpy as np
from pyrep.objects.proximity_sensor import ProximitySensor
from pyrep.objects.shape import Shape
from rlbench.backend.conditions import DetectedCondition, NothingGrasped
from rlbench.backend.task import Task


class PlayJenga(Task):

    def init_task(self) -> None:


        self._block = Shape('target_cuboid')
        self._target = ProximitySensor('success')
        self.register_graspable_objects([self._block])
        self.register_success_conditions([
            DetectedCondition(self._block, self._target)])

    def init_episode(self, index: int) -> List[str]:
        return ['play jenga'
                'Take the protruding block out of the jenga tower without the '
                'tower toppling',
                'Keeping the tower from tumbling, remove the protruding '
                'jenga block',
                'Ensuring the jenga tower remains in place, slide the '
                'protruding block out']

    def variation_count(self) -> int:
        return 1

    def base_rotation_bounds(self) -> Tuple[List[float], List[float]]:
        return [0, 0, -np.pi / 8], [0, 0, np.pi / 8]