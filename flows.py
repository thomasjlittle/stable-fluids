import numpy as np


class Flow:
    def __init__(
        self,
        point: np.array,
        normal: np.array,
        visible: bool = True,
        inflow_velocity=0.5,
        inflow_radius=4,
        inflow_start=0,
        inflow_duration=100,
    ):
        self.point = point
        self.normal = normal
        self.visible = visible
        self.inflow_velocity = inflow_velocity
        self.inflow_radius = inflow_radius
        self.inflow_start = inflow_start
        self.inflow_duration = inflow_duration
