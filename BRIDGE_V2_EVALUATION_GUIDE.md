# Bridge V2 评估使用指南

## 📋 当前状态

✅ **已完成的准备工作**：

1. ✅ 环境配置完成
   - Python 3.10.19
   - worldgym 环境（支持 OpenVLA, SpatialVLA, Octo）
   - 所有依赖已安装

2. ✅ Bridge V2 评估数据已就绪
   - 任务：`put_carrot_on_plate`
   - 试验数：54 个
   - 数据大小：19MB
   - 位置：`/workspace/world-model-eval/bridge_tasks/`
   - 状态：已验证，格式正确

3. ✅ 系统资源充足
   - 可用磁盘：277GB
   - 可用内存：231GB
   - GPU：NVIDIA GeForce RTX 5090

## 🚀 快速开始

### 步骤 1: 下载世界模型检查点

```bash
cd /workspace/world-model-eval

# 安装 gdown（如果还没有）
/venv/worldgym/bin/pip install gdown

# 下载检查点（约 9GB，需要几分钟）
/venv/worldgym/bin/gdown 1uiRP2BuavapMsyP9Cbr25mi_ymk9SEJb

# 可选：移动到标准位置
mkdir -p ~/checkpoints/world-model
mv mixed_openx_9robots_20frames_0p1actiondropout_580ksteps.pt ~/checkpoints/world-model/
```

### 步骤 2: 选择要使用的模型

#### 选项 A: OpenVLA（推荐，最简单）

```bash
/venv/worldgym/bin/world-model-eval-openvla \
  --root-dir /workspace/world-model-eval/bridge_tasks \
  --checkpoint-path ~/checkpoints/world-model/mixed_openx_9robots_20frames_0p1actiondropout_580ksteps.pt \
  --model-name openvla-7b \
  --save-video --video-out-dir ./rollouts/openvla
```

#### 选项 B: SpatialVLA

```bash
/venv/worldgym/bin/world-model-eval-spatialvla \
  --root-dir /workspace/world-model-eval/bridge_tasks \
  --checkpoint-path ~/checkpoints/world-model/mixed_openx_9robots_20frames_0p1actiondropout_580ksteps.pt \
  --model-name spatialvla-4b-224-pt \
  --save-video --video-out-dir ./rollouts/spatialvla
```

#### 选项 C: Octo（需要额外配置）

**首先完成 Octo 配置：**

```bash
# 1. 安装 dlimp 库
/venv/worldgym/bin/pip install git+https://github.com/kvablack/dlimp@5edaa4691567873d495633f2708982b42edf1972 --no-deps

# 2. 修改 Octo typing.py
echo "PRNGKey = jax.random.PRNGKey" >> /venv/worldgym/lib/python3.10/site-packages/octo/utils/typing.py

# 3. 验证修改
tail -1 /venv/worldgym/lib/python3.10/site-packages/octo/utils/typing.py
# 应该显示: PRNGKey = jax.random.PRNGKey
```

**然后运行评估：**

```bash
/venv/worldgym/bin/world-model-eval-octo \
  --root-dir /workspace/world-model-eval/bridge_tasks \
  --checkpoint-path ~/checkpoints/world-model/mixed_openx_9robots_20frames_0p1actiondropout_580ksteps.pt \
  --model-name octo-base-1.5 \
  --save-video --video-out-dir ./rollouts/octo
```

## 📊 评估数据详情

### 任务信息

- **任务名称**: `put_carrot_on_plate`
- **指令**: "place the carrot on plate"
- **部分成功标准**: "Pick up the carrot."
- **试验数量**: 54
- **数据来源**: Bridge V2 官方数据集

### 目录结构

```
/workspace/world-model-eval/bridge_tasks/
└── put_carrot_on_plate/
    ├── trial_001.png       # 初始帧图片
    ├── trial_001.json      # 元数据
    ├── trial_002.png
    ├── trial_002.json
    ├── ...
    ├── trial_054.png
    └── trial_054.json
```

### 元数据格式示例

```json
{
  "instruction": "place the carrot on plate",
  "partial_credit_criteria": "Pick up the carrot.",
  "source": "bridge_v2",
  "original_url": "https://rail.eecs.berkeley.edu/datasets/..."
}
```

## 📈 预期输出

### 评估过程中

- 进度条显示 54 个试验的处理进度
- 每个试验的世界模型推理（生成未来帧）
- VLM 评分（成功/部分成功/失败）
- 实时统计信息

### 完成后

**1. 视频输出** （如果使用 `--save-video`）：
```
./rollouts/openvla/  (或 spatialvla/octo)
├── video_001.mp4
├── video_002.mp4
├── ...
└── video_054.mp4
```

**2. 控制台输出**：
- 任务级别的成功率
- 部分成功率
- 平均得分
- 按试验的详细结果

**3. 结果文件**：
- 可能包含 JSON 格式的详细结果
- 每个试验的评分和评价

