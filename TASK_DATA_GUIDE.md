# 任务数据准备指南

## 📋 概述

本指南详细说明如何准备用于 WorldGym 评估的任务数据。

## 🎯 数据格式要求

### 目录结构

```
/path/to/tasks/                    # 任务根目录
├── task_name_1/                   # 任务1目录
│   ├── trial_001.png              # 试验1的初始帧图片
│   ├── trial_001.json             # 试验1的元数据
│   ├── trial_002.png              # 试验2的初始帧图片
│   ├── trial_002.json             # 试验2的元数据
│   └── ...
├── task_name_2/                   # 任务2目录
│   ├── scene_1.png
│   ├── scene_1.json
│   └── ...
└── nested/                        # 支持嵌套子目录
    └── subtask/
        ├── frame.png
        ├── frame.json
        └── ...
```

### 文件要求

#### 1. PNG 图片文件
- **格式**: PNG 格式
- **内容**: 机器人场景的初始帧
- **尺寸**: 任意尺寸（会自动缩放到 256x256）
- **命名**: 任意名称，如 `trial_001.png`, `scene_1.png`, `frame.png` 等

#### 2. JSON 元数据文件
- **命名**: 必须与对应的 PNG 文件同名（扩展名为 `.json`）
- **位置**: 必须与对应的 PNG 文件在同一目录

**JSON 格式：**
```json
{
  "instruction": "place the carrot on plate",
  "partial_credit_criteria": "Pick up the carrot."
}
```

**字段说明：**

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `instruction` | string | ✅ 是 | 任务指令/目标描述 |
| `partial_credit_criteria` | string | ❌ 否 | 部分成功的标准（可选）|

**评分说明：**
- 如果提供了 `partial_credit_criteria`：启用 3 级评分（0, 0.5, 1.0）
- 如果未提供 `partial_credit_criteria`：启用二元评分（0, 1.0）

## 🛠️ 使用准备工具

我们提供了 `prepare_tasks.py` 脚本来帮助你创建和管理任务数据。

### 方法 1: 创建示例数据（测试用）

```bash
# 使用默认输出目录 ./example_tasks
/venv/worldgym/bin/python prepare_tasks.py create

# 或指定自定义输出目录
/venv/worldgym/bin/python prepare_tasks.py create /path/to/output
```

这会创建包含 3 个任务、7 个试验的示例数据集：
- `pick_and_place` (3 个试验)
- `drawer_opening` (2 个试验)
- `stacking_blocks` (2 个试验)

⚠️ **注意**: 示例数据使用占位符图片（渐变色图），仅用于测试格式。实际评估需要真实的机器人场景图片。

### 方法 2: 从现有图片创建任务

如果你已经有机器人场景的 PNG 图片：

```bash
/venv/worldgym/bin/python prepare_tasks.py from-images \
  /path/to/your/images \
  /path/to/output \
  task_name \
  "complete the task"
```

**参数说明：**
- `/path/to/your/images`: 包含 PNG 图片的目录
- `/path/to/output`: 输出根目录
- `task_name`: 任务名称（将创建为子目录）
- `"complete the task"`: 默认指令（可选，会应用到所有试验）

**后续步骤：**
生成后，你需要手动编辑每个 JSON 文件，为每个试验自定义指令。

### 方法 3: 手动创建

1. 创建任务目录结构：
   ```bash
   mkdir -p /path/to/tasks/my_task
   ```

2. 将机器人场景的初始帧图片复制到任务目录

3. 为每个 PNG 创建对应的 JSON 文件：
   ```bash
   # 示例：为 scene_1.png 创建 scene_1.json
   cat > /path/to/tasks/my_task/scene_1.json << 'EOF'
   {
     "instruction": "pick up the red cube",
     "partial_credit_criteria": "Move gripper towards the cube"
   }
   EOF
   ```

## ✅ 验证任务数据

创建完任务数据后，使用验证工具检查格式：

```bash
/venv/worldgym/bin/python prepare_tasks.py validate /path/to/tasks
```

验证器会检查：
- ✅ PNG 文件是否存在
- ✅ 对应的 JSON 文件是否存在
- ✅ JSON 格式是否正确
- ✅ `instruction` 字段是否存在且非空
- ⚠️ 报告任何问题

**输出示例：**
```
验证任务目录: /workspace/world-model-eval/example_tasks
============================================================
找到 7 个 PNG 文件
✅ pick_and_place/trial_001.png
   指令: place the red block on the blue plate
   部分成功: Pick up the red block
✅ pick_and_place/trial_002.png
   指令: place the carrot on plate
   部分成功: Pick up the carrot
...
============================================================

总结: 7/7 个有效试验
```

## 🚀 运行评估

数据准备好后，可以运行评估：

### OpenVLA
```bash
/venv/worldgym/bin/world-model-eval-openvla \
  --root-dir /workspace/world-model-eval/example_tasks \
  --checkpoint-path ~/checkpoints/world-model/mixed_openx_9robots_20frames_0p1actiondropout_580ksteps.pt \
  --model-name openvla-7b \
  --save-video --video-out-dir ./rollouts/openvla
```

