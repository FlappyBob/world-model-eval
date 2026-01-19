# WorldGym 环境配置说明

## 当前环境概览

- **环境名称**: `worldgym`
- **Python 版本**: 3.10.19
- **位置**: `/venv/worldgym`
- **支持的模型**: OpenVLA, SpatialVLA, Octo

## 已安装的核心依赖

### 基础包
```
world-model-eval==0.1.0 (editable mode)
torch==2.11.0.dev (CUDA 12.8)
torchvision==0.25.0.dev
diffusers==0.35.1
accelerate==1.12.0
```

### OpenVLA & SpatialVLA
```
transformers==4.49.0
timm==0.9.10
scipy==1.15.3
```

### Octo
```
jax==0.4.29 (with CUDA 12 support)
jaxlib==0.4.29
flax==0.8.4
tensorflow==2.19.1
chex==0.1.85
optax==0.1.5
gym==0.26.2
wandb==0.24.0
octo==0.0.0 (from GitHub)
```

### 其他工具
```
numpy==1.26.4
pillow==11.3.0
opencv-python==4.11.0.86
matplotlib==3.10.6
imageio==2.37.0
```

---

## 使用方法

### 激活环境
使用以下任一方式激活环境：
```bash
# 方式 1: 使用 conda (如果已配置)
conda activate worldgym

# 方式 2: 直接使用 Python 解释器路径
/venv/worldgym/bin/python your_script.py

# 方式 3: 直接使用 pip 路径
/venv/worldgym/bin/pip install <package>
```

### 完成 Octo 的额外配置步骤

根据 README 说明，Octo 还需要两个额外步骤：

1. **安装 dlimp 库**:
   ```bash
   /venv/worldgym/bin/pip install git+https://github.com/kvablack/dlimp@5edaa4691567873d495633f2708982b42edf1972 --no-deps
   ```

2. **修改 Octo 的 typing.py 文件**:
   ```bash
   # 找到 Octo 的安装位置
   OCTO_PATH=$(/venv/worldgym/bin/python -c "import octo; import os; print(os.path.dirname(octo.__file__))")

   # 编辑 typing.py 文件，添加以下行：
   # PRNGKey = jax.random.PRNGKey
   ```

   或手动编辑 `/venv/worldgym/lib/python3.10/site-packages/octo/utils/typing.py`

---

## 运行评估任务

### 下载世界模型检查点
```bash
/venv/worldgym/bin/pip install gdown
/venv/worldgym/bin/gdown 1uiRP2BuavapMsyP9Cbr25mi_ymk9SEJb
```

这将下载约 9GB 的检查点文件：`mixed_openx_9robots_20frames_0p1actiondropout_580ksteps.pt`

### OpenVLA 评估
```bash
/venv/worldgym/bin/world-model-eval-openvla \
  --root-dir /path/to/tasks \
  --checkpoint-path ~/checkpoints/world-model/mixed_openx_9robots_20frames_0p1actiondropout_580ksteps.pt \
  --model-name openvla-7b \
  --save-video --video-out-dir ./rollouts/openvla
```

### SpatialVLA 评估
```bash
/venv/worldgym/bin/world-model-eval-spatialvla \
  --root-dir /path/to/tasks \
  --checkpoint-path ~/checkpoints/world-model/mixed_openx_9robots_20frames_0p1actiondropout_580ksteps.pt \
  --model-name spatialvla-4b-224-pt
```

### Octo 评估
```bash
/venv/worldgym/bin/world-model-eval-octo \
  --root-dir /path/to/tasks \
  --checkpoint-path ~/checkpoints/world-model/mixed_openx_9robots_20frames_0p1actiondropout_580ksteps.pt \
  --model-name octo-base-1.5
```

---

## 依赖冲突说明

### ⚠️ 关于 RT-1 模型

当前环境**不支持** RT-1 模型，原因是依赖冲突：
- **Octo** 需要 `jax==0.4.29`
- **RT-1** 需要 `jax==0.6.2`

这两个版本无法在同一环境中共存。

#### 如果需要使用 RT-1：

**选项 1: 创建单独的 RT-1 环境**（推荐）
```bash
conda create -n worldgym-rt1 python=3.10
conda activate worldgym-rt1
cd /workspace/world-model-eval
pip install -e .[rt1]
```

**选项 2: 在当前环境切换到 RT-1**（会移除 Octo）
```bash
/venv/worldgym/bin/pip uninstall jax jaxlib octo -y
/venv/worldgym/bin/pip install "jax[cuda12]==0.6.2" flax==0.10.2 tensorflow-hub==0.16.1
```

### Transformers 版本说明

虽然 `pyproject.toml` 中：
- `spatialvla` 指定 `transformers==4.48.1`
- `openvla` 指定 `transformers==4.49.0`

当前环境使用了 **`transformers==4.49.0`**（较新版本），这个版本应该向后兼容 4.48.1，可以同时支持两个模型。

---

## 验证安装

运行以下命令验证关键包是否正确安装：

```bash
/venv/worldgym/bin/python -c "
import world_model_eval
import torch
import transformers
import jax
import flax
import octo
print('✅ All core packages imported successfully!')
print(f'PyTorch: {torch.__version__}')
print(f'Transformers: {transformers.__version__}')
print(f'JAX: {jax.__version__}')
print(f'Flax: {flax.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
"
```

---

## 训练模型

### 快速开始（使用示例数据）
```bash
# 使用 N 个 GPU 进行训练
/venv/worldgym/bin/torchrun --nproc_per_node=N -m world_model_eval.train
```

### 在 Open X-Embodiment 数据集上训练

1. **安装 TensorFlow 相关依赖**:
   ```bash
   /venv/worldgym/bin/pip install tensorflow tensorflow_datasets
   ```

2. **下载数据集**:
   ```bash
   # 下载 RT-1 数据集
   /venv/worldgym/bin/python -m world_model_eval.download_data --dataset_name rt_1

   # 或指定输出目录
   /venv/worldgym/bin/python -m world_model_eval.download_data \
     --dataset_name rt_1 \
     --output_dir /path/to/output
   ```

3. **启动训练**:
   ```bash
   /venv/worldgym/bin/torchrun --nproc_per_node=N \
     -m world_model_eval.train \
     --dataset_dir ./converted_datasets \
     --subset_names rt_1
   ```

---

## 故障排除

### 问题：找不到 `world-model-eval-*` 命令
确保使用完整路径或激活环境：
```bash
/venv/worldgym/bin/world-model-eval-openvla --help
```

### 问题：CUDA 内存不足
- 减少 batch size
- 使用较小的模型
- 启用梯度检查点

### 问题：Octo 导入错误
确保完成了 Octo 的额外配置步骤（dlimp 安装和 typing.py 修改）

---

## 环境维护

### 查看已安装的包
```bash
/venv/worldgym/bin/pip list
```

### 更新某个包
```bash
/venv/worldgym/bin/pip install --upgrade <package-name>
```

### 冻结当前环境依赖
```bash
/venv/worldgym/bin/pip freeze > requirements_frozen.txt
```

---

## 相关链接

- [项目主页](https://world-model-eval.github.io/abstract)
- [论文](https://arxiv.org/abs/2506.00613)
- [GitHub 仓库](https://github.com/world-model-eval/world-model-eval)
- [世界模型检查点下载](https://drive.google.com/file/d/1uiRP2BuavapMsyP9Cbr25mi_ymk9SEJb/view?usp=sharing)

---

**最后更新**: 2026-01-19
