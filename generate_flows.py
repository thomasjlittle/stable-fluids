import numpy as np

from config import RESOLUTION
from flows import Flow


def generate_flows(
    flows: list[Flow], start: int = 0, duration: int = 200
) -> list[Flow]:
    n = 5
    for i in range(n + 1):
        variable_velocity = True if i % 2 == 1 else False
        flows.append(
            Flow(
                point=np.array([RESOLUTION[0] * 0.95, RESOLUTION[1] * i / n]),
                normal=np.array([0.35, 0.8]),
                visible=True,
                inflow_velocity=0.1,
                variable_velocity=variable_velocity,
                inflow_radius=8,
                inflow_start=start,
                inflow_duration=duration,
            )
        )

    return flows


def generate_clear_flows(
    flows: list[Flow], start: int = 0, duration: int = 200
) -> list[Flow]:
    n = 5
    for i in range(n + 1):
        flows.append(
            Flow(
                point=np.array([RESOLUTION[0] * 0.6, RESOLUTION[1] * i / n]),
                normal=np.array([0.3, 1]),
                inflow_radius=40,
                visible=False,
                inflow_velocity=0.1,
                inflow_start=400,
                inflow_duration=100,
            )
        )

    return flows
