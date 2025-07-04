import argparse
import json
import os
import sys

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def load_maturity_data(file_path):
    """加载AI成熟度模型数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_capabilities_data(data):
    """生成能力数据的JSON格式，供JavaScript使用"""
    capabilities_data = {}
    
    levels = list(data['levels'].keys())
    for level in levels:
        level_data = data['levels'][level]
        if 'capabilities' in level_data:
            for capability_type, capabilities in level_data['capabilities'].items():
                if capability_type not in capabilities_data:
                    capabilities_data[capability_type] = {}
                capabilities_data[capability_type][level] = capabilities
    
    return capabilities_data

def create_interactive_html_template():
    """创建交互式HTML模板"""
    template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>AI软件交付能力成熟度模型 - 交互式版本</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            background-color: #f5f5f5;
        }
        
        .sidebar {
            width: 350px;
            background-color: white;
            padding: 20px;
            box-shadow: 2px 0 5px rgba(0,0,0,0.1);
            height: 100vh;
            overflow-y: auto;
            position: fixed;
            left: 0;
            top: 0;
            z-index: 1000;
        }
        
        .main-content {
            margin-left: 350px;
            flex: 1;
            padding: 5px;
            overflow: hidden;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .sidebar h2 {
            color: #333;
            margin-top: 0;
            font-size: 18px;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }
        
        .capability-group {
            margin-bottom: 25px;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            background-color: #fafafa;
        }
        
        .capability-group h3 {
            margin: 0 0 10px 0;
            font-size: 16px;
            color: #333;
        }
        
        .level-group {
            margin-bottom: 15px;
        }
        
        .level-title {
            font-weight: bold;
            color: #555;
            margin-bottom: 8px;
            font-size: 14px;
        }
        
        .capability-item {
            margin: 5px 0;
            display: flex;
            align-items: center;
        }
        
        .capability-checkbox {
            margin-right: 8px;
            transform: scale(1.2);
        }
        
        .capability-text {
            font-size: 13px;
            color: #666;
            line-height: 1.4;
        }
        
        .capability-text.completed {
            text-decoration: line-through;
            color: #999;
        }
        
        .controls {
            margin-bottom: 20px;
            padding: 15px;
            background-color: #e9ecef;
            border-radius: 8px;
        }
        
        .controls button {
            margin: 5px;
            padding: 8px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
        }
        
        .btn-primary {
            background-color: #007bff;
            color: white;
        }
        
        .btn-secondary {
            background-color: #6c757d;
            color: white;
        }
        
        .btn-success {
            background-color: #28a745;
            color: white;
        }
        
        .progress-info {
            margin-top: 15px;
            padding: 10px;
            background-color: #d1ecf1;
            border-radius: 4px;
            font-size: 14px;
        }
        
        .capability-group.人员能力 {
            border-left: 4px solid #FF6B6B;
        }
        
        .capability-group.流程能力 {
            border-left: 4px solid #4ECDC4;
        }
        
        .capability-group.技术能力 {
            border-left: 4px solid #45B7D1;
        }
        
        .capability-group.知识能力 {
            border-left: 4px solid #96CEB4;
        }
        
        .capability-group.治理能力 {
            border-left: 4px solid #FFEAA7;
        }
        
        .plotly-graph-div {
            width: 100% !important;
            height: calc(100vh - 20px) !important;
            min-height: 800px !important;
        }
        
        #plotly-div {
            flex: 1;
            width: 100%;
            height: 100%;
        }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>🎯 能力完成度跟踪</h2>
        
        <div class="controls">
            <button class="btn-primary" onclick="selectAll()">全选</button>
            <button class="btn-secondary" onclick="deselectAll()">全不选</button>
            <button class="btn-success" onclick="saveProgress()">保存进度</button>
        </div>
        
        <div class="progress-info">
            <div id="progress-text">已完成: 0 / 0 (0%)</div>
        </div>
        
        <div id="capabilities-container">
            <!-- 能力列表将通过JavaScript动态生成 -->
        </div>
    </div>
    
    <div class="main-content">
        <div id="plotly-div">
            {plot_div}
        </div>
    </div>
    
    <script>
        // 能力数据
        const capabilitiesData = {capabilities_json};
        
        // 颜色映射
        const colors = {
            '人员能力': '#FF6B6B',
            '流程能力': '#4ECDC4', 
            '技术能力': '#45B7D1',
            '知识能力': '#96CEB4',
            '治理能力': '#FFEAA7'
        };
        
        // 初始化
        let completedCapabilities = new Set();
        
        // 从localStorage加载已完成的能力
        function loadProgress() {
            const saved = localStorage.getItem('ai_maturity_progress');
            if (saved) {
                completedCapabilities = new Set(JSON.parse(saved));
                updateCheckboxes();
                updateProgress();
            }
        }
        
        // 保存进度到localStorage
        function saveProgress() {
            localStorage.setItem('ai_maturity_progress', JSON.stringify([...completedCapabilities]));
            alert('进度已保存！');
        }
        
        // 生成能力列表HTML
        function generateCapabilitiesHTML() {
            const container = document.getElementById('capabilities-container');
            let html = '';
            
            for (const [capabilityType, levels] of Object.entries(capabilitiesData)) {
                html += `<div class="capability-group ${capabilityType}">`;
                html += `<h3>${capabilityType}</h3>`;
                
                for (const [level, capabilities] of Object.entries(levels)) {
                    html += `<div class="level-group">`;
                    html += `<div class="level-title">${level}</div>`;
                    
                    capabilities.forEach((capability, index) => {
                        const capabilityId = `${capabilityType}-${level}-${index}`;
                        html += `
                            <div class="capability-item">
                                <input type="checkbox" 
                                       class="capability-checkbox" 
                                       id="${capabilityId}" 
                                       onchange="toggleCapability('${capabilityId}', '${capability}')">
                                <label for="${capabilityId}" class="capability-text">${capability}</label>
                            </div>
                        `;
                    });
                    
                    html += `</div>`;
                }
                
                html += `</div>`;
            }
            
            container.innerHTML = html;
        }
        
        // 切换能力完成状态
        function toggleCapability(capabilityId, capabilityText) {
            const checkbox = document.getElementById(capabilityId);
            const label = checkbox.nextElementSibling;
            
            if (checkbox.checked) {
                completedCapabilities.add(capabilityId);
                label.classList.add('completed');
            } else {
                completedCapabilities.delete(capabilityId);
                label.classList.remove('completed');
            }
            
            updateProgress();
        }
        
        // 更新复选框状态
        function updateCheckboxes() {
            completedCapabilities.forEach(capabilityId => {
                const checkbox = document.getElementById(capabilityId);
                const label = checkbox ? checkbox.nextElementSibling : null;
                if (checkbox) {
                    checkbox.checked = true;
                    if (label) label.classList.add('completed');
                }
            });
        }
        
        // 更新进度显示
        function updateProgress() {
            const totalCapabilities = document.querySelectorAll('.capability-checkbox').length;
            const completedCount = completedCapabilities.size;
            const percentage = totalCapabilities > 0 ? Math.round((completedCount / totalCapabilities) * 100) : 0;
            
            document.getElementById('progress-text').textContent = 
                `已完成: ${completedCount} / ${totalCapabilities} (${percentage}%)`;
        }
        
        // 全选
        function selectAll() {
            document.querySelectorAll('.capability-checkbox').forEach(checkbox => {
                if (!checkbox.checked) {
                    checkbox.checked = true;
                    completedCapabilities.add(checkbox.id);
                    checkbox.nextElementSibling.classList.add('completed');
                }
            });
            updateProgress();
        }
        
        // 全不选
        function deselectAll() {
            document.querySelectorAll('.capability-checkbox').forEach(checkbox => {
                if (checkbox.checked) {
                    checkbox.checked = false;
                    completedCapabilities.delete(checkbox.id);
                    checkbox.nextElementSibling.classList.remove('completed');
                }
            });
            updateProgress();
        }
        
        // 页面加载完成后初始化
        document.addEventListener('DOMContentLoaded', function() {
            generateCapabilitiesHTML();
            loadProgress();
        });
    </script>
</body>
</html>
    """
    return template

