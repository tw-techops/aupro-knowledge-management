# AI成熟度模型可视化系统 (AI Maturity Model Visualization)

## 📋 项目概述

这是一个基于Plotly的AI软件交付能力成熟度模型可视化系统，通过交互式鱼骨图的形式展示AI能力发展的6个成熟度级别（L0-L5）和5个核心能力维度。该系统支持能力跟踪、进度保存和多语言展示，帮助个人和团队评估AI能力现状并制定发展规划。

## ✨ 主要特性

### 🎯 多版本支持
- **交互式版本** - 包含侧边栏checkbox功能，支持能力跟踪和进度保存
- **超清晰布局版本** - 优化的信息展示，包含可拖拽参考线，适合演示
- **静态展示版本** - 紧凑布局，基础信息展示
- **基础版本** - 简洁的鱼骨图结构展示
- **详细版本** - 完整的能力信息展示

### 🌐 多语言支持
- **中文版本** - 完整的中文界面和数据
- **英文版本** - 国际化支持，适合全球团队使用

### 🔧 核心功能
- **能力跟踪** - 通过checkbox勾选已完成的能力项
- **进度保存** - 自动保存到浏览器本地存储
- **实时统计** - 显示完成度百分比和数量统计
- **交互式图表** - 支持缩放、平移、图例控制
- **导出功能** - 支持PNG、SVG等格式导出
- **Web服务** - 内置Flask服务器，支持Web访问

## 🏗️ 项目结构

```
aupro-knowledge-management/
├── plotly/                           # 主要功能目录
│   ├── script/                       # 脚本目录
│   │   ├── ai_maturity_fishbone_plotly.py     # 中文版生成脚本
│   │   └── ai_maturity_fishbone_plotly_en.py  # 英文版生成脚本
│   ├── outpt/                        # 输出文件目录
│   │   ├── ai_sd_maturity_interactive.html    # 中文交互版
│   │   ├── ai_sd_maturity_interactive_en.html # 英文交互版
│   │   ├── ai_sd_maturity_ultra.html          # 中文超清晰版
│   │   └── ai_sd_maturity_ultra_en.html       # 英文超清晰版
│   ├── server.py                     # Flask Web服务器
│   ├── start_server.py               # 服务器启动脚本
│   ├── requirements.txt              # Python依赖
│   ├── README_EN.md                  # 英文说明文档
│   ├── README_fishbone.md            # 鱼骨图说明
│   ├── README_interactive.md         # 交互版说明
│   ├── README_server.md              # 服务器说明
│   ├── SUMMARY_EN.md                 # 英文版总结
│   └── user_manual.md                # 用户手册
├── resource/                         # 资源文件目录
│   ├── model_of_level.json           # 中文数据模型
│   ├── model_of_level_en.json        # 英文数据模型
│   └── ai_maturity_capabilities_summary.md  # 能力总结文档
└── README.md                         # 项目总README（本文件）
```

## 🚀 快速开始

### 环境要求
- Python 3.6+
- 现代浏览器（Chrome、Firefox、Safari、Edge）

### 安装依赖
```bash
cd plotly
pip install -r requirements.txt
```

### 生成图表
```bash
# 生成所有版本（中文）
python script/ai_maturity_fishbone_plotly.py

# 生成交互式版本（推荐）
python script/ai_maturity_fishbone_plotly.py --version interactive

# 生成英文版本
python script/ai_maturity_fishbone_plotly_en.py

# 查看可用版本
python script/ai_maturity_fishbone_plotly.py --list
```

### 启动Web服务
```bash
# 使用启动脚本（推荐）
python start_server.py

# 或直接启动
python server.py
```

访问 http://localhost:5000 查看所有版本的图表。

## 📊 成熟度模型说明

### 6个成熟度级别
- **L0 - 完全人工驱动** - 建立基础设施和流程规范
- **L1 - 智能编程助手** - AI辅助个体开发者
- **L2 - 团队级AI工程化** - 团队协同AI集成
- **L3 - AI自主开发** - AI主导开发流程
- **L4 - 高度自治与创新** - AI主动优化和创新
- **L5 - 完全自主AI交付** - AI完全自主软件交付

### 5个核心能力维度
- **🔴 人员能力** - 人力资源和技能发展
- **🟢 流程能力** - 工作流程和方法论
- **🔵 技术能力** - 工具和技术实现
- **🟡 知识能力** - 信息管理和学习能力
- **🟠 治理能力** - 监督和合规管理

## 🎯 使用指南

### 交互式版本使用
1. 在浏览器中打开交互式版本HTML文件
2. 左侧边栏显示所有能力的checkbox列表
3. 勾选您已经掌握的能力
4. 查看实时完成度统计
5. 点击"保存进度"按钮保存状态

### 快捷操作
- **全选** - 快速选择所有能力
- **全不选** - 快速取消所有选择
- **保存进度** - 手动保存到浏览器本地存储

### 数据持久化
- 选择状态自动保存到浏览器localStorage
- 下次打开时自动加载之前的选择
- 清除浏览器数据会丢失保存的进度

## 🌐 Web服务访问

启动服务器后，可通过以下地址访问：

- **主页**: http://localhost:8023
- **中文交互版**: http://localhost:8023/interactive
- **英文交互版**: http://localhost:8023/interactive_en
- **中文超清晰版**: http://localhost:8023/ultra
- **英文超清晰版**: http://localhost:8023/ultra_en
- **文件列表API**: http://localhost:8023/list

## 🔧 自定义配置

### 修改数据模型
编辑 `resource/model_of_level.json` 或 `resource/model_of_level_en.json` 文件来自定义能力数据。

### 修改服务器配置
编辑 `server.py` 文件来修改端口或其他服务器设置：
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

## 📝 最佳实践

### 个人使用
1. 使用交互式版本进行能力自评
2. 定期（每季度）重新评估能力状态
3. 使用"全选"功能可视化目标状态
4. 制定基于差距的学习计划

### 团队使用
1. 团队成员分别完成能力评估
2. 汇总团队整体能力现状
3. 识别能力短板和发展重点
4. 制定团队能力提升计划

### 组织使用
1. 各团队完成能力评估
2. 分析组织整体AI成熟度
3. 制定分阶段的能力发展路线图
4. 定期跟踪和调整发展策略

## 🛠️ 技术栈

- **后端**: Python + Flask
- **前端**: HTML + CSS + JavaScript
- **图表**: Plotly.js
- **数据**: JSON格式
- **存储**: 浏览器localStorage

## 🤝 贡献指南

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🆘 故障排除

### 常见问题

**Q: Flask未安装**
```bash
pip install flask
```

**Q: 端口被占用**
修改 `server.py` 中的端口号，或停止占用端口的程序。

**Q: 文件不存在**
请先运行生成脚本创建HTML文件。

**Q: 交互式版本选择没有保存**
确保点击"保存进度"按钮，并且浏览器支持localStorage。

### 技术支持

如遇到问题，请：
1. 查看相关README文档
2. 检查浏览器控制台错误信息
3. 确认Python依赖已正确安装
4. 提交Issue描述具体问题

## 📞 联系方式

如有疑问或建议，请通过以下方式联系：
- 提交GitHub Issue
- 发送邮件至项目维护者

---

**🎉 开始使用AI成熟度模型可视化系统，评估和提升您的AI能力！** 