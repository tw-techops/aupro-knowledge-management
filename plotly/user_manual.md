# AI成熟度模型鱼骨图生成工具使用说明

## 概述

这个工具可以生成多种版本的AI成熟度模型鱼骨图，帮助您可视化和跟踪AI能力发展状况。

## 版本说明

### 🆕 interactive - 交互式版本（推荐）
**特点**：
- 左侧侧边栏包含所有能力的checkbox列表
- 可以勾选已完成的能力，实时显示完成度
- 自动保存进度到浏览器本地存储
- 提供全选/全不选/保存进度等快捷操作
- 适合个人能力评估和进度跟踪

**使用场景**：
- 个人AI能力自评
- 团队能力现状评估
- 学习进度跟踪
- 目标设定和规划

### ultra - 超清晰布局版本
**特点**：
- 优化的布局设计，信息清晰易读
- 包含可拖拽的行业位置和组织位置参考线
- 所有能力信息直接显示在图表上
- 适合演示和汇报

### static - 静态展示版本
**特点**：
- 紧凑的布局设计
- 包含可拖拽的参考线
- 静态信息展示，无交互功能

### basic - 基础版本
**特点**：
- 基本的鱼骨图结构
- 简洁的信息展示
- 适合快速查看

### detailed - 详细版本
**特点**：
- 详细的能力信息展示
- 包含子分支显示
- 信息丰富但布局复杂

## 使用方法

### 1. 生成指定版本

```bash
# 生成交互式版本（推荐）
python ai_maturity_fishbone_plotly.py --version interactive

# 生成超清晰布局版本
python ai_maturity_fishbone_plotly.py --version ultra

# 生成所有版本
python ai_maturity_fishbone_plotly.py --version all
```

### 2. 查看可用版本

```bash
python ai_maturity_fishbone_plotly.py --list
```

### 3. 查看帮助

```bash
python ai_maturity_fishbone_plotly.py --help
```

## 输出文件

生成的HTML文件保存在 `../outpt/` 目录下：

- `ai_maturity_fishbone_interactive.html` - 交互式版本
- `ai_maturity_fishbone_ultra_clean.html` - 超清晰布局版本
- `ai_maturity_fishbone_static.html` - 静态展示版本
- `ai_maturity_fishbone_basic.html` - 基础版本
- `ai_maturity_fishbone_detailed.html` - 详细版本

## 交互式版本使用指南

### 基本操作
1. 在浏览器中打开 `ai_maturity_fishbone_interactive.html`
2. 左侧边栏显示所有能力的checkbox列表
3. 勾选您已经掌握的能力
4. 顶部显示实时完成度统计
5. 点击"保存进度"按钮保存当前状态

### 快捷功能
- **全选**：快速选择所有能力
- **全不选**：快速取消所有选择
- **保存进度**：手动保存当前状态到浏览器本地存储

### 数据持久化
- 您的选择会自动保存到浏览器的localStorage中
- 下次打开时会自动加载之前的选择状态
- 清除浏览器数据会丢失保存的进度

## 技术要求

- Python 3.6+
- 依赖包：plotly, numpy
- 现代浏览器（Chrome、Firefox、Safari、Edge）

## 数据源

工具从 `../../resource/model_of_level.json` 文件中读取AI成熟度模型数据。

## 常见问题

**Q: 为什么交互式版本的选择没有保存？**
A: 确保点击了"保存进度"按钮，并且浏览器支持localStorage。

**Q: 可以自定义能力数据吗？**
A: 可以修改 `model_of_level.json` 文件中的数据，然后重新生成图表。

**Q: 如何分享我的能力评估结果？**
A: 可以截图分享，或者在浏览器控制台中导出数据：
```javascript
console.log(JSON.stringify([...completedCapabilities]));
```

## 更新日志