def create_fishbone_diagram(data):
    """创建鱼骨图"""
    fig = go.Figure()
    
    # 定义颜色方案
    colors = {
        '人员能力': '#FF6B6B',
        '流程能力': '#4ECDC4', 
        '技术能力': '#45B7D1',
        '知识能力': '#96CEB4',
        '治理能力': '#FFEAA7'
    }
    
    # 能力维度的Y坐标
    capability_positions = {
        '人员能力': 2,
        '流程能力': 1,
        '技术能力': 0,
        '知识能力': -1,
        '治理能力': -2
    }
    
    # 绘制主干线（水平线）
    fig.add_trace(go.Scatter(
        x=[0, 4.8],
        y=[0, 0],
        mode='lines',
        line=dict(color='black', width=4),
        name='AI成熟度演进主线',
        hovertemplate='AI成熟度演进主线<extra></extra>'
    ))
    
    # 在主干线末尾添加向右的箭头
    fig.add_annotation(
        x=4.8,
        y=0,
        text='▶',
        showarrow=False,
        font=dict(size=20, color='black'),
        xanchor='left',
        yanchor='middle'
    )
    
    # 添加成熟度级别标记点
    levels = list(data['levels'].keys())
    level_names = [data['levels'][level]['title'] for level in levels]
    
    fig.add_trace(go.Scatter(
        x=list(range(len(levels))),
        y=[0] * len(levels),
        mode='markers+text',
        marker=dict(size=12, color='red', symbol='circle'),
        text=level_names,
        textposition='top center',
        name='成熟度级别',
        hovertemplate='%{text}<br>级别: %{x}<extra></extra>'
    ))
    
    # 为每个能力维度绘制分支
    for capability_type, y_pos in capability_positions.items():
        color = colors[capability_type]
        
        # 收集该维度在各级别的能力数据
        capability_data = []
        for i, level in enumerate(levels):
            level_data = data['levels'][level]
            if 'capabilities' in level_data and capability_type in level_data['capabilities']:
                capabilities = level_data['capabilities'][capability_type]
                capability_data.append({
                    'level': i,
                    'level_name': level,
                    'capabilities': capabilities,
                    'count': len(capabilities)
                })
        
        # 绘制主分支线（从主干到各级别）
        for item in capability_data:
            # 从主干线到能力维度的连接线
            fig.add_trace(go.Scatter(
                x=[item['level'], item['level']],
                y=[0, y_pos],
                mode='lines',
                line=dict(color=color, width=2),
                showlegend=False,
                hovertemplate=f'{capability_type}<br>级别: {item["level_name"]}<extra></extra>'
            ))
            
            # 能力维度的端点
            hover_text = f"<b>{capability_type}</b><br>级别: {item['level_name']}<br>能力数量: {item['count']}<br><br>具体能力:<br>"
            hover_text += "<br>".join([f"• {cap}" for cap in item['capabilities']])
            
            fig.add_trace(go.Scatter(
                x=[item['level']],
                y=[y_pos],
                mode='markers',
                marker=dict(size=8, color=color),
                name=capability_type if item == capability_data[0] else None,
                showlegend=item == capability_data[0],
                hovertemplate=hover_text + '<extra></extra>'
            ))
    
    # 添加能力维度标签
    for capability_type, y_pos in capability_positions.items():
        fig.add_annotation(
            x=-0.5,
            y=y_pos,
            text=capability_type,
            showarrow=False,
            font=dict(size=12, color=colors[capability_type]),
            xanchor='right'
        )
    
    # 设置布局
    fig.update_layout(
        title={
            'text': 'AI成熟度模型鱼骨图',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        xaxis=dict(
            title='成熟度级别',
            tickmode='array',
            tickvals=list(range(len(levels))),
            ticktext=levels,
            range=[-1, 6]
        ),
        yaxis=dict(
            title='能力维度',
            tickmode='array',
            tickvals=list(capability_positions.values()),
            ticktext=list(capability_positions.keys()),
            range=[-3, 3]
        ),
        width=1200,
        height=800,
        showlegend=True,
        legend=dict(
            x=1.02,
            y=1,
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='rgba(0, 0, 0, 0.2)',
            borderwidth=1
        ),
        hovermode='closest',
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    # 添加网格
    fig.update_xaxes(showgrid=True, gridcolor='lightgray', gridwidth=1)
    fig.update_yaxes(showgrid=True, gridcolor='lightgray', gridwidth=1)
    
    return fig

def create_detailed_fishbone_diagram(data):
    """创建详细版鱼骨图，包含更多信息"""
    fig = make_subplots(
        rows=1, cols=1,
        subplot_titles=('AI成熟度模型详细鱼骨图',)
    )
    
    # 基本配置同上，但添加更多细节
    colors = {
        '人员能力': '#FF6B6B',
        '流程能力': '#4ECDC4', 
        '技术能力': '#45B7D1',
        '知识能力': '#96CEB4',
        '治理能力': '#FFEAA7'
    }
    
    capability_positions = {
        '人员能力': 2.5,
        '流程能力': 1.2,
        '技术能力': 0,
        '知识能力': -1.2,
        '治理能力': -2.5
    }
    
    # 绘制主干线
    fig.add_trace(go.Scatter(
        x=[0, 4.8],
        y=[0, 0],
        mode='lines',
        line=dict(color='black', width=5),
        name='AI成熟度演进主线'
    ))
    
    # 在主干线末尾添加向右的箭头
    fig.add_annotation(
        x=4.8,
        y=0,
        text='▶',
        showarrow=False,
        font=dict(size=20, color='black'),
        xanchor='left',
        yanchor='middle'
    )
    
    levels = list(data['levels'].keys())
    
    # 为每个级别添加详细信息
    for i, level in enumerate(levels):
        level_data = data['levels'][level]
        
        # 添加级别主节点
        fig.add_trace(go.Scatter(
            x=[i],
            y=[0],
            mode='markers+text',
            marker=dict(size=15, color='darkred', symbol='diamond'),
            text=[level],
            textposition='top center',
            name=f'级别 {level}',
            hovertemplate=f'<b>{level_data["title"]}</b><br>{level_data["description"]}<br><br>特征: {level_data["features"]}<extra></extra>'
        ))
        
        # 为每个能力维度添加详细分支
        if 'capabilities' in level_data:
            for capability_type, capabilities in level_data['capabilities'].items():
                if capability_type in capability_positions:
                    y_pos = capability_positions[capability_type]
                    color = colors[capability_type]
                    
                    # 主分支
                    fig.add_trace(go.Scatter(
                        x=[i, i],
                        y=[0, y_pos],
                        mode='lines',
                        line=dict(color=color, width=3),
                        showlegend=False
                    ))
                    
                    # 子分支 - 每个具体能力
                    for j, capability in enumerate(capabilities):
                        offset = (j - len(capabilities)/2) * 0.3
                        sub_y = y_pos + offset * 0.3
                        
                        # 子分支线
                        fig.add_trace(go.Scatter(
                            x=[i, i + 0.3],
                            y=[y_pos, sub_y],
                            mode='lines',
                            line=dict(color=color, width=1),
                            showlegend=False
                        ))
                        
                        # 能力点
                        fig.add_trace(go.Scatter(
                            x=[i + 0.3],
                            y=[sub_y],
                            mode='markers',
                            marker=dict(size=6, color=color),
                            showlegend=False,
                            hovertemplate=f'<b>{capability}</b><br>维度: {capability_type}<br>级别: {level}<extra></extra>'
                        ))
    
    # 添加维度标签
    for capability_type, y_pos in capability_positions.items():
        fig.add_annotation(
            x=-0.5,
            y=y_pos,
            text=f'<b>{capability_type}</b>',
            showarrow=True,
            arrowhead=2,
            arrowcolor=colors[capability_type],
            font=dict(size=14, color=colors[capability_type]),
            xanchor='right'
        )
    
    fig.update_layout(
        title={
            'text': 'AI成熟度模型详细鱼骨图',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 22}
        },
        xaxis=dict(
            title='成熟度级别',
            tickmode='array',
            tickvals=list(range(len(levels))),
            ticktext=levels,
            range=[-1, 6]
        ),
        yaxis=dict(
            title='能力维度',
            range=[-3.5, 3.5]
        ),
        width=1400,
        height=1000,
        showlegend=False,
        hovermode='closest',
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

def create_static_fishbone_diagram(data):
    """创建静态信息展示的鱼骨图，所有信息直接显示在页面上"""
    fig = go.Figure()
    
    # 定义颜色方案
    colors = {
        '人员能力': '#FF6B6B',
        '流程能力': '#4ECDC4', 
        '技术能力': '#45B7D1',
        '知识能力': '#96CEB4',
        '治理能力': '#FFEAA7'
    }
    
    # 能力维度的Y坐标（紧凑间距）
    capability_positions = {
        '人员能力': 4,
        '流程能力': 2,
        '技术能力': -2,
        '知识能力': -4,
        '治理能力': -6
    }
    
    # 绘制主干线（水平线）
    fig.add_trace(go.Scatter(
        x=[0, 11.7],
        y=[0, 0],
        mode='lines',
        line=dict(color='black', width=4),
        name='AI成熟度演进主线',
        showlegend=False
    ))
    
    # 在主干线末尾添加向右的箭头
    fig.add_annotation(
        x=11.7,
        y=0,
        text='▶',
        showarrow=False,
        font=dict(size=20, color='black'),
        xanchor='left',
        yanchor='middle'
    )
    
    # 添加成熟度级别标记点和标签
    levels = list(data['levels'].keys())
    level_names = [data['levels'][level]['title'] for level in levels]
    
    # 适中的X轴间距 - 根据实际级别数量动态生成，避免重叠
    x_positions = [2 + i * 3 for i in range(len(levels))]  # 每个级别之间间隔3个单位
    
    fig.add_trace(go.Scatter(
        x=x_positions,
        y=[0] * len(levels),
        mode='markers+text',
        marker=dict(size=15, color='red', symbol='circle'),
        text=level_names,
        textposition='top center',
        textfont=dict(size=12, color='darkred'),
        name='成熟度级别',
        showlegend=False
    ))
    
    # 为每个能力维度绘制分支和详细信息
    for capability_type, y_pos in capability_positions.items():
        color = colors[capability_type]
        
        # 添加能力维度主标签 - 进一步向右移动
        fig.add_annotation(
            x=1,  # 进一步向右移动
            y=y_pos,
            text=f'<b>{capability_type}</b>',
            showarrow=False,
            font=dict(size=16, color=color),
            xanchor='right',
            yanchor='middle',  # 垂直居中对齐
            bgcolor='rgba(255, 255, 255, 0.9)',
            bordercolor=color,
            borderwidth=2
        )
        
        # 收集该维度在各级别的能力数据
        for i, level in enumerate(levels):
            level_data = data['levels'][level]
            if 'capabilities' in level_data and capability_type in level_data['capabilities']:
                capabilities = level_data['capabilities'][capability_type]
                x_pos = x_positions[i]
                
                # 绘制从主干到能力维度的连接线
                fig.add_trace(go.Scatter(
                    x=[x_pos, x_pos],
                    y=[0, y_pos],
                    mode='lines',
                    line=dict(color=color, width=2),
                    showlegend=False
                ))
                
                # 能力维度的端点
                fig.add_trace(go.Scatter(
                    x=[x_pos],
                    y=[y_pos],
                    mode='markers',
                    marker=dict(size=10, color=color),
                    showlegend=False
                ))
                
                # 在图表上直接显示具体能力 - 直接放在节点位置
                capabilities_text = '<br>'.join([f'• {cap}' for cap in capabilities])
                
                fig.add_annotation(
                    x=x_pos,
                    y=y_pos,
                    text=capabilities_text,
                    showarrow=False,  # 不显示箭头
                    font=dict(size=9, color='black'),
                    bgcolor='rgba(255, 255, 255, 0.95)',
                    bordercolor=color,
                    borderwidth=1,
                    align='left',
                    width=220,  # 适中的文本框宽度
                    xanchor='center',  # 水平居中
                    yanchor='middle'   # 垂直居中
                )
    
    # 添加级别描述信息 - 紧凑布局
    for i, level in enumerate(levels):
        level_data = data['levels'][level]
        description_text = f"<b>{level_data['title']}</b><br>{level_data['description']}<br><br>特征: {level_data['features']}"
        x_pos = x_positions[i]
        
        fig.add_annotation(
            x=x_pos,
            y=7,  # 紧凑的位置
            text=description_text,
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowcolor='darkred',
            ax=0,
            ay=-30,
            font=dict(size=8, color='darkred'),
            bgcolor='rgba(255, 255, 255, 0.95)',
            bordercolor='darkred',
            borderwidth=1,
            align='left',
            width=180  # 限制文本框宽度
        )
    
    # 添加可移动的参考线
    # 行业位置线（初始位置在L2和L3之间）
    industry_position = (x_positions[1] + x_positions[2]) / 2
    # 组织位置线（初始位置在L1和L2之间）
    organization_position = (x_positions[0] + x_positions[1]) / 2
    
    # 设置布局 - 大幅增加画布尺寸
    fig.update_layout(
        title={
            'text': 'AI成熟度模型鱼骨图 - 静态信息展示版（优化布局）',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 22}
        },
        xaxis=dict(
            title='成熟度级别',
            tickmode='array',
            tickvals=x_positions,
            ticktext=levels,
            range=[0, max(x_positions) + 1]
        ),
        yaxis=dict(
            title='能力维度',
            showticklabels=False,  # 隐藏Y轴标签，只保留有颜色的标签
            range=[-8, 10]  # 紧凑的Y轴范围
        ),
        width=1600,  # 优化宽度以适应一屏显示
        height=1000,  # 保持高度
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=80, r=80, t=80, b=80),  # 紧凑边距
        # 添加可拖拽的参考线
        shapes=[
            # 行业位置线
            dict(
                type="line",
                x0=industry_position,
                y0=-8,
                x1=industry_position,
                y1=10,
                line=dict(
                    color="orange",
                    width=3,
                    dash="dash"
                ),
                editable=True,
                name="行业位置"
            ),
            # 组织位置线
            dict(
                type="line",
                x0=organization_position,
                y0=-8,
                x1=organization_position,
                y1=10,
                line=dict(
                    color="purple",
                    width=3,
                    dash="dash"
                ),
                editable=True,
                name="组织位置"
            )
        ],
        # 添加注释说明
        annotations=list(fig.layout.annotations) + [
            dict(
                x=industry_position,
                y=8.5,
                text="<b>行业位置</b><br>(可拖拽)",
                showarrow=True,
                arrowhead=2,
                arrowcolor="orange",
                font=dict(size=11, color="orange"),
                bgcolor="rgba(255, 255, 255, 0.9)",
                bordercolor="orange",
                borderwidth=2,
                ax=0,
                ay=-25
            ),
            dict(
                x=organization_position,
                y=8.5,
                text="<b>组织位置</b><br>(可拖拽)",
                showarrow=True,
                arrowhead=2,
                arrowcolor="purple",
                font=dict(size=11, color="purple"),
                bgcolor="rgba(255, 255, 255, 0.9)",
                bordercolor="purple",
                borderwidth=2,
                ax=0,
                ay=-25
            )
        ]
    )
    
    # 添加网格
    fig.update_xaxes(showgrid=True, gridcolor='lightgray', gridwidth=1)
    fig.update_yaxes(showgrid=True, gridcolor='lightgray', gridwidth=1)
    
    return fig

