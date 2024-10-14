import numpy as np
from PIL import Image
from scipy.special import erf

from flows import Flow
from fluid import Fluid

RESOLUTION = 140, 240
DURATION = 200

INFLOW_PADDING = RESOLUTION[0] * 0.1
INFLOW_DURATION = 50
INFLOW_RADIUS = 4
INFLOW_VELOCITY = 1
INFLOW_COUNT = 3

print("Generating fluid solver, this may take some time.")
fluid = Fluid(RESOLUTION, "dye")

# center = np.floor_divide(RESOLUTION, 2)
# r = np.min(center) - INFLOW_PADDING

# points = np.linspace(-np.pi, np.pi, INFLOW_COUNT, endpoint=False)
# points = tuple(np.array((np.cos(p), np.sin(p))) for p in points)
# normals = tuple(-p for p in points)
# points = tuple(r * p + center for p in points)


# normals = (
#     np.array([0.05, 1]),
#     np.array([-0.2, 1]),
#     np.array([0, -1]),
#     np.array([-1, -1]),
# )
# points = (
#     np.array([RESOLUTION[0] * 0.95, RESOLUTION[1] * 0.05]),
#     np.array([RESOLUTION[0] * 0.90, RESOLUTION[1] * 0.15]),
#     np.array([RESOLUTION[0] * 0.90, RESOLUTION[1] * 0.5]),
#     np.array([RESOLUTION[0] * 0.90, RESOLUTION[1] * 0.9]),
# )

# inflow_velocity = np.zeros_like(fluid.velocity)
# inflow_dye = np.zeros(fluid.shape)
# for p, n in zip(points, normals):
#     mask = np.linalg.norm(fluid.indices - p[:, None, None], axis=0) <= INFLOW_RADIUS
#     inflow_velocity[:, mask] += n[:, None] * INFLOW_VELOCITY
#     if all(p == np.array([RESOLUTION[0] * 0.90, RESOLUTION[1] * 0.5])):
#         inflow_dye[mask] = 0
#     else:
#         inflow_dye[mask] = 1

# Setup flows
flows = []
flows.append(
    Flow(
        point=np.array([RESOLUTION[0] * 0.95, RESOLUTION[1] * 0.05]),
        normal=np.array([0.05, 1]),
        inflow_start=0,
        inflow_duration=100,
    )
)
flows.append(
    Flow(
        point=np.array([RESOLUTION[0] * 0.90, RESOLUTION[1] * 0.15]),
        normal=np.array([-0.2, 1]),
        inflow_start=50,
        inflow_duration=100,
    )
)
flows.append(
    Flow(
        point=np.array([RESOLUTION[0] * 0.90, RESOLUTION[1] * 0.5]),
        normal=np.array([0, -1]),
        inflow_start=20,
        inflow_duration=80,
    )
)
flows.append(
    Flow(
        point=np.array([RESOLUTION[0] * 0.90, RESOLUTION[1] * 0.9]),
        normal=np.array([-1, -1]),
        inflow_velocity=1,
        inflow_radius=8,
        inflow_start=60,
        inflow_duration=50,
    )
)


# Run sim
def update_state(flows, fluid, step):
    for flow in flows:
        if flow.inflow_start <= step < flow.inflow_start + flow.inflow_duration:
            mask = (
                np.linalg.norm(fluid.indices - flow.point[:, None, None], axis=0)
                <= flow.inflow_radius
            )
            inflow_velocity[:, mask] = flow.normal[:, None] * flow.inflow_velocity
            if flow.visible:
                inflow_dye[mask] = 1

        else:
            mask = (
                np.linalg.norm(fluid.indices - flow.point[:, None, None], axis=0)
                <= flow.inflow_radius
            )
            inflow_velocity[:, mask] = flow.normal[:, None] * 0
            inflow_dye[mask] = 0

    return inflow_velocity, inflow_dye


inflow_velocity = np.zeros_like(fluid.velocity)
inflow_dye = np.zeros(fluid.shape)
inflow_velocity, inflow_dye = update_state(flows, fluid, 0)


frames = []
for f in range(DURATION):
    print(f"Computing frame {f + 1} of {DURATION}.")
    # if f == 100:
    inflow_velocity, inflow_dye = update_state(flows, fluid, f)
    # if f <= INFLOW_DURATION:
    fluid.velocity += inflow_velocity
    fluid.dye += inflow_dye

    curl = fluid.step()[1]
    # Using the error function to make the contrast a bit higher.
    # Any other sigmoid function e.g. smoothstep would work.
    curl = (erf(curl * 2) + 1) / 4

    # color = np.dstack((hue, saturation, value))
    color = np.dstack((curl, np.ones(fluid.shape), fluid.dye))

    color = (np.clip(color, 0, 1) * 255).astype("uint8")
    frames.append(Image.fromarray(color, mode="HSV").convert("RGB"))


def convert_to_bmp(frames):
    total_height = 32 * len(frames)
    concatenated_image = Image.new("RGB", (64, total_height))
    y_offset = 0

    for img in frames:
        downscaled_image = img.resize((64, 32), Image.LANCZOS)
        concatenated_image.paste(downscaled_image, (0, y_offset))
        y_offset += (
            downscaled_image.height
        )  # Move the y offset by the height of the current image
    concatenated_image.save("flow_v4.bmp")


def crop_frame(frame, border=20):
    crop_box = (border, border, RESOLUTION[1] - border, RESOLUTION[0] - border)
    return frame.crop(crop_box)


for i in range(len(frames)):
    frames[i] = crop_frame(frames[i], 0)

convert_to_bmp(frames)


print("Saving simulation result.")
frames[0].save(
    "example2.gif", save_all=True, append_images=frames[1:], duration=20, loop=0
)