### v1.1.0 (2024-07-03)
- 🆕 添加交互式版本，支持checkbox能力跟踪
- 🆕 添加进度保存和加载功能
- 🆕 添加快捷操作按钮
- 📝 更新文档和使用说明

### v1.0.0
- 初始版本，支持基础、详细、静态、超清晰布局四种版本

## 生成的文件

### 核心文件
- `ai_maturity_fishbone_plotly.py` - 主要的鱼骨图生成脚本
- `demo_fishbone.py` - 演示脚本，展示如何使用生成器
- `requirements.txt` - Python 依赖包列表

### 生成的图表
- `ai_maturity_fishbone_basic.html` - 基础版鱼骨图（4.5MB）
- `ai_maturity_fishbone_detailed.html` - 详细版鱼骨图（4.5MB）
- `ai_maturity_fishbone_static.html` - 静态展示版鱼骨图（包含可拖拽参考线）
- `ai_maturity_fishbone_ultra_clean.html` - 超清晰布局版鱼骨图（包含可拖拽参考线）
- `demo_fishbone.html` - 演示版鱼骨图

### 文档
- `README_fishbone.md` - 英文使用说明
- `使用说明.md` - 中文使用说明（本文件）

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行脚本
```bash
# 查看所有可用版本
python ai_maturity_fishbone_plotly.py --list

# 生成完整的鱼骨图（所有版本）
python ai_maturity_fishbone_plotly.py

# 生成特定版本
python ai_maturity_fishbone_plotly.py --version ultra
python ai_maturity_fishbone_plotly.py -v static
```

### 3. 查看结果
在浏览器中打开生成的 HTML 文件即可查看交互式鱼骨图。

## 鱼骨图特点

### 结构设计
- **主干线**: 黑色水平线，代表 AI 成熟度演进路径（L0 → L5）
- **主分支**: 五个能力维度，每个维度用不同颜色表示：
  - 🔴 人员能力
  - 🟢 流程能力  
  - 🔵 技术能力
  - 🟡 知识能力
  - 🟠 治理能力

### 交互功能
- **悬停提示**: 鼠标悬停显示详细能力信息
- **缩放**: 支持图表缩放和平移
- **图例控制**: 点击图例可隐藏/显示特定维度
- **导出**: 支持导出为 PNG、SVG 等格式
- **可拖拽参考线**: 静态版和超清晰版包含可移动的行业位置和组织位置参考线

## 数据分析结果

根据演示脚本的分析，各能力维度的分布情况：

| 能力维度 | 总能力数 | 主要集中级别 |
|---------|---------|------------|
| 技术能力 | 27项 | L3级别（33.3%） |
| 知识能力 | 17项 | L4级别（35.3%） |
| 流程能力 | 16项 | L2和L4级别（各25%） |
| 治理能力 | 16项 | L3级别（31.2%） |
| 人员能力 | 14项 | L2级别（28.6%） |

## 版本选择

### 可用版本
- `all`: 生成所有版本（默认）
- `basic`: 基础版本 - 简单的鱼骨图结构
- `detailed`: 详细版本 - 包含更多细节信息
- `static`: 静态展示版本 - 包含可拖拽参考线，适合一屏显示
- `ultra`: 超清晰布局版本 - 包含可拖拽参考线，最佳视觉效果

### 命令行参数
```bash
# 显示帮助信息
python ai_maturity_fishbone_plotly.py --help

# 显示所有可用版本
python ai_maturity_fishbone_plotly.py --list

# 生成特定版本
python ai_maturity_fishbone_plotly.py --version ultra
python ai_maturity_fishbone_plotly.py -v static

# 生成所有版本（默认）
python ai_maturity_fishbone_plotly.py
```

### 推荐使用
推荐使用 `static` 或 `ultra` 版本，因为它们包含：
- 可拖拽的行业位置参考线（橙色虚线）
- 可拖拽的组织位置参考线（紫色虚线）
- 优化的布局，适合在一个屏幕上完整显示
- 更好的视觉效果和交互体验