def create_ultra_clean_fishbone_diagram(data):
    """创建超清晰布局的鱼骨图，采用分层显示策略"""
    fig = go.Figure()
    
    # 定义颜色方案
    colors = {
        '人员能力': '#FF6B6B',
        '流程能力': '#4ECDC4', 
        '技术能力': '#45B7D1',
        '知识能力': '#96CEB4',
        '治理能力': '#FFEAA7'
    }
    
    # 能力维度的Y坐标（紧凑间距）
    capability_positions = {
        '人员能力': 4,
        '流程能力': 2,
        '技术能力': -2,
        '知识能力': -4,
        '治理能力': -6
    }
    
    levels = list(data['levels'].keys())
    level_names = [data['levels'][level]['title'] for level in levels]
    
    # X轴位置 - 适中的间距，避免重叠
    x_positions = [3 + i * 4 for i in range(len(levels))]
    
    # 绘制主干线（水平线）
    fig.add_trace(go.Scatter(
        x=[0, max(x_positions) + 2.7],
        y=[0, 0],
        mode='lines',
        line=dict(color='black', width=5),
        name='AI成熟度演进主线',
        showlegend=False
    ))
    
    # 在主干线末尾添加向右的箭头
    fig.add_annotation(
        x=max(x_positions) + 2.7,
        y=0,
        text='▶',
        showarrow=False,
        font=dict(size=20, color='black'),
        xanchor='left',
        yanchor='middle'
    )
    
    # 添加成熟度级别标记点
    fig.add_trace(go.Scatter(
        x=x_positions,
        y=[0] * len(levels),
        mode='markers+text',
        marker=dict(size=20, color='darkred', symbol='diamond'),
        text=level_names,
        textposition='top center',
        textfont=dict(size=14, color='darkred'),
        name='成熟度级别',
        showlegend=False
    ))
    
    # 为每个能力维度绘制分支
    for capability_type, y_pos in capability_positions.items():
        color = colors[capability_type]
        
        # 添加能力维度主标签（更大更醒目）- 进一步向右移动
        fig.add_annotation(
            x=0.5,  # 进一步向右移动
            y=y_pos,
            text=f'<b>{capability_type}</b>',
            showarrow=False,
            font=dict(size=20, color=color),
            xanchor='right',
            yanchor='middle',  # 垂直居中对齐
            bgcolor='rgba(255, 255, 255, 0.95)',
            bordercolor=color,
            borderwidth=3
        )
        
        # 为每个级别绘制该维度的信息
        for i, level in enumerate(levels):
            level_data = data['levels'][level]
            if 'capabilities' in level_data and capability_type in level_data['capabilities']:
                capabilities = level_data['capabilities'][capability_type]
                x_pos = x_positions[i]
                
                # 绘制连接线
                fig.add_trace(go.Scatter(
                    x=[x_pos, x_pos],
                    y=[0, y_pos],
                    mode='lines',
                    line=dict(color=color, width=3),
                    showlegend=False
                ))
                
                # 端点
                fig.add_trace(go.Scatter(
                    x=[x_pos],
                    y=[y_pos],
                    mode='markers',
                    marker=dict(size=12, color=color),
                    showlegend=False
                ))
                
                # 能力详情文本框 - 直接放在节点位置，不偏移
                capabilities_text = '<br>'.join([f'• {cap}' for cap in capabilities])
                
                fig.add_annotation(
                    x=x_pos,
                    y=y_pos,
                    text=capabilities_text,
                    showarrow=False,  # 不显示箭头
                    font=dict(size=10, color='black'),
                    bgcolor='rgba(255, 255, 255, 0.98)',
                    bordercolor=color,
                    borderwidth=2,
                    align='left',
                    width=280,  # 增加文本框宽度以适应更大的间距
                    xanchor='center',  # 水平居中
                    yanchor='middle'   # 垂直居中
                )
    
    # 在顶部添加级别描述信息 - 紧凑布局
    description_y = 7
    for i, level in enumerate(levels):
        level_data = data['levels'][level]
        description_text = f"<b>{level_data['title']}</b><br><br>{level_data['description']}<br><br><b>特征:</b> {level_data['features']}"
        x_pos = x_positions[i]
        
        fig.add_annotation(
            x=x_pos,
            y=description_y,
            text=description_text,
            showarrow=True,
            arrowhead=2,
            arrowsize=1.5,
            arrowcolor='darkred',
            arrowwidth=2,
            ax=0,
            ay=-40,
            font=dict(size=9, color='darkred'),
            bgcolor='rgba(255, 248, 248, 0.98)',
            bordercolor='darkred',
            borderwidth=2,
            align='left',
            width=200,
            standoff=10
        )
    
    # 添加可移动的参考线
    # 行业位置线（初始位置在L2和L3之间）
    industry_position = (x_positions[1] + x_positions[2]) / 2
    # 组织位置线（初始位置在L1和L2之间）
    organization_position = (x_positions[0] + x_positions[1]) / 2
    
    # 设置布局
    fig.update_layout(
        title={
            'text': 'AI软件交付能力成熟度模型全景图',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': 'darkblue'}
        },
        xaxis=dict(
            title=dict(text='成熟度级别', font=dict(size=16)),
            tickmode='array',
            tickvals=x_positions,
            ticktext=levels,
            tickfont=dict(size=14),
            range=[-1, max(x_positions) + 2],
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=1
        ),
        yaxis=dict(
            title=dict(text='能力维度', font=dict(size=16)),
            tickfont=dict(size=14),
            showticklabels=False,  # 隐藏Y轴标签，只保留有颜色的标签
            range=[-10, 10],
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=1
        ),
        width=1900,  # 优化宽度以适应一屏显示
        height=1200,  # 保持高度
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=100, r=100, t=100, b=100),
        # 添加可拖拽的参考线
        shapes=[
            # 行业位置线
            dict(
                type="line",
                x0=industry_position,
                y0=-10,
                x1=industry_position,
                y1=10,
                line=dict(
                    color="orange",
                    width=3,
                    dash="dash"
                ),
                editable=True,
                name="行业位置"
            ),
            # 组织位置线
            dict(
                type="line",
                x0=organization_position,
                y0=-10,
                x1=organization_position,
                y1=10,
                line=dict(
                    color="purple",
                    width=3,
                    dash="dash"
                ),
                editable=True,
                name="组织位置"
            )
        ],
        # 添加注释说明
        annotations=list(fig.layout.annotations) + [
            dict(
                x=industry_position,
                y=9,
                text="<b>行业位置</b><br>(可拖拽)",
                showarrow=True,
                arrowhead=2,
                arrowcolor="orange",
                font=dict(size=12, color="orange"),
                bgcolor="rgba(255, 255, 255, 0.9)",
                bordercolor="orange",
                borderwidth=2,
                ax=0,
                ay=-30
            ),
            dict(
                x=organization_position,
                y=9,
                text="<b>组织位置</b><br>(可拖拽)",
                showarrow=True,
                arrowhead=2,
                arrowcolor="purple",
                font=dict(size=12, color="purple"),
                bgcolor="rgba(255, 255, 255, 0.9)",
                bordercolor="purple",
                borderwidth=2,
                ax=0,
                ay=-30
            )
        ]
    )
    
    return fig

