#!/usr/bin/env python3
"""
AI成熟度模型可视化服务器启动脚本
"""

import subprocess
import sys
from pathlib import Path


def check_dependencies():
    """检查并安装依赖"""
    try:
        import flask
        print("✅ Flask 已安装")
        return True
    except ImportError:
        print("❌ Flask 未安装")
        
        # 询问用户是否自动安装
        response = input("是否自动安装 Flask？(y/n): ").lower().strip()
        if response in ['y', 'yes', '是']:
            try:
                print("正在安装 Flask...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'flask'])
                print("✅ Flask 安装成功")
                return True
            except subprocess.CalledProcessError:
                print("❌ Flask 安装失败，请手动安装：pip install flask")
                return False
        else:
            print("请手动安装依赖：pip install flask")
            return False

def main():
    """主函数"""
    print("🚀 AI成熟度模型可视化服务器")
    print("=" * 40)
    
    # 检查依赖
    if not check_dependencies():
        print("\n❌ 依赖检查失败，无法启动服务器")
        sys.exit(1)
    
    # 检查文件是否存在
    current_dir = Path(__file__).parent
    outpt_dir = current_dir / 'outpt'
    
    if not outpt_dir.exists():
        print(f"❌ 输出目录不存在: {outpt_dir}")
        print("请先运行 ai_maturity_fishbone_plotly.py 生成图表文件")
        sys.exit(1)
    
    # 检查HTML文件
    html_files = list(outpt_dir.glob('*.html'))
    if not html_files:
        print(f"❌ 在 {outpt_dir} 中没有找到HTML文件")
        print("请先运行 ai_maturity_fishbone_plotly.py 生成图表文件")
        sys.exit(1)
    
    print(f"✅ 找到 {len(html_files)} 个HTML文件")
    for file in html_files:
        size_mb = file.stat().st_size / 1024 / 1024
        print(f"   - {file.name} ({size_mb:.1f}MB)")
    
    print("\n🌐 启动服务器...")
    print("   访问地址: http://localhost:5000")
    print("   按 Ctrl+C 停止服务器")
    print("=" * 40)
    
    # 启动服务器
    try:
        from server import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"\n❌ 服务器启动失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 