## 可拖拽参考线功能

### 功能说明
在 `static` 和 `ultra` 版本中，包含两条可移动的虚线：
- **橙色虚线**: 代表行业当前位置
- **紫色虚线**: 代表组织当前位置

### 使用方法
1. 打开包含参考线的HTML文件
2. 直接用鼠标点击并拖拽虚线到目标位置
3. 通过两条线的位置对比，直观查看组织与行业的成熟度差距
4. 可根据实际评估结果随时调整线条位置

### 应用场景
- 成熟度评估报告
- 对标分析
- 差距分析
- 发展规划制定

## 自定义选项

### 颜色方案
在 `ai_maturity_fishbone_plotly.py` 中修改 `colors` 字典：
```python
colors = {
    '人员能力': '#FF6B6B',  # 红色
    '流程能力': '#4ECDC4',  # 青色
    '技术能力': '#45B7D1',  # 蓝色
    '知识能力': '#96CEB4',  # 绿色
    '治理能力': '#FFEAA7'   # 黄色
}
```

### 布局调整
修改 `capability_positions` 字典来调整维度位置：
```python
capability_positions = {
    '人员能力': 2,    # Y轴位置
    '流程能力': 1,
    '技术能力': 0,    # 主干线位置
    '知识能力': -1,
    '治理能力': -2
}
```

### 图表尺寸
在 `fig.update_layout()` 中调整：
```python
width=1200,   # 宽度
height=800,   # 高度
```

## 技术说明

### 依赖包
- `plotly>=5.0.0` - 交互式图表库
- `numpy>=1.20.0` - 数值计算
- `argparse` - 命令行参数解析（Python内置）
- `sys` - 系统相关功能（Python内置）
- `pandas>=1.3.0` - 数据处理（可选）

### 数据源
脚本读取 `model_of_level.json` 文件，该文件包含：
- 6个成熟度级别（L0-L5）
- 每个级别的标题、描述、特征
- 5个能力维度的具体能力项

### 图表实现
- 使用 `go.Scatter` 绘制线条和点
- 使用 `annotations` 添加文本标签
- 通过 `hovertemplate` 实现交互式提示
- 支持图例控制和缩放功能
- 使用 `shapes` 添加可拖拽的参考线
- 通过 `editable=True` 启用交互编辑功能

## 使用建议

1. **首次使用**: 先运行 `python ai_maturity_fishbone_plotly.py --list` 查看可用版本
2. **快速开始**: 使用 `python ai_maturity_fishbone_plotly.py -v ultra` 生成推荐版本
3. **评估分析**: 使用可拖拽参考线功能进行组织和行业对比分析
4. **定制需求**: 根据需要修改颜色和布局
5. **分享展示**: HTML 文件可直接在浏览器中打开，支持全屏展示
6. **进一步开发**: 可基于现有代码扩展更多功能

## 更新历史

### 最新版本特性
- ✅ 新增可拖拽参考线功能（行业位置和组织位置）
- ✅ 新增命令行参数支持，可选择生成特定版本
- ✅ 优化布局，支持一屏显示
- ✅ 改进交互体验，支持编辑模式
- ✅ 新增静态展示版本和超清晰布局版本

### 版本对比

| 功能特性 | 基础版 | 详细版 | 静态版 | 超清晰版 |
|---------|--------|--------|--------|----------|
| 基本鱼骨图 | ✅ | ✅ | ✅ | ✅ |
| 详细信息显示 | ❌ | ✅ | ✅ | ✅ |
| 可拖拽参考线 | ❌ | ❌ | ✅ | ✅ |
| 一屏显示优化 | ❌ | ❌ | ✅ | ✅ |
| 最佳视觉效果 | ❌ | ❌ | ❌ | ✅ |

## 联系支持

如需进一步定制或有技术问题，请提供具体需求和错误信息。 