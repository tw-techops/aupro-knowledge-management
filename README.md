# AI Maturity Model Visualization System

## 📋 Project Overview

This is a Plotly-based AI software delivery capability maturity model visualization system that displays 6 maturity levels (L0-L5) and 5 core capability dimensions through interactive fishbone diagrams. The system supports capability tracking, progress saving, and multi-language display, helping individuals and teams assess their current AI capabilities and develop improvement plans.

## ✨ Key Features

### 🎯 Multi-Version Support
- **Interactive Version** - Includes sidebar checkbox functionality for capability tracking and progress saving
- **Ultra-Clear Layout Version** - Optimized information display with draggable reference lines, suitable for presentations
- **Static Display Version** - Compact layout with basic information display
- **Basic Version** - Simple fishbone diagram structure display
- **Detailed Version** - Complete capability information display

### 🌐 Multi-Language Support
- **Chinese Version** - Complete Chinese interface and data
- **English Version** - International support for global teams

### 🔧 Core Features
- **Capability Tracking** - Check completed capability items through checkboxes
- **Progress Saving** - Automatic saving to browser local storage
- **Real-time Statistics** - Display completion percentage and quantity statistics
- **Interactive Charts** - Support zooming, panning, and legend control
- **Export Functionality** - Support PNG, SVG and other format exports
- **Web Service** - Built-in Flask server for web access

## 🏗️ Project Structure

```
aupro-knowledge-management/
├── plotly/                           # Main functionality directory
│   ├── script/                       # Script directory
│   │   ├── ai_maturity_fishbone_plotly.py     # Chinese version generation script
│   │   └── ai_maturity_fishbone_plotly_en.py  # English version generation script
│   ├── outpt/                        # Output files directory
│   │   ├── ai_sd_maturity_interactive.html    # Chinese interactive version
│   │   ├── ai_sd_maturity_interactive_en.html # English interactive version
│   │   ├── ai_sd_maturity_ultra.html          # Chinese ultra-clear version
│   │   └── ai_sd_maturity_ultra_en.html       # English ultra-clear version
│   ├── server.py                     # Flask web server
│   ├── start_server.py               # Server startup script
│   ├── requirements.txt              # Python dependencies
│   ├── README_EN.md                  # English documentation
│   ├── README_fishbone.md            # Fishbone diagram documentation
│   ├── README_interactive.md         # Interactive version documentation
│   ├── README_server.md              # Server documentation
│   ├── SUMMARY_EN.md                 # English version summary
│   └── user_manual.md                # User manual
├── resource/                         # Resource files directory
│   ├── model_of_level.json           # Chinese data model
│   ├── model_of_level_en.json        # English data model
│   └── ai_maturity_capabilities_summary.md  # Capability summary document
└── README.md                         # Project main README (this file)
```

## 🚀 Quick Start

### Requirements
- Python 3.6+
- Modern browser (Chrome, Firefox, Safari, Edge)

### Install Dependencies
```bash
cd plotly
pip install -r requirements.txt
```

### Generate Charts
```bash
# Generate all versions (Chinese)
python script/ai_maturity_fishbone_plotly.py

# Generate interactive version (recommended)
python script/ai_maturity_fishbone_plotly.py --version interactive

# Generate English version
python script/ai_maturity_fishbone_plotly_en.py

# View available versions
python script/ai_maturity_fishbone_plotly.py --list
```

### Start Web Service
```bash
# Use startup script (recommended)
python start_server.py

# Or start directly
python server.py
```

Visit http://localhost:5000 to view all versions of the charts.

## 📊 Maturity Model Description

### 6 Maturity Levels
- **L0 - Fully Manual Driven** - Establish infrastructure and process standards
- **L1 - Intelligent Programming Assistant** - AI-assisted individual developers
- **L2 - Team-level AI Engineering** - Team collaborative AI integration
- **L3 - AI Autonomous Development** - AI-driven development processes
- **L4 - High Autonomy and Innovation** - AI proactive optimization and innovation
- **L5 - Fully Autonomous AI Delivery** - AI fully autonomous software delivery

### 5 Core Capability Dimensions
- **🔴 Personnel Capability** - Human resources and skill development
- **🟢 Process Capability** - Workflows and methodologies
- **🔵 Technical Capability** - Tools and technical implementation
- **🟡 Knowledge Capability** - Information management and learning ability
- **🟠 Governance Capability** - Supervision and compliance management

## 🎯 Usage Guide

### Interactive Version Usage
1. Open the interactive version HTML file in your browser
2. The left sidebar displays a checkbox list of all capabilities
3. Check the capabilities you have mastered
4. View real-time completion statistics
5. Click the "Save Progress" button to save status

### Quick Operations
- **Select All** - Quickly select all capabilities
- **Deselect All** - Quickly deselect all selections
- **Save Progress** - Manually save to browser local storage

### Data Persistence
- Selection status automatically saved to browser localStorage
- Automatically loads previous selections when reopened
- Clearing browser data will lose saved progress

## 🌐 Web Service Access

After starting the server, access through the following URLs:

- **Homepage**: http://localhost:8023
- **Chinese Interactive Version**: http://localhost:8023/interactive
- **English Interactive Version**: http://localhost:8023/interactive_en
- **Chinese Ultra-Clear Version**: http://localhost:8023/ultra
- **English Ultra-Clear Version**: http://localhost:8023/ultra_en
- **File List API**: http://localhost:8023/list

## 🔧 Custom Configuration

### Modify Data Model
Edit `resource/model_of_level.json` or `resource/model_of_level_en.json` files to customize capability data.

### Modify Server Configuration
Edit `server.py` file to modify port or other server settings:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

## 📝 Best Practices

### Personal Use
1. Use interactive version for capability self-assessment
2. Regularly (quarterly) reassess capability status
3. Use "Select All" function to visualize target state
4. Develop gap-based learning plans

### Team Use
1. Team members complete capability assessments separately
2. Aggregate team overall capability status
3. Identify capability gaps and development priorities
4. Develop team capability improvement plans

### Organizational Use
1. Teams complete capability assessments
2. Analyze organizational overall AI maturity
3. Develop phased capability development roadmaps
4. Regularly track and adjust development strategies

## 🛠️ Technology Stack

- **Backend**: Python + Flask
- **Frontend**: HTML + CSS + JavaScript
- **Charts**: Plotly.js
- **Data**: JSON format
- **Storage**: Browser localStorage

## 🤝 Contributing Guidelines

1. Fork this project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Create Pull Request

## 📄 License

This project uses MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

**Q: Flask not installed**
```bash
pip install flask
```

**Q: Port already in use**
Modify the port number in `server.py`, or stop the program occupying the port.

**Q: File not found**
Please run the generation script first to create HTML files.

**Q: Interactive version selections not saved**
Make sure to click the "Save Progress" button and that your browser supports localStorage.

### Technical Support

If you encounter issues, please:
1. Check relevant README documentation
2. Check browser console error messages
3. Confirm Python dependencies are correctly installed
4. Submit an Issue describing the specific problem

## 📞 Contact Information

For questions or suggestions, please contact through:
- Submit GitHub Issue
- Send email to project maintainers

---

**🎉 Start using the AI Maturity Model Visualization System to assess and improve your AI capabilities!** 