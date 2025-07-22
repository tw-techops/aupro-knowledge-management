import argparse
import json
import os
import sys

import plotly.graph_objects as go


def load_maturity_data(file_path):
    """Load AI maturity model data"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_capabilities_data(data):
    """Generate capabilities data in JSON format for JavaScript usage"""
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
    """Create interactive HTML template"""
    template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>AI Maturity Model Fishbone Diagram - Interactive Version</title>
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
            width: 300px;
            background-color: white;
            padding: 15px;
            box-shadow: 2px 0 5px rgba(0,0,0,0.1);
            height: 100vh;
            overflow-y: auto;
            position: fixed;
            left: 0;
            top: 0;
            z-index: 1000;
        }
        
        .main-content {
            margin-left: 300px;
            flex: 1;
            padding: 20px;
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
        
        .capability-group[data-type="Personnel"] {
            border-left: 4px solid #FF6B6B;
        }
        
        .capability-group[data-type="Technical"] {
            border-left: 4px solid #45B7D1;
        }
        
        .capability-group[data-type="Process"] {
            border-left: 4px solid #4ECDC4;
        }
        
        .capability-group[data-type="Knowledge Management"] {
            border-left: 4px solid #96CEB4;
        }
        
        .capability-group[data-type="Governance"] {
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
        <h2>🎯 Capability Completion Tracking</h2>
        
        <div class="controls">
            <button class="btn-primary" onclick="selectAll()">Select All</button>
            <button class="btn-secondary" onclick="deselectAll()">Deselect All</button>
            <button class="btn-success" onclick="saveProgress()">Save Progress</button>
        </div>
        
        <div class="progress-info">
            <div id="progress-text">Completed: 0 / 0 (0%)</div>
        </div>
        
        <div id="capabilities-container">
            <!-- Capability list will be dynamically generated by JavaScript -->
        </div>
    </div>
    
    <div class="main-content">
        <div id="plotly-div">
            {plot_div}
        </div>
    </div>
    
    <script>
        // Capabilities data
        const capabilitiesData = {capabilities_json};
        
        // Color mapping
        const colors = {
            'Personnel': '#FF6B6B',
            'Technical': '#45B7D1',
            'Process': '#4ECDC4', 
            'Knowledge Management': '#96CEB4',
            'Governance': '#FFEAA7'
        };
        
        // Initialize
        let completedCapabilities = new Set();
        
        // Load completed capabilities from localStorage
        function loadProgress() {
            const saved = localStorage.getItem('ai_maturity_progress_en');
            if (saved) {
                completedCapabilities = new Set(JSON.parse(saved));
                updateCheckboxes();
                updateProgress();
            }
        }
        
        // Save progress to localStorage
        function saveProgress() {
            localStorage.setItem('ai_maturity_progress_en', JSON.stringify([...completedCapabilities]));
            alert('Progress saved!');
        }
        
        // Generate capabilities list HTML
        function generateCapabilitiesHTML() {
            const container = document.getElementById('capabilities-container');
            let html = '';
            
            for (const [capabilityType, levels] of Object.entries(capabilitiesData)) {
                html += `<div class="capability-group" data-type="${capabilityType}">`;
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
        
        // Toggle capability completion status
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
        
        // Update checkbox states
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
        
        // Update progress display
        function updateProgress() {
            const totalCapabilities = document.querySelectorAll('.capability-checkbox').length;
            const completedCount = completedCapabilities.size;
            const percentage = totalCapabilities > 0 ? Math.round((completedCount / totalCapabilities) * 100) : 0;
            
            document.getElementById('progress-text').textContent = 
                `Completed: ${completedCount} / ${totalCapabilities} (${percentage}%)`;
        }
        
        // Select all
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
        
        // Deselect all
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
        
        // Initialize after page load
        document.addEventListener('DOMContentLoaded', function() {
            generateCapabilitiesHTML();
            loadProgress();
        });
    </script>
</body>
</html>
    """
    return template