## 💡 关于 400GB Bridge 数据集的说明

### 为什么不需要下载 400GB 数据集？

1. **评估只需初始帧**
   - 每个试验只用 1 张 PNG 图片（初始状态）
   - 加上 1 个 JSON 文件（任务描述）
   - 总共约 350KB/试验

2. **400GB 包含什么？**
   - 完整的视频序列（每个试验数百帧）
   - 动作序列数据
   - 所有任务的所有轨迹
   - 主要用于**训练**，不用于评估

3. **已下载的数据足够**
   - 54 个 `put_carrot_on_plate` 试验
   - 高质量、多样化的场景
   - 占用空间：仅 19MB

### 如果需要更多任务？

**方法 1: 使用现有工具下载**

如果官方提供了其他任务的 JSON 清单（类似 `put_carrot_on_plate.json`）：

```bash
# 假设有 put_eggplant_into_pot_or_pan.json
/venv/worldgym/bin/python prepare_bridge_data.py \
  ./bridge_tasks_more \
  --json-file src/world_model_eval/put_eggplant_into_pot_or_pan.json
```

**方法 2: 从 TFDS 数据提取**

如果你有本地的 400GB TFDS 数据：

1. 修改 `download_data.py` 中的路径指向本地
2. 运行转换脚本提取特定任务
3. 从转换结果提取初始帧

**方法 3: 手动选择**

如果想从 400GB 中选择特定试验：

1. 浏览 TFDS 数据找到感兴趣的任务
2. 提取初始帧为 PNG
3. 手动创建对应的 JSON 元数据
4. 使用 `prepare_tasks.py validate` 验证

## 🛠️ 实用工具

### 验证数据格式

```bash
/venv/worldgym/bin/python prepare_tasks.py validate /workspace/world-model-eval/bridge_tasks
```

### 查看任务统计

```bash
# 查看试验数量
ls /workspace/world-model-eval/bridge_tasks/put_carrot_on_plate/*.png | wc -l

# 查看数据大小
du -sh /workspace/world-model-eval/bridge_tasks

# 查看示例元数据
cat /workspace/world-model-eval/bridge_tasks/put_carrot_on_plate/trial_001.json
```

### 查看图片

```bash
# 如果有图片查看器
display /workspace/world-model-eval/bridge_tasks/put_carrot_on_plate/trial_001.png

# 或用 Python 查看图片信息
/venv/worldgym/bin/python -c "
from PIL import Image
img = Image.open('/workspace/world-model-eval/bridge_tasks/put_carrot_on_plate/trial_001.png')
print(f'尺寸: {img.size}, 模式: {img.mode}')
"
```

## 🔍 故障排除

### 问题 1: 找不到检查点文件

**错误**: `FileNotFoundError: checkpoint.pt`

**解决**:
```bash
# 检查检查点是否已下载
ls -lh ~/checkpoints/world-model/mixed_openx_9robots_20frames_0p1actiondropout_580ksteps.pt

# 如果不存在，重新下载
cd /workspace/world-model-eval
/venv/worldgym/bin/gdown 1uiRP2BuavapMsyP9Cbr25mi_ymk9SEJb
```

### 问题 2: CUDA 内存不足

**错误**: `RuntimeError: CUDA out of memory`

**解决**:
- 你的 RTX 5090 显存非常充足，不应该出现此问题
- 如果出现，可能是其他进程占用了 GPU
- 检查 GPU 使用情况：`nvidia-smi`

### 问题 3: Octo 导入错误

**错误**: `AttributeError: module 'octo.utils.typing' has no attribute 'PRNGKey'`

**解决**: 确保完成了 Octo 配置步骤（见上文"选项 C"）

### 问题 4: 评估速度慢

**原因**: 世界模型推理需要 GPU 计算

**优化建议**:
- 使用较小的模型（如 spatialvla-4b 而不是 openvla-7b）
- 减少保存视频的数量
- 确保没有其他 GPU 任务在运行

## 📚 相关文档

- [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md) - 完整环境配置
- [QUICK_START.md](QUICK_START.md) - 快速开始指南
- [TASK_DATA_GUIDE.md](TASK_DATA_GUIDE.md) - 任务数据格式
- [README.md](README.md) - 项目文档

## 🎯 总结

**你现在可以：**

1. ✅ 直接使用已准备的 Bridge V2 数据（54 个试验）
2. ✅ 运行 OpenVLA、SpatialVLA 或 Octo 评估
3. ✅ 无需下载 400GB 完整数据集
4. ✅ 根据需要添加更多任务

**下一步：**

1. 下载世界模型检查点（9GB）
2. 运行评估命令
3. 查看生成的视频和评分结果

**需要帮助？**

- 检查 [verify_env.py](verify_env.py) 确保环境正确
- 查看日志输出了解详细错误信息
- 参考项目文档获取更多信息

---

**祝评估顺利！** 🚀
