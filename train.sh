cd /gpfs/scratch/sy3535/code/world-model-eval

export BRIDGE_V2_PATH="/gpfs/scratch/sy3535/data/bridge_dataset/tfds/bridge_dataset/1.0.0"
export CONVERTED_DIR="/gpfs/scratch/sy3535/converted_datasets"

if [ ! -d "$CONVERTED_DIR/bridge_v2/train" ]; then
  python -m world_model_eval.download_data --dataset_name bridge_v2 --output_dir "$CONVERTED_DIR"
fi

export INPUT_H=256
export INPUT_W=256
export N_FRAMES=10
export FRAME_SKIP=1
export SUBSET_NAMES="bridge_v2"
export ACTION_DIM=10
# Use train.py defaults for training hyperparameters unless you need to override.
export BATCH_SIZE=8
export NUM_WORKERS=32

# 计算 1 个 epoch 的 step 数
MAX_TRAIN_STEPS=125_000

echo "Max train steps : ${MAX_TRAIN_STEPS}"

torchrun --nproc_per_node=2 -m world_model_eval.train \
  --dataset_dir "$CONVERTED_DIR" \
  --subset_names "$SUBSET_NAMES" \
  --input_h "$INPUT_H" \
  --input_w "$INPUT_W" \
  --n_frames "$N_FRAMES" \
  --frame_skip "$FRAME_SKIP" \
  --action_dim "$ACTION_DIM" \
  --batch_size "$BATCH_SIZE" \
  --num_workers "$NUM_WORKERS" \
  --max_train_steps "$MAX_TRAIN_STEPS"
