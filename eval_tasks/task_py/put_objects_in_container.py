from typing import List

from pyrep.objects.proximity_sensor import ProximitySensor
from pyrep.objects.shape import Shape

from rlbench.backend.conditions import DetectedCondition
from rlbench.backend.task import Task


class PutObjectsInContainer(Task):

    def init_task(self) -> None:
        # self._rubik_cube = Shape("rubiks_cube")
        # self._tomato_soup_can = Shape("tomato_soup_can")
        self._mustard_bottle = Shape("mustard_bottle")
        self._container_detector = ProximitySensor("container_detector")

        self.register_graspable_objects(
            [self._mustard_bottle]
        )

        self.register_success_conditions(
            [
                DetectedCondition(self._mustard_bottle, self._container_detector),
             
            ]
        )

    def init_episode(self, index: int) -> List[str]:
        # TODO: This is called at the start of each episode.
        return [""]

    def variation_count(self) -> int:
        # TODO: The number of variations for this task.
        return 1
