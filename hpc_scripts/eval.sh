world-model-eval-openvla \
  --root-dir /gpfs/scratch/sy3535/code/world-model-eval/bridge_tasks \
  --checkpoint-path /gpfs/scratch/sy3535/code/world-model-eval/outputs/20260125_153536/ckpt_000040000.pt \
  --model-name openvla-7b \
  --save-video --video-out-dir ./rollouts/openvla

# export BRIDGE_V2_PATH="/gpfs/scratch/sy3535/data/bridge_dataset/tfds/bridge_dataset/1.0.0"
# export CONVERTED_DIR="/gpfs/scratch/sy3535/converted_datasets"
# export SUBSET_NAMES="bridge_v2"
# export INPUT_H=128
# export INPUT_W=128
# export N_FRAMES=6
# export FRAME_SKIP=1
# export ACTION_DIM=10
# export BATCH_SIZE=1
# export NUM_WORKERS=4

# MAX_TRAIN_STEPS=$(
# python - <<'PY'
# import math, os
# from pathlib import Path
# from world_model_eval.dataset import OpenXMP4VideoDataset
# ds = OpenXMP4VideoDataset(
#     save_dir=Path(os.environ["CONVERTED_DIR"]),
#     input_h=int(os.environ["INPUT_H"]),
#     input_w=int(os.environ["INPUT_W"]),
#     n_frames=int(os.environ["N_FRAMES"]),
#     frame_skip=int(os.environ["FRAME_SKIP"]),
#     action_dim=int(os.environ["ACTION_DIM"]),
#     subset_names=os.environ["SUBSET_NAMES"],
#     split="train",
# )
# print(math.ceil(len(ds) / int(os.environ["BATCH_SIZE"])))
# PY
# )

# torchrun --nproc_per_node=1 -m world_model_eval.train \
#   --dataset_dir "$CONVERTED_DIR" \
#   --subset_names "$SUBSET_NAMES" \
#   --input_h "$INPUT_H" --input_w "$INPUT_W" \
#   --n_frames "$N_FRAMES" --frame_skip "$FRAME_SKIP" \
#   --action_dim "$ACTION_DIM" --batch_size "$BATCH_SIZE" \
#   --num_workers "$NUM_WORKERS" \
#   --max_train_steps "$MAX_TRAIN_STEPS"

