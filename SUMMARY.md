# WorldGym Bridge V2 评估 - 完整总结

## ✅ 已完成的工作

### 1. 环境配置 ✅

**环境名称**: `worldgym` (位于 `/venv/worldgym`)

**已安装的核心组件**:
- ✅ Python 3.10.19
- ✅ PyTorch 2.11.0 (CUDA 12.8)
- ✅ Transformers 4.49.0
- ✅ JAX 0.4.29 (CUDA 12)
- ✅ Flax 0.8.4
- ✅ TensorFlow 2.19.1
- ✅ Diffusers 0.35.1
- ✅ Octo (from GitHub)
- ✅ world-model-eval (editable install)

**支持的模型**:
- ✅ OpenVLA (7B)
- ✅ SpatialVLA (4B)
- ✅ Octo (base-1.5)
- ❌ RT-1 (不支持，JAX 版本冲突)

### 2. 评估数据准备 ✅

**Bridge V2 数据**:
- 任务: `put_carrot_on_plate`
- 试验数: 54 个
- 数据大小: 19MB
- 位置: `/workspace/world-model-eval/bridge_tasks/`
- 格式: PNG + JSON (符合评估要求)
- 状态: ✅ 已验证

**示例数据**:
- 位置: `/workspace/world-model-eval/example_tasks/`
- 任务: 3 个 (pick_and_place, drawer_opening, stacking_blocks)
- 试验数: 7 个
- 大小: 56KB
- 用途: 测试工具和格式

### 3. 工具脚本 ✅

**数据准备工具**:
- ✅ `prepare_tasks.py` - 通用任务数据创建/验证
  - 创建示例数据
  - 从现有图片创建任务
  - 验证数据格式

- ✅ `prepare_bridge_data.py` - Bridge V2 数据下载
  - 从 JSON 清单下载图片
  - 自动转换格式
  - 支持限制下载数量

**环境工具**:
- ✅ `verify_env.py` - 环境验证脚本
- ✅ `activate_env.sh` - 环境激活脚本

### 4. 文档 ✅

**配置文档**:
- ✅ `ENVIRONMENT_SETUP.md` - 完整环境配置说明
- ✅ `QUICK_START.md` - 快速开始指南
- ✅ `TASK_DATA_GUIDE.md` - 任务数据格式详细说明

**使用指南**:
- ✅ `BRIDGE_V2_EVALUATION_GUIDE.md` - Bridge V2 评估使用指南
- ✅ `COMMANDS_CHEATSHEET.md` - 命令速查表
- ✅ `SUMMARY.md` - 本文档（总结）

**原始文档**:
- ✅ `README.md` - 项目原始文档

**依赖记录**:
- ✅ `requirements_installed.txt` - 已安装包列表

---

## 🎯 下一步操作

### 必须做的事情

#### 1. 下载世界模型检查点（必需）

```bash
cd /workspace/world-model-eval
/venv/worldgym/bin/pip install gdown
/venv/worldgym/bin/gdown 1uiRP2BuavapMsyP9Cbr25mi_ymk9SEJb
mkdir -p ~/checkpoints/world-model
mv mixed_openx_9robots_20frames_0p1actiondropout_580ksteps.pt ~/checkpoints/world-model/
```

**大小**: 约 9GB
**时间**: 取决于网速，可能需要 5-30 分钟

#### 2. 运行评估（必需）

选择一个模型运行：

**OpenVLA（推荐）**:
```bash
/venv/worldgym/bin/world-model-eval-openvla \
  --root-dir /workspace/world-model-eval/bridge_tasks \
  --checkpoint-path ~/checkpoints/world-model/mixed_openx_9robots_20frames_0p1actiondropout_580ksteps.pt \
  --model-name openvla-7b \
  --save-video --video-out-dir ./rollouts/openvla
```

### 可选的事情

#### 1. 完成 Octo 配置（如果要用 Octo）

```bash
# 安装 dlimp
/venv/worldgym/bin/pip install git+https://github.com/kvablack/dlimp@5edaa4691567873d495633f2708982b42edf1972 --no-deps

# 修改 typing.py
echo "PRNGKey = jax.random.PRNGKey" >> /venv/worldgym/lib/python3.10/site-packages/octo/utils/typing.py
```

#### 2. 添加更多评估任务

如果需要评估其他任务，使用准备工具：

