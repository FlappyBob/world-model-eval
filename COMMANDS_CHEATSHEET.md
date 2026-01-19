# 命令速查表

## 🎯 一键运行评估

### 完整流程（推荐新手）

```bash
cd /workspace/world-model-eval

# 1. 安装 gdown（如果需要）
/venv/worldgym/bin/pip install gdown

# 2. 下载检查点（约 9GB）
/venv/worldgym/bin/gdown 1uiRP2BuavapMsyP9Cbr25mi_ymk9SEJb

# 3. 创建输出目录
mkdir -p ~/checkpoints/world-model
mv mixed_openx_9robots_20frames_0p1actiondropout_580ksteps.pt ~/checkpoints/world-model/

# 4. 运行 OpenVLA 评估（最简单）
/venv/worldgym/bin/world-model-eval-openvla \
  --root-dir /workspace/world-model-eval/bridge_tasks \
  --checkpoint-path ~/checkpoints/world-model/mixed_openx_9robots_20frames_0p1actiondropout_580ksteps.pt \
  --model-name openvla-7b \
  --save-video --video-out-dir ./rollouts/openvla
```

---

## 📥 数据准备命令

### 验证现有 Bridge V2 数据

```bash
/venv/worldgym/bin/python prepare_tasks.py validate bridge_tasks
```

### 查看数据统计

```bash
# 试验数量
ls bridge_tasks/put_carrot_on_plate/*.png | wc -l

# 数据大小
du -sh bridge_tasks

# 查看示例
cat bridge_tasks/put_carrot_on_plate/trial_001.json
```

### 下载更多 Bridge V2 数据（可选）

```bash
# 如果有其他任务的 JSON 文件
/venv/worldgym/bin/python prepare_bridge_data.py ./bridge_tasks_more

# 限制下载数量（测试用）
/venv/worldgym/bin/python prepare_bridge_data.py ./bridge_tasks_test 5
```

---

## 🚀 运行评估命令

### OpenVLA（7B 参数，推荐）

```bash
/venv/worldgym/bin/world-model-eval-openvla \
  --root-dir /workspace/world-model-eval/bridge_tasks \
  --checkpoint-path ~/checkpoints/world-model/mixed_openx_9robots_20frames_0p1actiondropout_580ksteps.pt \
  --model-name openvla-7b \
  --save-video --video-out-dir ./rollouts/openvla
```

### SpatialVLA（4B 参数，更快）

```bash
/venv/worldgym/bin/world-model-eval-spatialvla \
  --root-dir /workspace/world-model-eval/bridge_tasks \
  --checkpoint-path ~/checkpoints/world-model/mixed_openx_9robots_20frames_0p1actiondropout_580ksteps.pt \
  --model-name spatialvla-4b-224-pt \
  --save-video --video-out-dir ./rollouts/spatialvla
```

### Octo（需先完成配置）

**首次使用前配置 Octo：**

```bash
# 安装 dlimp
/venv/worldgym/bin/pip install git+https://github.com/kvablack/dlimp@5edaa4691567873d495633f2708982b42edf1972 --no-deps

# 修改 typing.py
echo "PRNGKey = jax.random.PRNGKey" >> /venv/worldgym/lib/python3.10/site-packages/octo/utils/typing.py
```

**运行评估：**

```bash
/venv/worldgym/bin/world-model-eval-octo \
  --root-dir /workspace/world-model-eval/bridge_tasks \
  --checkpoint-path ~/checkpoints/world-model/mixed_openx_9robots_20frames_0p1actiondropout_580ksteps.pt \
  --model-name octo-base-1.5 \
  --save-video --video-out-dir ./rollouts/octo
```

---

## 🔧 环境管理命令

### 验证环境

```bash
/venv/worldgym/bin/python verify_env.py
```

### 检查已安装的包

```bash
/venv/worldgym/bin/pip list | grep -E "(world-model|transformers|jax|octo)"
```

### 查看系统资源

```bash
# 磁盘空间
df -h /workspace

# 内存使用
free -h

# GPU 状态
nvidia-smi
```

---

## 📊 结果查看命令

### 查看生成的视频

```bash
# 列出所有视频
ls -lh rollouts/openvla/*.mp4

# 视频数量
ls rollouts/openvla/*.mp4 | wc -l

# 播放视频（如果有播放器）
vlc rollouts/openvla/video_001.mp4
```

### 查看评估日志

```bash
# 查看最近的日志（根据实际输出位置）
tail -100 evaluation.log

# 或直接查看控制台输出
```

---

## 🛠️ 工具脚本命令

### 创建示例任务数据

```bash
# 创建测试用的示例数据
/venv/worldgym/bin/python prepare_tasks.py create ./my_example_tasks

# 从现有图片创建任务
/venv/worldgym/bin/python prepare_tasks.py from-images \
  /path/to/images \
  ./my_tasks \
  task_name \
  "complete the task"
```

