cd /gpfs/scratch/sy3535/code/world-model-eval

export BRIDGE_V2_PATH="/gpfs/scratch/sy3535/data/bridge_dataset/tfds/bridge_dataset/1.0.0"
export CONVERTED_DIR="/gpfs/scratch/sy3535/converted_datasets"

rm -rf "$CONVERTED_DIR/bridge_v2"
if [ ! -d "$CONVERTED_DIR/bridge_v2/train" ]; then
  python -m world_model_eval.download_data --dataset_name bridge_v2 --output_dir "$CONVERTED_DIR"
fi