def create_interactive_fishbone_diagram(data):
    """创建带有checkbox功能的交互式鱼骨图"""
    fig = go.Figure()
    
    # 定义颜色方案
    colors = {
        '人员能力': '#FF6B6B',
        '流程能力': '#4ECDC4', 
        '技术能力': '#45B7D1',
        '知识能力': '#96CEB4',
        '治理能力': '#FFEAA7'
    }
    
    # 能力维度的Y坐标
    capability_positions = {
        '人员能力': 4,
        '流程能力': 2,
        '技术能力': -2,
        '知识能力': -4,
        '治理能力': -6
    }
    
    levels = list(data['levels'].keys())
    level_names = [data['levels'][level]['title'] for level in levels]
    
    # X轴位置 - 优化间距以更好利用右侧空间
    x_positions = [2 + i * 3.5 for i in range(len(levels))]
    
    # 绘制主干线 - 调整长度以适应新的X轴范围
    fig.add_trace(go.Scatter(
        x=[-0.5, max(x_positions) + 1.2],
        y=[0, 0],
        mode='lines',
        line=dict(color='black', width=5),
        name='AI成熟度演进主线',
        showlegend=False
    ))
    
    # 在主干线末尾添加向右的箭头
    arrow_x = max(x_positions) + 1.2
    fig.add_annotation(
        x=arrow_x,
        y=0,
        text='▶',
        showarrow=False,
        font=dict(size=20, color='black'),
        xanchor='left',
        yanchor='middle'
    )
    
    # 添加成熟度级别标记点
    fig.add_trace(go.Scatter(
        x=x_positions,
        y=[0] * len(levels),
        mode='markers+text',
        marker=dict(size=20, color='darkred', symbol='diamond'),
        text=level_names,
        textposition='top center',
        textfont=dict(size=14, color='darkred'),
        name='成熟度级别',
        showlegend=False
    ))
    
    # 为每个能力维度绘制分支
    for capability_type, y_pos in capability_positions.items():
        color = colors[capability_type]
        
        # 添加能力维度主标签
        fig.add_annotation(
            x=-0.3,
            y=y_pos,
            text=f'<b>{capability_type}</b>',
            showarrow=False,
            font=dict(size=16, color=color),
            xanchor='right',
            yanchor='middle',
            bgcolor='rgba(255, 255, 255, 0.95)',
            bordercolor=color,
            borderwidth=2
        )
        
        # 为每个级别绘制该维度的信息
        for i, level in enumerate(levels):
            level_data = data['levels'][level]
            if 'capabilities' in level_data and capability_type in level_data['capabilities']:
                capabilities = level_data['capabilities'][capability_type]
                x_pos = x_positions[i]
                
                # 绘制连接线
                fig.add_trace(go.Scatter(
                    x=[x_pos, x_pos],
                    y=[0, y_pos],
                    mode='lines',
                    line=dict(color=color, width=3),
                    showlegend=False
                ))
                
                # 端点
                fig.add_trace(go.Scatter(
                    x=[x_pos],
                    y=[y_pos],
                    mode='markers',
                    marker=dict(size=12, color=color),
                    showlegend=False
                ))
                
                # 简化的能力信息显示（因为详细信息在侧边栏）
                fig.add_annotation(
                    x=x_pos,
                    y=y_pos,
                    text=f'共{len(capabilities)}项能力<br>详见侧边栏',
                    showarrow=False,
                    font=dict(size=10, color='black'),
                    bgcolor='rgba(255, 255, 255, 0.98)',
                    bordercolor=color,
                    borderwidth=2,
                    align='center',
                    width=120,
                    xanchor='center',
                    yanchor='middle'
                )
    
    # 在顶部添加级别描述信息 - 调整位置避免重叠
    description_y = 10
    for i, level in enumerate(levels):
        level_data = data['levels'][level]
        description_text = f"<b>{level_data['title']}</b><br><br>{level_data['description']}<br><br><b>特征:</b> {level_data['features']}"
        x_pos = x_positions[i]
        
        fig.add_annotation(
            x=x_pos,
            y=description_y,
            text=description_text,
            showarrow=True,
            arrowhead=2,
            arrowsize=1.2,
            arrowcolor='darkred',
            arrowwidth=2,
            ax=0,
            ay=-50,
            font=dict(size=8, color='darkred'),
            bgcolor='rgba(255, 248, 248, 0.98)',
            bordercolor='darkred',
            borderwidth=1,
            align='left',
            width=180,
            standoff=5
        )
    
    # 设置布局
    fig.update_layout(
        title={
            'text': 'AI软件交付成熟度模型 - 交互式版本（左侧可勾选已完成能力）',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': 'darkblue'}
        },
        xaxis=dict(
            title=dict(text='成熟度级别', font=dict(size=14)),
            tickmode='array',
            tickvals=x_positions,
            ticktext=levels,
            tickfont=dict(size=12),
            range=[-1.0, max(x_positions) + 1.5],
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=1
        ),
        yaxis=dict(
            title=dict(text=''),  # 清空默认标题，用annotation替代
            tickfont=dict(size=12),
            showticklabels=False,
            range=[-8, 12],
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=1
        ),
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=80, r=20, t=60, b=40),
        autosize=True
    )
    
    # 添加与主干线对齐的Y轴标题
    fig.add_annotation(
        x=-0.8,
        y=0,
        text='<b>能力维度</b>',
        showarrow=False,
        font=dict(size=14, color='black'),
        xanchor='center',
        yanchor='middle',
        textangle=-90,  # 垂直显示
        bgcolor='rgba(255, 255, 255, 0.8)',
        bordercolor='gray',
        borderwidth=1
    )
    
    return fig

