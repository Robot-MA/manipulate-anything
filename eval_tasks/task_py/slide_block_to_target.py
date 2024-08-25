from typing import List
from pyrep.objects.shape import Shape
from pyrep.objects.proximity_sensor import ProximitySensor
from rlbench.backend.task import Task
from rlbench.backend.conditions import DetectedCondition



class SlideBlockToTarget(Task):

    def init_task(self) -> None:
        self._block = Shape('block')
        self._target = ProximitySensor('success')
        self.register_graspable_objects([self._block])
        self.register_success_conditions([
            DetectedCondition(self._block, self._target)])
        # if (self.register_success_conditions([
        #     DetectedCondition(self._block, self._target)]) == True):
        #     print("SUCCEED!!!!!!!!!!!!")
        # else:
        #     print("Not yet")

    def init_episode(self, index: int) -> List[str]:
        self._variation_index = index
        return ['slide the block to target',
                'slide the block onto the target',
                'push the block until it is sitting on top of the target',
                'slide the block towards the green target',
                'cover the target with the block by pushing the block in its'
                ' direction']

    def variation_count(self) -> int:
        return 1