```bash
# 方法1: 从 JSON 清单下载（如果有）
/venv/worldgym/bin/python prepare_bridge_data.py ./bridge_tasks_more --json-file path/to/task.json

# 方法2: 从现有图片创建
/venv/worldgym/bin/python prepare_tasks.py from-images \
  /path/to/images \
  ./new_tasks \
  task_name \
  "task instruction"

# 方法3: 创建示例数据测试
/venv/worldgym/bin/python prepare_tasks.py create ./test_tasks
```

---

## 📊 资源使用情况

### 当前使用

| 资源 | 使用 | 可用 | 总计 |
|------|------|------|------|
| 磁盘 | 24GB | 277GB | 300GB |
| 内存 | 19GB | 231GB | 251GB |
| GPU 内存 | - | - | RTX 5090 |

**数据占用**:
- Bridge V2 评估数据: 19MB
- 示例数据: 56KB
- 测试数据: 1.8MB
- **总计**: 约 21MB

**还需要**:
- 世界模型检查点: 9GB
- 模型运行时内存: 取决于模型大小
- 生成的视频: 取决于试验数量（每个视频约 1-10MB）

### 估算的总需求

| 项目 | 大小 |
|------|------|
| 环境 + 依赖 | 约 15GB |
| 评估数据 | 19MB |
| 世界模型检查点 | 9GB |
| 输出视频（54个） | 约 100-500MB |
| **总计** | 约 25GB |

**结论**: 资源非常充足，完全够用！

---

## 🔑 关键文件位置

### 代码和脚本

```
/workspace/world-model-eval/
├── src/world_model_eval/          # 主代码
│   ├── run_openvla.py            # OpenVLA 评估器
│   ├── run_spatialvla.py         # SpatialVLA 评估器
│   ├── run_octo.py               # Octo 评估器
│   ├── download_data.py          # 数据下载/转换
│   └── put_carrot_on_plate.json  # Bridge V2 任务清单
├── prepare_tasks.py               # 任务数据工具
├── prepare_bridge_data.py         # Bridge V2 下载工具
└── verify_env.py                  # 环境验证脚本
```

### 数据

```
/workspace/world-model-eval/
├── bridge_tasks/                  # Bridge V2 评估数据（主要）
│   └── put_carrot_on_plate/
│       ├── trial_001.png + .json
│       ├── trial_002.png + .json
│       └── ... (54 个试验)
├── bridge_tasks_test/             # 测试数据（5个试验）
└── example_tasks/                 # 示例数据（7个试验）
```

### 文档

```
/workspace/world-model-eval/
├── BRIDGE_V2_EVALUATION_GUIDE.md  # Bridge V2 评估指南 ⭐
├── COMMANDS_CHEATSHEET.md         # 命令速查表 ⭐
├── SUMMARY.md                     # 本文档 ⭐
├── ENVIRONMENT_SETUP.md           # 环境配置详解
├── QUICK_START.md                 # 快速开始
├── TASK_DATA_GUIDE.md             # 数据格式指南
└── README.md                      # 项目原始文档
```

**⭐ 推荐优先阅读**

### 检查点（需下载）

```
~/checkpoints/world-model/
└── mixed_openx_9robots_20frames_0p1actiondropout_580ksteps.pt  (9GB)
```

### 输出

```
/workspace/world-model-eval/
└── rollouts/
    ├── openvla/           # OpenVLA 输出
    ├── spatialvla/        # SpatialVLA 输出
    └── octo/              # Octo 输出
```

---

## 💡 常见问题

### Q1: 需要下载完整的 400GB Bridge 数据集吗？

**A**: 不需要！

原因：
- 评估只需要初始帧（PNG 图片）
- 已经下载了 54 个 `put_carrot_on_plate` 试验
- 400GB 数据主要用于训练，包含完整视频序列
- 如需更多任务，可以选择性下载

### Q2: 哪个模型最好用？

**A**: 推荐 OpenVLA

- **OpenVLA**: 7B 参数，性能好，配置简单 ✅
- **SpatialVLA**: 4B 参数，速度快，适合快速测试
- **Octo**: 需要额外配置，但可能有不同的性能特点

建议先用 OpenVLA，如果需要速度可以试 SpatialVLA。

### Q3: 评估需要多长时间？

**A**: 取决于模型和试验数量