def main(version='all'):
    """主函数
    
    Args:
        version (str): 指定生成的版本
            - 'all': 生成所有版本（默认）
            - 'basic': 基础版本
            - 'detailed': 详细版本
            - 'static': 静态展示版本
            - 'ultra': 超清晰布局版本
            - 'interactive': 交互式版本（带checkbox）
    """
    # 创建输出目录
    output_dir = '../output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"已创建输出目录: {output_dir}")
    
    # 加载数据
    data = load_maturity_data('../../resource/model_of_level.json')
    
    generated_files = []
    
    if version == 'all' or version == 'basic':
        # 创建基础鱼骨图
        print("正在生成基础版本...")
        fig1 = create_fishbone_diagram(data)
        fig1.show()
        output_file = os.path.join(output_dir, 'ai_sd_maturity_basic.html')
        fig1.write_html(output_file)
        generated_files.append(f"- 基础版本: {output_file}")
    
    if version == 'all' or version == 'detailed':
        # 创建详细鱼骨图
        print("正在生成详细版本...")
        fig2 = create_detailed_fishbone_diagram(data)
        fig2.show()
        output_file = os.path.join(output_dir, 'ai_sd_maturity_detailed.html')
        fig2.write_html(output_file)
        generated_files.append(f"- 详细版本: {output_file}")
    
    if version == 'all' or version == 'static':
        # 创建静态信息展示鱼骨图
        print("正在生成静态展示版本...")
        fig3 = create_static_fishbone_diagram(data)
        fig3.show()
        output_file = os.path.join(output_dir, 'ai_sd_maturity_static.html')
        fig3.write_html(output_file, 
                        config={'editable': True, 'toImageButtonOptions': {'format': 'png', 'filename': 'ai_maturity_fishbone_static', 'height': 1000, 'width': 1600, 'scale': 1}})
        generated_files.append(f"- 静态展示版本: {output_file}")
    
    if version == 'all' or version == 'ultra':
        # 创建超清晰布局鱼骨图
        print("正在生成超清晰布局版本...")
        fig4 = create_ultra_clean_fishbone_diagram(data)
        fig4.show()
        output_file = os.path.join(output_dir, 'ai_sd_maturity_overview_ultra.html')
        fig4.write_html(output_file, 
                        config={'editable': True, 'toImageButtonOptions': {'format': 'png', 'filename': 'ai_maturity_fishbone', 'height': 1200, 'width': 1900, 'scale': 1}})
        generated_files.append(f"- 超清晰布局版本: {output_file}")
    
    if version == 'all' or version == 'interactive':
        # 创建交互式鱼骨图（带checkbox）
        print("正在生成交互式版本（带checkbox）...")
        fig5 = create_interactive_fishbone_diagram(data)
        capabilities_data = generate_capabilities_data(data)
        
        # 先生成完整的HTML，然后保存为临时文件
        temp_file = os.path.join(output_dir, 'temp_plot.html')
        fig5.write_html(temp_file, include_plotlyjs='cdn')
        
        # 读取生成的HTML内容
        with open(temp_file, 'r', encoding='utf-8') as f:
            plot_html = f.read()
        
        # 删除临时文件
        os.remove(temp_file)
        
        # 提取body内容
        import re
        body_match = re.search(r'<body[^>]*>(.*?)</body>', plot_html, re.DOTALL)
        if body_match:
            plot_content = body_match.group(1).strip()
        else:
            plot_content = '<div id="plotly-div"></div>'
        
        # 使用自定义模板
        template = create_interactive_html_template()
        html_content = template.replace('{plot_div}', plot_content)
        html_content = html_content.replace('{capabilities_json}', json.dumps(capabilities_data, ensure_ascii=False))
        
        output_file = os.path.join(output_dir, 'ai_sd_maturity_interactive.html')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        generated_files.append(f"- 交互式版本（带checkbox）: {output_file}")
        print(f"交互式版本已生成: {output_file}")
    
    if not generated_files:
        print(f"错误：未知的版本参数 '{version}'")
        print("可用的版本参数：")
        print("- 'all': 生成所有版本")
        print("- 'basic': 基础版本")
        print("- 'detailed': 详细版本")  
        print("- 'static': 静态展示版本")
        print("- 'ultra': 超清晰布局版本")
        print("- 'interactive': 交互式版本（带checkbox）")
        return
    
    print(f"\n鱼骨图已生成完成！")
    for file_info in generated_files:
        print(file_info)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='生成AI成熟度模型鱼骨图')
    parser.add_argument(
        '--version', '-v', 
        choices=['all', 'basic', 'detailed', 'static', 'ultra', 'interactive'],
        default='all',
        help='指定生成的版本 (默认: all)'
    )
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='显示所有可用的版本'
    )
    
    args = parser.parse_args()
    
    if args.list:
        print("可用的版本：")
        print("- all: 生成所有版本（默认）")
        print("- basic: 基础版本")
        print("- detailed: 详细版本")
        print("- static: 静态展示版本（包含可拖拽参考线）")
        print("- ultra: 超清晰布局版本（包含可拖拽参考线）")
        print("- interactive: 交互式版本（带checkbox能力跟踪）")
        print("\n推荐使用 'interactive' 版本，它包含侧边栏checkbox让您可以跟踪已完成的能力。")
        sys.exit(0)
    
    main(args.version) 