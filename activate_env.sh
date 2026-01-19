#!/bin/bash
# WorldGym 环境激活脚本

# 设置环境变量
export WORLDGYM_ENV=/venv/worldgym
export PATH=$WORLDGYM_ENV/bin:$PATH
export PYTHONPATH=/workspace/world-model-eval:$PYTHONPATH

# 显示环境信息
echo "======================================"
echo "  WorldGym Environment Activated"
echo "======================================"
echo "Python: $WORLDGYM_ENV/bin/python"
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
