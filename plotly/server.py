from flask import Flask, send_file, render_template_string
import os
from pathlib import Path

app = Flask(__name__)

# 获取当前文件的目录
current_dir = Path(__file__).parent
outpt_dir = current_dir / 'output'

# 主页模板
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI SD Maturity Model Visualization</title>
    <style>
        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            padding: 40px;
            max-width: 800px;
            width: 90%;
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        .title {
            font-size: 2.5em;
            color: #333;
            margin-bottom: 10px;
            font-weight: bold;
        }
        .subtitle {
            font-size: 1.2em;
            color: #666;
            margin-bottom: 30px;
        }
        .charts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .chart-card {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            transition: all 0.3s ease;
            border: 2px solid transparent;
            cursor: pointer;
        }
        .chart-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            border-color: #667eea;
        }
        .chart-icon {
            font-size: 3em;
            margin-bottom: 15px;
        }
        .chart-title {
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }
        .chart-description {
            color: #666;
            font-size: 0.9em;
            line-height: 1.5;
            margin-bottom: 20px;
        }
        .chart-button {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 25px;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }
        .chart-button:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        .interactive-badge {
            background: #28a745;
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            margin-left: 10px;
        }
        .interactive-badge.english {
            background: #007bff;
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #666;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">🎯 AI Maturity Model Visualization</h1>
            <p class="subtitle">AI Software Delivery Capability Maturity Model - Multi-dimensional Display</p>
        </div>
        
        <div class="charts-grid">
            <div class="chart-card">
                <div class="chart-icon">🎯</div>
                <h3 class="chart-title">
                    Interactive Version
                </h3>
                <span class="interactive-badge english">Chinese</span>
                <p class="chart-description">
                    Includes sidebar checkbox functionality to track completed capabilities with progress saving. Best for practical use.
                </p>
                <a href="/interactive" class="chart-button">View Interactive Version</a>
            </div>
            
            <div class="chart-card">
                <div class="chart-icon">🌟</div>
                <h3 class="chart-title">Ultra Clean Layout Version</h3>
                <span class="interactive-badge english">Chinese</span>
                <p class="chart-description">
                    Uses layered display strategy with the clearest information layout, includes draggable reference lines, suitable for presentation and analysis.
                </p>
                <a href="/ultra" class="chart-button">View Ultra Clean Version</a>
            </div>
            
            <div class="chart-card">
                <div class="chart-icon">🔍</div>
                <h3 class="chart-title">
                    Interactive Version
                </h3>
                <span class="interactive-badge english">English</span>
                <p class="chart-description">
                    English interactive chart with sidebar checkbox functionality, suitable for international display and use.
                </p>
                <a href="/interactive_en" class="chart-button">View Interactive (EN)</a>
            </div>
            
            <div class="chart-card">
                <div class="chart-icon">👁️</div>
                <h3 class="chart-title">
                    Ultra Clean Layout Version
                </h3>
                <span class="interactive-badge english">English</span>
                <p class="chart-description">
                    English ultra clean layout chart with layered display strategy, suitable for international presentation and analysis.
                </p>
                <a href="/ultra_en" class="chart-button">View Ultra Clean (EN)</a>
            </div>
        </div>
        
        <div class="footer">
            <p>💡 Tip: <strong>Interactive Version</strong> is recommended as it provides the best user experience and functionality.</p>
            <p>🌐 Available in both Chinese and English versions to meet different user needs.</p>
            <p>🚀 Server running on <code>http://localhost:8023</code></p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """Home page - Display all available charts"""
    return render_template_string(HOME_TEMPLATE)

@app.route('/interactive')
def interactive():
    """Interactive version - with checkbox functionality"""
    file_path = outpt_dir / 'ai_sd_maturity_interactive.html'
    if file_path.exists():
        return send_file(file_path)
    else:
        return "File not found", 404

@app.route('/ultra')
def ultra():
    """Ultra clean layout version"""
    file_path = outpt_dir / 'ai_sd_maturity_overview_ultra.html'
    if file_path.exists():
        return send_file(file_path)
    else:
        return "File not found", 404

@app.route('/interactive_en')
def interactive_en():
    """Interactive version (English) - with checkbox functionality"""
    file_path = outpt_dir / 'ai_sd_maturity_interactive_en.html'
    if file_path.exists():
        return send_file(file_path)
    else:
        return "File not found", 404

@app.route('/ultra_en')
def ultra_en():
    """Ultra clean layout version (English)"""
    file_path = outpt_dir / 'ai_sd_maturity_ultra_en.html'
    if file_path.exists():
        return send_file(file_path)
    else:
        return "File not found", 404

@app.route('/list')
def list_files():
    """List all available files"""
    files = []
    if outpt_dir.exists():
        for file in outpt_dir.glob('*.html'):
            files.append({
                'name': file.name,
                'size': f"{file.stat().st_size / 1024 / 1024:.1f}MB"
            })
    
    return {
        'files': files,
        'total': len(files)
    }

if __name__ == '__main__':
    print("🚀 Starting AI Maturity Model Visualization Server...")
    print("📁 Service Directory:", outpt_dir)
    print("🌐 Access URL: http://localhost:8023")
    print("📊 Available Routes:")
    print("   - /              Home page (Recommended starting point)")
    print("   - /interactive   Interactive version (Chinese, Recommended)")
    print("   - /ultra         Ultra clean layout version (Chinese)")
    print("   - /interactive_en Interactive version (English)")
    print("   - /ultra_en      Ultra clean layout version (English)")
    print("   - /list          File list API")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=8023) 