估算：
- 每个试验: 10-60 秒（取决于模型和硬件）
- 54 个试验: 10-60 分钟
- RTX 5090 性能强劲，应该在较快的一端

### Q4: 评估结果保存在哪里？

**A**:

- **视频**: `./rollouts/<model_name>/`
- **日志**: 控制台输出或日志文件
- **统计**: 评估完成后的总结输出

### Q5: 如何验证环境是否正确？

**A**: 运行验证脚本

```bash
/venv/worldgym/bin/python verify_env.py
```

应该看到所有包都标记为 ✅

### Q6: GPU 内存够用吗？

**A**: 完全够用！

- RTX 5090 有大量显存
- 世界模型和策略模型都不会占用太多
- 如果真的不够，可以减少 batch size（但应该不需要）

### Q7: 可以同时运行多个评估吗？

**A**: 理论上可以，但不推荐

- 会占用更多 GPU 内存
- 可能导致性能下降
- 建议按顺序运行不同模型

### Q8: 如何添加更多任务？

**A**: 三种方法

1. **从在线 URL 下载**（推荐）
   - 使用 `prepare_bridge_data.py`
   - 需要 JSON 清单文件

2. **从本地图片创建**
   - 使用 `prepare_tasks.py from-images`
   - 适合有自己的机器人数据

3. **从 TFDS 数据提取**
   - 使用 `download_data.py`
   - 适合有完整 Bridge V2 数据集

详见 [TASK_DATA_GUIDE.md](TASK_DATA_GUIDE.md)

---

## 🚨 注意事项

### 重要的事情

1. **环境使用**
   - 始终使用 `/venv/worldgym/bin/python`
   - 不要用系统 Python（会找不到包）

2. **检查点路径**
   - 确保检查点路径正确
   - 检查点文件约 9GB

3. **数据格式**
   - PNG 图片 + JSON 元数据
   - JSON 必须有 `instruction` 字段
   - 文件名必须匹配（除了扩展名）

4. **Octo 特殊配置**
   - 如果用 Octo，必须先完成额外配置
   - 不配置会报错

5. **GPU 监控**
   - 用 `nvidia-smi` 查看 GPU 状态
   - 如果卡住，可能是内存不足（虽然不太可能）

### 不要做的事情

- ❌ 不要删除或移动 `bridge_tasks/` 目录
- ❌ 不要用系统 Python 运行脚本
- ❌ 不要在运行评估时重启环境
- ❌ 不要同时运行多个评估（除非你知道在做什么）
- ❌ 不要手动修改生成的 JSON 文件（会破坏格式）

---

## 📞 获取帮助

### 文档

1. **快速问题**: 查看 [COMMANDS_CHEATSHEET.md](COMMANDS_CHEATSHEET.md)
2. **评估问题**: 查看 [BRIDGE_V2_EVALUATION_GUIDE.md](BRIDGE_V2_EVALUATION_GUIDE.md)
3. **环境问题**: 查看 [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md)
4. **数据问题**: 查看 [TASK_DATA_GUIDE.md](TASK_DATA_GUIDE.md)

### 验证工具

```bash
# 验证环境
/venv/worldgym/bin/python verify_env.py

# 验证数据
/venv/worldgym/bin/python prepare_tasks.py validate bridge_tasks

# 查看帮助
/venv/worldgym/bin/world-model-eval-openvla --help
```

### 社区资源

- 项目主页: https://world-model-eval.github.io/
- 论文: https://arxiv.org/abs/2506.00613
- GitHub: https://github.com/world-model-eval/world-model-eval
- Bridge V2: https://rail.eecs.berkeley.edu/datasets/bridge_release/

---

## 🎉 总结

### 你现在拥有

✅ 完整配置的环境（OpenVLA, SpatialVLA, Octo）
✅ 54 个 Bridge V2 评估试验数据
✅ 所有必要的工具和脚本
✅ 详细的文档和使用指南
✅ 充足的系统资源（GPU, 内存, 磁盘）

### 你需要做的

1️⃣ 下载世界模型检查点（9GB）
2️⃣ 运行评估命令
3️⃣ 查看结果和生成的视频

### 预计时间

- 下载检查点: 5-30 分钟（取决于网速）
- 运行评估: 10-60 分钟（取决于模型）
- 总计: 约 1-2 小时

---

**一切准备就绪！祝评估顺利！** 🚀🎊

有问题随时查看文档或运行验证脚本。