### 验证任务数据格式

```bash
/venv/worldgym/bin/python prepare_tasks.py validate /path/to/tasks
```

---

## 🔍 调试命令

### 检查 Python 路径

```bash
/venv/worldgym/bin/python -c "import sys; print('\n'.join(sys.path))"
```

### 测试导入

```bash
/venv/worldgym/bin/python -c "
import world_model_eval
import torch
import transformers
import jax
print('All imports successful!')
print(f'PyTorch: {torch.__version__}')
print(f'JAX: {jax.__version__}')
print(f'CUDA: {torch.cuda.is_available()}')
"
```

### 检查 Octo 配置

```bash
# 验证 dlimp 安装
/venv/worldgym/bin/python -c "import dlimp; print('dlimp OK')"

# 验证 typing.py 修改
tail -1 /venv/worldgym/lib/python3.10/site-packages/octo/utils/typing.py
# 应该显示: PRNGKey = jax.random.PRNGKey
```

### 清理 GPU 内存

```bash
# 如果评估卡住，清理 GPU
nvidia-smi

# 杀掉占用 GPU 的进程（小心使用）
# kill -9 <PID>
```

---

## 📁 常用路径

```bash
# 环境路径
ENV_PATH="/venv/worldgym"

# Python 解释器
PYTHON="$ENV_PATH/bin/python"

# 数据目录
BRIDGE_TASKS="/workspace/world-model-eval/bridge_tasks"

# 检查点路径
CHECKPOINT="$HOME/checkpoints/world-model/mixed_openx_9robots_20frames_0p1actiondropout_580ksteps.pt"

# 使用示例
$PYTHON verify_env.py
```

---

## ⚡ 快捷方式

### 设置别名（可选）

在 `~/.bashrc` 中添加：

```bash
alias wgpython='/venv/worldgym/bin/python'
alias wgpip='/venv/worldgym/bin/pip'
alias wg-openvla='/venv/worldgym/bin/world-model-eval-openvla'
alias wg-spatialvla='/venv/worldgym/bin/world-model-eval-spatialvla'
alias wg-octo='/venv/worldgym/bin/world-model-eval-octo'
```

然后：

```bash
source ~/.bashrc

# 现在可以使用短命令
wgpython verify_env.py
wg-openvla --root-dir bridge_tasks --checkpoint-path ...
```

---

## 📖 帮助命令

### 查看命令行选项

```bash
# OpenVLA 选项
/venv/worldgym/bin/world-model-eval-openvla --help

# SpatialVLA 选项
/venv/worldgym/bin/world-model-eval-spatialvla --help

# Octo 选项
/venv/worldgym/bin/world-model-eval-octo --help
```

### 查看工具脚本帮助

```bash
/venv/worldgym/bin/python prepare_tasks.py --help
/venv/worldgym/bin/python prepare_bridge_data.py --help
```

---

## 🎓 完整示例

### 从头到尾运行 OpenVLA 评估

```bash
#!/bin/bash

# 进入项目目录
cd /workspace/world-model-eval

# 设置变量
PYTHON="/venv/worldgym/bin/python"
CHECKPOINT_DIR="$HOME/checkpoints/world-model"
CHECKPOINT_FILE="mixed_openx_9robots_20frames_0p1actiondropout_580ksteps.pt"

# 1. 验证环境
echo "验证环境..."
$PYTHON verify_env.py

# 2. 下载检查点（如果不存在）
if [ ! -f "$CHECKPOINT_DIR/$CHECKPOINT_FILE" ]; then
    echo "下载检查点..."
    /venv/worldgym/bin/pip install gdown
    /venv/worldgym/bin/gdown 1uiRP2BuavapMsyP9Cbr25mi_ymk9SEJb
    mkdir -p "$CHECKPOINT_DIR"
    mv "$CHECKPOINT_FILE" "$CHECKPOINT_DIR/"
fi

# 3. 验证数据
echo "验证数据..."
$PYTHON prepare_tasks.py validate bridge_tasks

# 4. 运行评估
echo "运行评估..."
/venv/worldgym/bin/world-model-eval-openvla \
  --root-dir bridge_tasks \
  --checkpoint-path "$CHECKPOINT_DIR/$CHECKPOINT_FILE" \
  --model-name openvla-7b \
  --save-video --video-out-dir ./rollouts/openvla

echo "完成！查看 ./rollouts/openvla/ 获取结果"
```

保存为 `run_evaluation.sh`，然后：

```bash
chmod +x run_evaluation.sh
./run_evaluation.sh
```

---

**提示**: 复制粘贴这些命令到终端即可使用！
