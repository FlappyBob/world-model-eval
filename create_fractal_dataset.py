import os, re
import numpy as np
import tensorflow as tf
from tqdm import tqdm
import tensorflow_datasets as tfds

OUT_ROOT = "/vast/as20482/data/fractal/processed"

def sanitize(instr_tensor):
    text = instr_tensor.numpy().decode("utf-8").strip().lower()
    text = text.replace(" ", "_")
    text = re.sub(r"[^a-z_]", "", text)
    if not text:
        text = "unknown"
    return text

def pick_first_available_image(step):
    return step["observation"]["image"]

def extract_state(obs):
    """Flatten some key obs fields into a single vector."""
    parts = [
        obs["base_pose_tool_reached"].numpy(),
        obs["gripper_closed"].numpy(),
        obs["height_to_bottom"].numpy(),
        obs["vector_to_go"].numpy(),
    ]
    return np.concatenate(parts, axis=0)

def extract_first(ep, eid):
    first_step = next(iter(ep["steps"]))

    instr = first_step["observation"]["natural_language_instruction"]
    instr_key = sanitize(instr)

    img = pick_first_available_image(first_step).numpy()  # uint8 HWC
    # state = extract_state(first_step["observation"])

    return instr_key, eid, img#, state

def save_sample(instr_key, eid, img):#, state):
    d = os.path.join(OUT_ROOT, instr_key)
    os.makedirs(d, exist_ok=True)
    stem = f"ep{eid:08d}"

    # Save PNG
    png = tf.io.encode_png(img)
    tf.io.write_file(os.path.join(d, stem + ".png"), png)

    # Save state
    # np.save(os.path.join(d, stem + ".state.npy"), state)

def export_by_instruction(ds, limit=None):
    os.makedirs(OUT_ROOT, exist_ok=True)
    counts = {}
    n = 0
    for eid, ep in enumerate(tqdm(ds)):
        instr_key, eid, img = extract_first(ep, eid)
        save_sample(instr_key, eid, img)
        counts[instr_key] = counts.get(instr_key, 0) + 1
        n += 1
        if limit and n >= limit:
            break
    return counts

# point builder_dir to where you extracted fractal
ds_builder = tfds.builder_from_directory(
    builder_dir="/vast/as20482/tensorflow_datasets/fractal/0.1.0"
)
ds = ds_builder.as_dataset(split="train")
counts = export_by_instruction(ds)
print("Episodes per instruction:", counts)