def create_ultra_clean_fishbone_diagram(data):
    """Create ultra-clean layout fishbone diagram with layered display strategy"""
    fig = go.Figure()
    
    # Define color scheme
    colors = {
        'Personnel': '#FF6B6B',
        'Technical': '#45B7D1',
        'Process': '#4ECDC4', 
        'Knowledge Management': '#96CEB4',
        'Governance': '#FFEAA7'
    }
    
    # Y-coordinates for capability dimensions (compact spacing)
    capability_positions = {
        'Personnel': 4,
        'Technical': 2,
        'Process': -2,
        'Knowledge Management': -4,
        'Governance': -6
    }
    
    levels = list(data['levels'].keys())
    level_names = [data['levels'][level]['title'] for level in levels]
    
    # X-axis positions - moderate spacing to avoid overlap
    x_positions = [3 + i * 4 for i in range(len(levels))]
    
    # Draw main trunk (horizontal line)
    fig.add_trace(go.Scatter(
        x=[0, max(x_positions) + 2.7],
        y=[0, 0],
        mode='lines',
        line=dict(color='black', width=5),
        name='AI Maturity Evolution Main Line',
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add right arrow at the end of main trunk
    fig.add_annotation(
        x=max(x_positions) + 2.7,
        y=0,
        text='▶',
        showarrow=False,
        font=dict(size=20, color='black'),
        xanchor='left',
        yanchor='middle'
    )
    
    # Add maturity level markers (without text)
    fig.add_trace(go.Scatter(
        x=x_positions,
        y=[0] * len(levels),
        mode='markers',
        marker=dict(size=20, color='darkred', symbol='diamond'),
        name='Maturity Levels',
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Draw branches for each capability dimension
    for capability_type, y_pos in capability_positions.items():
        color = colors[capability_type]
        
        # Add main capability dimension label (larger and more prominent)
        fig.add_annotation(
            x=-0.5,
            y=y_pos,
            text=f'<b>{capability_type}</b>',
            showarrow=False,
            font=dict(size=20, color=color),
            xanchor='right',
            yanchor='middle',
            bgcolor='rgba(255, 255, 255, 0.95)',
            bordercolor=color,
            borderwidth=3
        )
        
        # Draw information for each level in this dimension
        for i, level in enumerate(levels):
            level_data = data['levels'][level]
            if 'capabilities' in level_data and capability_type in level_data['capabilities']:
                capabilities = level_data['capabilities'][capability_type]
                x_pos = x_positions[i]
                
                # Draw connection line
                fig.add_trace(go.Scatter(
                    x=[x_pos, x_pos],
                    y=[0, y_pos],
                    mode='lines',
                    line=dict(color=color, width=3),
                    showlegend=False,
                    hoverinfo='skip'
                ))
                
                # Create hover-enabled markers for capability details
                capabilities_text = '<br>'.join([f'• {cap}' for cap in capabilities])
                hover_text = f'<b>{capability_type} - {level}</b><br><br>{capabilities_text}'
                
                # Display full capability details text box - restore original full display
                capabilities_text_display = '<br>'.join([f'• {cap}' for cap in capabilities])
                
                fig.add_annotation(
                    x=x_pos,
                    y=y_pos,
                    text=capabilities_text_display,
                    showarrow=False,
                    font=dict(size=10, color='black'),
                    bgcolor='rgba(255, 255, 255, 0.98)',
                    bordercolor=color,
                    borderwidth=2,
                    align='left',
                    width=400,
                    xanchor='center',
                    yanchor='middle'
                )
                
                # Add appropriately sized invisible marker to cover just the annotation area
                # For Ultra-Clean version with width=400, use a moderate marker
                fig.add_trace(go.Scatter(
                    x=[x_pos],
                    y=[y_pos],
                    mode='markers',
                    marker=dict(size=80, color=color, opacity=0),  # Smaller marker for more precise hover area
                    showlegend=False,
                    hovertemplate=hover_text + '<extra></extra>',
                    name=f'{capability_type}-{level}'
                ))
                
                # Visible end point
                fig.add_trace(go.Scatter(
                    x=[x_pos],
                    y=[y_pos],
                    mode='markers',
                    marker=dict(size=12, color=color),
                    showlegend=False,
                    hoverinfo='skip'
                ))
    
    # Add level description information at the top - compact layout
    description_y = 9
    for i, level in enumerate(levels):
        level_data = data['levels'][level]
        description_text = f"<b>{level_data['title']}</b><br><br>{level_data['description']}<br><br><b>Features:</b> {level_data['features']}"
        x_pos = x_positions[i]
        
        # Add hover-enabled markers for level descriptions
        hover_description = f"<b>{level_data['title']}</b><br><br><b>Description:</b><br>{level_data['description']}<br><br><b>Features:</b><br>{level_data['features']}"
        
        fig.add_trace(go.Scatter(
            x=[x_pos],
            y=[description_y],
            mode='markers',
            marker=dict(size=50, color='darkred', opacity=0),  # Smaller marker for more precise hover area
            showlegend=False,
            hovertemplate=hover_description + '<extra></extra>',
            name=f'Level-{level}'
        ))
        
        fig.add_annotation(
            x=x_pos,
            y=description_y,
            text=f"<b>{level_data['title']}</b><br><br>{level_data['description']}<br><br><b>Features:</b> {level_data['features']}",
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
    
    # Add reference lines
    # Industry position line (at L4 position)
    industry_position = x_positions[4]  # L4 position
    # GITS position line (between L1 and L2)
    organization_position = (x_positions[1] + x_positions[2]) / 2
    
    # Set layout
    fig.update_layout(
        title={
            'text': 'AI Software Delivery Capability Maturity Model Overview',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': 'darkblue'}
        },
        xaxis=dict(
            title=dict(text='Maturity Levels', font=dict(size=16)),
            tickmode='array',
            tickvals=x_positions,
            ticktext=levels,
            tickfont=dict(size=14),
            range=[-3, max(x_positions) + 2],
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=1
        ),
        yaxis=dict(
            title=dict(text='Capability Dimensions', font=dict(size=16)),
            tickfont=dict(size=14),
            showticklabels=False,
            range=[-10, 12],
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=1
        ),
        width=1900,
        height=1200,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=200, r=100, t=100, b=100),
        # Configure hover settings
        hovermode='closest',
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="gray",
            font_size=12,
            font_family="Arial"
        ),
        # Add reference lines (non-editable)
        shapes=[
            # Industry position line
            dict(
                type="line",
                x0=industry_position,
                y0=-10,
                x1=industry_position,
                y1=12,
                line=dict(
                    color="orange",
                    width=3,
                    dash="dash"
                ),
                editable=False,
                name="Industry Position"
            ),
            # Organization position line
            dict(
                type="line",
                x0=organization_position,
                y0=-10,
                x1=organization_position,
                y1=12,
                line=dict(
                    color="purple",
                    width=3,
                    dash="dash"
                ),
                editable=False,
                name="GITS Position"
            )
        ],
        # Add annotation explanations
        annotations=list(fig.layout.annotations) + [
            dict(
                x=industry_position,
                y=11,
                text="<b>Industry Position</b><br>(Reference)",
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
                y=11,
                text="<b>GITS Position</b><br>(Reference)",
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
    """Create interactive fishbone diagram with checkbox functionality"""
    fig = go.Figure()
    
    # Add Y-axis title as first annotation (bottom layer with transparency)
    fig.add_annotation(
        x=-2.5,
        y=0,
        text='<b>Capability Dimensions</b>',
        showarrow=False,
        font=dict(size=14, color='rgba(0, 0, 0, 0.5)'),  # Semi-transparent black
        xanchor='center',
        yanchor='middle',
        textangle=-90,
        bgcolor='rgba(255, 255, 255, 0.3)',  # More transparent background
        bordercolor='rgba(128, 128, 128, 0.3)',  # Semi-transparent border
        borderwidth=1
    )
    
    # Define color scheme
    colors = {
        'Personnel': '#FF6B6B',
        'Technical': '#45B7D1',
        'Process': '#4ECDC4', 
        'Knowledge Management': '#96CEB4',
        'Governance': '#FFEAA7'
    }
    
    # Y-coordinates for capability dimensions
    capability_positions = {
        'Personnel': 4,
        'Technical': 2,
        'Process': -2,
        'Knowledge Management': -4,
        'Governance': -6
    }
    
    levels = list(data['levels'].keys())
    level_names = [data['levels'][level]['title'] for level in levels]
    
    # X-axis positions - optimized spacing for better right-side space utilization
    x_positions = [2 + i * 3.5 for i in range(len(levels))]
    
    # Draw main trunk - adjust length to fit new X-axis range
    fig.add_trace(go.Scatter(
        x=[-0.5, max(x_positions) + 1.2],
        y=[0, 0],
        mode='lines',
        line=dict(color='black', width=5),
        name='AI Maturity Evolution Main Line',
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add right arrow at the end of main trunk
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
    
    # Add maturity level markers (without text)
    fig.add_trace(go.Scatter(
        x=x_positions,
        y=[0] * len(levels),
        mode='markers',
        marker=dict(size=20, color='darkred', symbol='diamond'),
        name='Maturity Levels',
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Draw branches for each capability dimension
    for capability_type, y_pos in capability_positions.items():
        color = colors[capability_type]
        
        # Add main capability dimension label
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
        
        # Draw information for each level in this dimension
        for i, level in enumerate(levels):
            level_data = data['levels'][level]
            if 'capabilities' in level_data and capability_type in level_data['capabilities']:
                capabilities = level_data['capabilities'][capability_type]
                x_pos = x_positions[i]
                
                # Draw connection line
                fig.add_trace(go.Scatter(
                    x=[x_pos, x_pos],
                    y=[0, y_pos],
                    mode='lines',
                    line=dict(color=color, width=3),
                    showlegend=False,
                    hoverinfo='skip'
                ))
                
                # Create hover-enabled markers for capability details
                capabilities_text = '<br>'.join([f'• {cap}' for cap in capabilities])
                hover_text = f'<b>{capability_type} - {level}</b><br><br>{capabilities_text}'
                
                # Simplified capability information display (detailed info in sidebar)
                # Use different font sizes within the same annotation
                main_text = f'<b style="font-size:12px">{len(capabilities)} capabilities</b>'
                hover_text_display = f'<i style="font-size:10px">Hover for details</i>'
                sidebar_text = f'<span style="font-size:8px; color:gray">See sidebar for tracking</span>'
                
                fig.add_annotation(
                    x=x_pos,
                    y=y_pos,
                    text=f'{main_text}<br>{hover_text_display}<br>{sidebar_text}',
                    showarrow=False,
                    font=dict(size=10, color='black'),
                    bgcolor='rgba(255, 255, 255, 0.98)',
                    bordercolor=color,
                    borderwidth=2,
                    align='center',
                    width=200,
                    xanchor='center',
                    yanchor='middle'
                )
                
                # Add appropriately sized invisible marker to cover just the annotation area
                # For Interactive version with width=200, use a smaller marker for precise targeting
                fig.add_trace(go.Scatter(
                    x=[x_pos],
                    y=[y_pos],
                    mode='markers',
                    marker=dict(size=60, color=color, opacity=0),  # Smaller marker for more precise hover area
                    showlegend=False,
                    hovertemplate=hover_text + '<extra></extra>',
                    name=f'{capability_type}-{level}'
                ))
                
                # Visible end point
                fig.add_trace(go.Scatter(
                    x=[x_pos],
                    y=[y_pos],
                    mode='markers',
                    marker=dict(size=12, color=color),
                    showlegend=False,
                    hoverinfo='skip'
                ))
    
    # Add level description information at the top - adjust position to avoid overlap
    description_y = 12
    for i, level in enumerate(levels):
        level_data = data['levels'][level]
        description_text = f"<b>{level_data['title']}</b><br><br>{level_data['description']}<br><br><b>Features:</b> {level_data['features']}"
        x_pos = x_positions[i]
        
        # Add hover-enabled markers for level descriptions
        hover_description = f"<b>{level_data['title']}</b><br><br><b>Description:</b><br>{level_data['description']}<br><br><b>Features:</b><br>{level_data['features']}"
        
        fig.add_trace(go.Scatter(
            x=[x_pos],
            y=[description_y],
            mode='markers',
            marker=dict(size=50, color='darkred', opacity=0),  # Smaller marker for more precise hover area
            showlegend=False,
            hovertemplate=hover_description + '<extra></extra>',
            name=f'Level-{level}'
        ))
        
        fig.add_annotation(
            x=x_pos,
            y=description_y,
            text=f"<b>{level_data['title']}</b><br><br>{level_data['description']}<br><br><b>Features:</b> {level_data['features']}",
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
            width=160,
            standoff=10
        )
    
    # Set layout
    fig.update_layout(
        title={
            'text': 'AI Maturity Model Fishbone Diagram - Interactive Version (Check completed capabilities on the left)',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': 'darkblue'}
        },
        xaxis=dict(
            title=dict(text='Maturity Levels', font=dict(size=14)),
            tickmode='array',
            tickvals=x_positions,
            ticktext=levels,
            tickfont=dict(size=12),
            range=[-2.5, max(x_positions) + 1.5],
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=1
        ),
        yaxis=dict(
            title=dict(text=''),
            tickfont=dict(size=12),
            showticklabels=False,
            range=[-8, 14],
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=1
        ),
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=50, r=50, t=60, b=40),
        autosize=True,
        # Configure hover settings
        hovermode='closest',
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="gray",
            font_size=12,
            font_family="Arial"
        )
    )
    

    
    return fig

def main(version='both'):
    """Main function
    
    Args:
        version (str): Specify the version to generate
            - 'ultra': Ultra-clean layout version
            - 'interactive': Interactive version (with checkbox)
            - 'both': Generate both versions
    """
    # Create output directory
    output_dir = '../output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    
    # Load data
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(script_dir, '../../resource/model_of_level_en.json')
    data = load_maturity_data(data_file)
    
    generated_files = []
    
    if version == 'both' or version == 'ultra':
        # Create ultra-clean layout fishbone diagram
        print("Generating ultra-clean layout version...")
        fig = create_ultra_clean_fishbone_diagram(data)
        fig.show()
        output_file = os.path.join(output_dir, 'ai_sd_maturity_ultra_en.html')
        fig.write_html(output_file, 
                        config={
                            'editable': False, 
                            'staticPlot': False,
                            'displayModeBar': True,
                            'displaylogo': False,
                            'modeBarButtonsToRemove': ['select2d', 'lasso2d', 'editInChartStudio'],
                            'toImageButtonOptions': {'format': 'png', 'filename': 'ai_sd_maturity_fishbone_en', 'height': 1200, 'width': 1900, 'scale': 1}
                        })
        generated_files.append(f"- Ultra-clean layout version: {output_file}")
    
    if version == 'both' or version == 'interactive':
        # Create interactive fishbone diagram (with checkbox)
        print("Generating interactive version (with checkbox)...")
        fig = create_interactive_fishbone_diagram(data)
        capabilities_data = generate_capabilities_data(data)
        
        # First generate complete HTML, then save as temporary file
        temp_file = os.path.join(output_dir, 'temp_plot_en.html')
        fig.write_html(temp_file, 
                      include_plotlyjs='cdn',
                      config={
                          'editable': False,
                          'staticPlot': False,
                          'displayModeBar': True,
                          'displaylogo': False,
                          'modeBarButtonsToRemove': ['select2d', 'lasso2d', 'editInChartStudio'],
                          'toImageButtonOptions': {'format': 'png', 'filename': 'ai_sd_maturity_interactive_en', 'height': 800, 'width': 1200, 'scale': 1}
                      })
        
        # Read generated HTML content
        with open(temp_file, 'r', encoding='utf-8') as f:
            plot_html = f.read()
        
        # Delete temporary file
        os.remove(temp_file)
        
        # Extract body content
        import re
        body_match = re.search(r'<body[^>]*>(.*?)</body>', plot_html, re.DOTALL)
        if body_match:
            plot_content = body_match.group(1).strip()
        else:
            plot_content = '<div id="plotly-div"></div>'
        
        # Use custom template
        template = create_interactive_html_template()
        html_content = template.replace('{plot_div}', plot_content)
        html_content = html_content.replace('{capabilities_json}', json.dumps(capabilities_data, ensure_ascii=False))
        
        output_file = os.path.join(output_dir, 'ai_sd_maturity_interactive_en.html')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        generated_files.append(f"- Interactive version (with checkbox): {output_file}")
        print(f"Interactive version generated: {output_file}")
    
    if not generated_files:
        print(f"Error: Unknown version parameter '{version}'")
        print("Available version parameters:")
        print("- 'ultra': Ultra-clean layout version")
        print("- 'interactive': Interactive version (with checkbox)")
        print("- 'both': Generate both versions")
        return
    
    print(f"\nFishbone diagram generation completed!")
    for file_info in generated_files:
        print(file_info)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate AI Maturity Model Fishbone Diagram (English Version)')
    parser.add_argument(
        '--version', '-v', 
        choices=['ultra', 'interactive', 'both'],
        default='both',
        help='Specify the version to generate (default: both)'
    )
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='Show all available versions'
    )
    
    args = parser.parse_args()
    
    if args.list:
        print("Available versions:")
        print("- ultra: Ultra-clean layout version (with draggable reference lines)")
        print("- interactive: Interactive version (with checkbox capability tracking)")
        print("- both: Generate both versions (default)")
        print("\nRecommended to use 'interactive' version, which includes sidebar checkboxes for tracking completed capabilities.")
        sys.exit(0)
    
    main(args.version) 