### SpatialVLA
```bash
/venv/worldgym/bin/world-model-eval-spatialvla \
  --root-dir /workspace/world-model-eval/example_tasks \
  --checkpoint-path ~/checkpoints/world-model/mixed_openx_9robots_20frames_0p1actiondropout_580ksteps.pt \
  --model-name spatialvla-4b-224-pt
```

### Octo
```bash
/venv/worldgym/bin/world-model-eval-octo \
  --root-dir /workspace/world-model-eval/example_tasks \
  --checkpoint-path ~/checkpoints/world-model/mixed_openx_9robots_20frames_0p1actiondropout_580ksteps.pt \
  --model-name octo-base-1.5
```

## 📂 示例数据结构

已创建的示例数据位于 `/workspace/world-model-eval/example_tasks/`：

```
example_tasks/
├── drawer_opening/
│   ├── trial_001.png
│   ├── trial_001.json          # {"instruction": "open the top drawer", ...}
│   ├── trial_002.png
│   └── trial_002.json          # {"instruction": "open the cabinet door", ...}
├── pick_and_place/
│   ├── trial_001.png
│   ├── trial_001.json          # {"instruction": "place the red block on the blue plate", ...}
│   ├── trial_002.png
│   ├── trial_002.json          # {"instruction": "place the carrot on plate", ...}
│   ├── trial_003.png
│   └── trial_003.json          # {"instruction": "put the apple in the bowl", ...}
└── stacking_blocks/
    ├── trial_001.png
    ├── trial_001.json          # {"instruction": "stack the blue block on top of the red block", ...}
    ├── trial_002.png
    └── trial_002.json          # {"instruction": "create a tower with three blocks", ...}
```

**查看示例 JSON：**
```bash
cat /workspace/world-model-eval/example_tasks/pick_and_place/trial_001.json
```

输出：
```json
{
  "instruction": "place the red block on the blue plate",
  "partial_credit_criteria": "Pick up the red block"
}
```

## 💡 实际使用建议

### 1. 从真实机器人数据创建任务

如果你有机器人操作的视频或图片序列：

1. **提取初始帧**：
   ```bash
   ffmpeg -i robot_demo.mp4 -vf "select=eq(n\,0)" -vframes 1 initial_frame.png
   ```

2. **使用工具创建任务**：
   ```bash
   /venv/worldgym/bin/python prepare_tasks.py from-images \
     ./initial_frames \
     ./my_tasks \
     my_robot_task \
     "complete the manipulation task"
   ```

3. **编辑 JSON 文件**，为每个试验添加具体指令

### 2. 从 Open X-Embodiment 数据集创建任务

项目代码中包含 Bridge V2 数据集的示例（`put_carrot_on_plate.json`）。你可以：

1. 下载数据集中的初始帧图片
2. 提取 instruction 和 subtasks 字段
3. 使用我们的格式创建 PNG + JSON 对

### 3. 批量处理多个任务

创建一个脚本批量处理：

```bash
#!/bin/bash
for task_dir in task1 task2 task3; do
  /venv/worldgym/bin/python prepare_tasks.py from-images \
    raw_images/$task_dir \
    processed_tasks \
    $task_dir \
    "default instruction for $task_dir"
done
```

## ⚠️ 常见问题

### Q1: 图片必须是 256x256 吗？
**A**: 不需要。任何尺寸的图片都可以，评估器会自动缩放到 256x256。

### Q2: 可以使用 JPG 或其他格式吗？
**A**: 不可以。评估器只查找 `*.png` 文件。如果你有其他格式，需要先转换：
```bash
convert image.jpg image.png  # 使用 ImageMagick
# 或
ffmpeg -i image.jpg image.png
```

### Q3: JSON 文件必须有 partial_credit_criteria 吗？
**A**: 不是必需的。如果不提供，评估将使用二元评分（成功/失败）。

### Q4: 指令可以多长？
**A**: 没有明确限制，但建议保持简洁明了（1-2 句话）。

### Q5: 可以有嵌套的子目录吗？
**A**: 可以！`discover_trials` 使用 `rglob("*.png")` 递归查找所有 PNG 文件。

### Q6: 任务目录名有要求吗？
**A**: 没有特殊要求。目录名会被用作任务的 `task_key`，并在结果中显示为标题化的名称（如 `pick_and_place` → `Pick And Place`）。

## 📚 相关文件

- [prepare_tasks.py](prepare_tasks.py) - 任务数据准备工具
- [verify_env.py](verify_env.py) - 环境验证脚本
- [QUICK_START.md](QUICK_START.md) - 快速开始指南
- [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md) - 完整环境配置
- [README.md](README.md) - 项目主文档

## 🎓 下一步

1. ✅ 准备任务数据（使用本指南）
2. 📥 下载世界模型检查点
3. 🔧 完成 Octo 配置（如果使用 Octo）
4. 🚀 运行评估
5. 📊 分析结果

---

**需要帮助？** 查看 [QUICK_START.md](QUICK_START.md) 获取快速上手指引。
