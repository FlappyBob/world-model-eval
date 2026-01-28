#!/bin/bash
# WorldGym 环境激活脚本（conda）

module load anaconda

# 激活 conda 环境
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate worldgym

# 设置项目路径
export PYTHONPATH=/gpfs/scratch/sy3535/code/world-model-eval:$PYTHONPATH
# Prefer conda toolchain libs over system ones.
export LD_LIBRARY_PATH="$CONDA_PREFIX/lib:$LD_LIBRARY_PATH"

# 显示环境信息
echo "======================================"
echo "  WorldGym Environment Activated"
echo "======================================"
echo "Python: $(which python)"
echo "Location: $(pwd)"
echo ""
echo "Available commands:"
echo "  - world-model-eval-openvla"
echo "  - world-model-eval-spatialvla"
echo "  - world-model-eval-octo"
echo ""
echo "To verify installation, run:"
echo "  python verify_env.py"
echo "======================================"
