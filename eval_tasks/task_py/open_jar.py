from typing import List, Tuple
from rlbench.backend.task import Task
from typing import List
from rlbench.backend.task import Task
from rlbench.const import colors
from rlbench.backend.conditions import DetectedCondition
from rlbench.backend.spawn_boundary import SpawnBoundary
import numpy as np
from pyrep.objects.shape import Shape
from pyrep.objects.proximity_sensor import ProximitySensor
from pyrep.objects.dummy import Dummy


class OpenJar(Task):
    def init_task(self) -> None:
        self._lid = Shape("jar_lid")
        self._jar = Shape("jar")
        self._success = ProximitySensor("success")
        self.register_graspable_objects([self._lid])
        self.boundary = Shape("spawn_boundary")
        self._spawn_boundary = SpawnBoundary([self.boundary])
        self.register_success_conditions(
            [DetectedCondition(self._lid, self._success, negated=True)]
        )

    def init_episode(self, index: int) -> List[str]:
        self._spawn_boundary.clear()
        self._spawn_boundary.sample(self._jar, min_distance=0.01)

        w0 = Dummy("waypoint0")
        w0.set_orientation([-np.pi, 0, -np.pi], reset_dynamics=False)
        w0.set_position(
            [0, 0, 0.1], relative_to=self._lid, reset_dynamics=False
        )
        target_color_name, target_color_rgb = colors[index]
        self._jar.set_color(target_color_rgb)
        return [
            "open the %s jar" % target_color_name,
            "unscrew the %s jar" % target_color_name,
            (
                "grasp the lid of the %s jar, unscrew it in an anti_clockwise "
                + "direction until it is removed from the jar, and leave it on "
                + "the table top"
            )
            % target_color_name,
            "remove the lid from the %s jam jar and set it down on the table"
            % target_color_name,
        ]

    def variation_count(self) -> int:
        return len(colors)

    def base_rotation_bounds(
        self,
    ) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
        # This is here to stop the issue of gripper rotation joint reaching its
        # limit and not being able to go through the full range of rotation to
        # unscrew, leading to a weird jitery and tilted cap while unscrewing.
        # Issue occured rarely so is only minor
        return (0.0, 0.0, -0.6 * np.pi), (0.0, 0.0, +0.6 * np.pi)
