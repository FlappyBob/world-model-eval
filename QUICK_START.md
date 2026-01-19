# WorldGym 快速开始指南

## 🚀 环境已就绪

你的 `worldgym` 环境已经安装并配置好以下组件：
- ✅ OpenVLA
- ✅ SpatialVLA
- ✅ Octo
- ✅ CUDA 12.8 支持
- ✅ GPU: NVIDIA GeForce RTX 5090

## 📋 验证安装

```bash
/venv/worldgym/bin/python verify_env.py
```

## 🔧 完成 Octo 配置（必需）

在使用 Octo 之前，需要完成以下两个步骤：

### 1. 安装 dlimp 库
```bash
/venv/worldgym/bin/pip install git+https://github.com/kvablack/dlimp@5edaa4691567873d495633f2708982b42edf1972 --no-deps
```

### 2. 修改 Octo 的 typing.py
编辑文件：`/venv/worldgym/lib/python3.10/site-packages/octo/utils/typing.py`

在文件末尾添加：
```python
PRNGKey = jax.random.PRNGKey
```

或者使用命令：
```bash
echo "PRNGKey = jax.random.PRNGKey" >> /venv/worldgym/lib/python3.10/site-packages/octo/utils/typing.py
```

## 📥 下载世界模型检查点

```bash
/venv/worldgym/bin/pip install gdown
/venv/worldgym/bin/gdown 1uiRP2BuavapMsyP9Cbr25mi_ymk9SEJb
```

这会下载 `mixed_openx_9robots_20frames_0p1actiondropout_580ksteps.pt` (~9GB)

## 🎮 运行评估

将检查点移到合适的位置（如 `~/checkpoints/world-model/`），然后运行：

### OpenVLA
```bash
/venv/worldgym/bin/world-model-eval-openvla \
  --root-dir /path/to/tasks \
  --checkpoint-path ~/checkpoints/world-model/mixed_openx_9robots_20frames_0p1actiondropout_580ksteps.pt \
  --model-name openvla-7b \
  --save-video --video-out-dir ./rollouts/openvla
```

### SpatialVLA
```bash
/venv/worldgym/bin/world-model-eval-spatialvla \
  --root-dir /path/to/tasks \
  --checkpoint-path ~/checkpoints/world-model/mixed_openx_9robots_20frames_0p1actiondropout_580ksteps.pt \
  --model-name spatialvla-4b-224-pt
```

### Octo
```bash
/venv/worldgym/bin/world-model-eval-octo \
  --root-dir /path/to/tasks \
  --checkpoint-path ~/checkpoints/world-model/mixed_openx_9robots_20frames_0p1actiondropout_580ksteps.pt \
  --model-name octo-base-1.5
```

## 📚 更多信息

- 完整环境配置说明: [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md)
- 项目 README: [README.md](README.md)
- 验证脚本: [verify_env.py](verify_env.py)

## 💡 常用命令

```bash
# 使用环境的 Python
/venv/worldgym/bin/python your_script.py

# 使用环境的 pip 安装包
/venv/worldgym/bin/pip install package_name

# 查看已安装的包
/venv/worldgym/bin/pip list

# 训练模型（快速开始）
/venv/worldgym/bin/torchrun --nproc_per_node=1 -m world_model_eval.train
```

## ⚠️ 注意事项

- **RT-1 不支持**: 当前环境无法运行 RT-1，因为它需要 `jax==0.6.2`，与 Octo 的 `jax==0.4.29` 冲突
- **GPU 内存**: RTX 5090 有充足的显存，但仍需根据模型大小调整 batch size
- **Gym 警告**: 你可能会看到 Gym 已弃用的警告，这是正常的，不影响使用

## 🐛 故障排除

### 找不到命令
使用完整路径：`/venv/worldgym/bin/world-model-eval-openvla`

### CUDA 内存不足
减少 batch size 或使用梯度检查点

### Octo 导入错误
确保完成了上述的 Octo 配置步骤
