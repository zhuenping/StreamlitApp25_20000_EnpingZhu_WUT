"""
Complete Visualization Utilities | 完整可视化工具库
- Time Series Line Chart | 时间序列线图
- Region-SES Bar Chart | 区域-SES柱状图
- Vaccine Effect Scatter Chart | 疫苗效果散点图（解决“66+岁不显示”问题）
- Data Quality Chart | 数据质量图
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 全局样式配置（统一所有图表风格，确保美观一致）
GLOBAL_CONFIG = {
    "color_scheme": {
        # 区域颜色
        "Urban": "#1f77b4",       # 蓝色（城市）
        "Suburban": "#2ca02c",    # 绿色（郊区）
        "Rural": "#ff7f0e",       # 橙色（农村）
        # SES颜色
        "High": "#d62728",        # 红色（高SES）
        "Medium": "#9467bd",      # 紫色（中SES）
        "Low": "#8c564b",         # 棕色（低SES）
        # 免疫水平颜色（疫苗效果图）
        "Low_Immunity": "#d62728",# 红色（低免疫）
        "Medium_Immunity": "#9467bd",# 紫色（中免疫）
        "High_Immunity": "#1f77b4",# 蓝色（高免疫）
        # 接种状态符号（疫苗效果图）
        "vaccine_symbol": {
            "Vaccinated": "circle",    # 已接种→圆形
            "Unvaccinated": "x"        # 未接种→X形
        }
    },
    "font_config": {
        "family": "Arial",        # 字体家族
        "base_size": 12,          # 基础字体大小
        "title_size": 16,         # 标题字体大小
        "axis_title_size": 14     # 坐标轴标题字体大小
    },
    "chart_size": {
        "time_series_height": 600, # 时间序列图高度
        "bar_chart_height": 500,   # 柱状图高度
        "scatter_chart_height": 600,# 散点图高度
        "quality_chart_height": 500 # 数据质量图高度
    },
    "legend_config": {
        "time_series_legend": {"orientation": "h", "y": 1.02, "x": 1},  # 水平图例（底部）
        "scatter_legend": {"orientation": "v", "y": 1, "x": 1}          # 垂直图例（右侧）
    }
}

# 找到line_chart_timeseries函数并添加以下修复 | Find line_chart_timeseries function and add these fixes
# 替换现有的line_chart_timeseries函数
from utils.viz import go

# 导入make_subplots
# 修改line_chart_timeseries函数，增加更多功能和优化
# 修复line_chart_timeseries函数，解决字符串未终止和缩进问题
from plotly.subplots import make_subplots
import numpy as np

def line_chart_timeseries(timeseries_df: pd.DataFrame, target_metric: str) -> go.Figure:
    """时间序列线图：显示不同区域、不同年份的指标趋势
    
    参数:
    - timeseries_df: 时间序列数据框
    - target_metric: 目标指标
    """
    # 1. 指标标签映射（中英文双注释）
    metric_label_map = {
        "daily_new_cases": "Daily New Cases | 每日新增病例",
        "vaccine_coverage": "Vaccine Coverage | 疫苗覆盖率",
        "transmission_rate": "Transmission Rate | 传播率",
        "resource_load": "Resource Load | 资源负荷"
    }
    y_axis_label = metric_label_map.get(target_metric, target_metric.replace("_", " ").title())
    
    # 确保年份列存在
    if 'year' in timeseries_df.columns and not timeseries_df['year'].isna().all():
        year_range = f"{timeseries_df['year'].min()}-{timeseries_df['year'].max()}"
    else:
        year_range = "Time Period | 时间段"
    
    # 简化标题，移除聚合方式相关内容
    chart_title = f"Trend of {y_axis_label} by Region & Year ({year_range}) | 区域&年份{y_axis_label}趋势"
    
    # 2. 数据预处理：确保月份格式正确
    if 'month' in timeseries_df.columns:
        timeseries_df = timeseries_df.copy()
        # 转换month列为整数
        timeseries_df['month'] = timeseries_df['month'].astype(int)
    
    # 3. 数据聚合 - 始终使用均值聚合
    timeseries_df = timeseries_df.groupby(['year', 'month', 'location']).agg({target_metric: 'mean'}).reset_index()
    
    # 4. 获取唯一年份并创建子图
    years = sorted(timeseries_df['year'].unique())
    # 创建垂直排列的子图，增加垂直间距
    fig = make_subplots(
        rows=len(years), 
        cols=1,
        shared_xaxes=False,
        vertical_spacing=0.2,  # 保持适当的垂直间距
        subplot_titles=[f"Year {year} | 年份{year}" for year in years]
    )

    # 区域颜色映射
    colors = {
        'Urban': GLOBAL_CONFIG["color_scheme"]["Urban"],
        'Suburban': GLOBAL_CONFIG["color_scheme"]["Suburban"],
        'Rural': GLOBAL_CONFIG["color_scheme"]["Rural"]
    }

    # 5. 为每个年份和区域添加数据轨迹
    locations = ['Urban', 'Suburban', 'Rural']

    for year_idx, year in enumerate(years):
        for location in locations:
            # 筛选该年份和区域的数据
            filtered_data = timeseries_df[(timeseries_df['year'] == year) & (timeseries_df['location'] == location)]
            
            # 只在有数据时添加轨迹
            if not filtered_data.empty and target_metric in filtered_data.columns:
                # 确保数据按月份排序
                filtered_data = filtered_data.sort_values('month')
                
                # 添加线条轨迹
                fig.add_trace(
                    go.Scatter(
                        x=filtered_data['month'],
                        y=filtered_data[target_metric],
                        name=location,
                        line=dict(color=colors[location], width=2),
                        mode='lines+markers',  # 同时显示线条和标记点
                        hovertemplate=f"Month: %{{x}}<br>{y_axis_label}: %{{y:.2f}}<extra></extra>",
                        legendgroup=location,  # 为了图例正确显示
                        showlegend=(year_idx == 0)  # 只在第一个年份显示图例
                    ),
                    row=year_idx + 1,
                    col=1
                )
    
    # 6. 图表布局配置
    fig.update_layout(
        font=dict(
            family=GLOBAL_CONFIG["font_config"]["family"],
            size=GLOBAL_CONFIG["font_config"]["base_size"]
        ),
        title_font=dict(
            size=GLOBAL_CONFIG["font_config"]["title_size"],
            weight="bold"
        ),
        title=chart_title,
        legend=GLOBAL_CONFIG["legend_config"]["time_series_legend"],
        height=GLOBAL_CONFIG["chart_size"]["time_series_height"] * len(years),  # 动态调整高度
        margin=dict(l=50, r=50, t=50, b=50),  # 增加边距
        hovermode='x unified'  # 改善悬停体验
    )
    
    # 7. 坐标轴配置
    for i in range(1, len(years) + 1):
        fig.update_xaxes(
            title_text="Month | 月份",
            tickvals=list(range(1, 13)),
            ticktext=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            row=i,
            col=1
        )
        fig.update_yaxes(
            title_text=y_axis_label,
            row=i,
            col=1
        )
    
    # 移除比较模式相关代码
    
    return fig

def bar_chart_region_ses(region_ses_df: pd.DataFrame, target_metric: str) -> go.Figure:
    """区域-SES-季节柱状图：对比不同维度的指标差异"""
    # 1. 指标标签映射
    metric_label_map = {
        "daily_new_cases": "Daily New Cases | 每日新增病例",
        "vaccine_coverage": "Vaccine Coverage | 疫苗覆盖率",
        "resource_load": "Resource Load | 资源负荷",
        "age": "Median Age | 年龄中位数"
    }
    y_axis_label = metric_label_map.get(target_metric, target_metric.replace("_", " ").title())
    chart_title = f"{y_axis_label} by Region, SES & Season | 区域-SES-季节{y_axis_label}对比"
    
    # 2. 创建柱状图（按季节分面）
    fig = px.bar(
        region_ses_df,
        x="location",
        y=target_metric,
        color="ses",
        facet_col="season",  # 按季节水平分面
        color_discrete_map={
            "High": GLOBAL_CONFIG["color_scheme"]["High"],
            "Medium": GLOBAL_CONFIG["color_scheme"]["Medium"],
            "Low": GLOBAL_CONFIG["color_scheme"]["Low"]
        },
        # 强制分类顺序
        category_orders={
            "location": ["Urban", "Suburban", "Rural"],
            "ses": ["High", "Medium", "Low"],
            "season": ["Spring", "Summer", "Autumn", "Winter"]  # 季节顺序
        },
        labels={
            "location": "Region | 区域",
            "ses": "Socio-Economic Status | 社会经济水平",
            "season": "Season | 季节",
            target_metric: y_axis_label
        },
        title=chart_title
    )
    
    # 3. 图表样式配置
    fig.update_layout(
        font=dict(
            family=GLOBAL_CONFIG["font_config"]["family"],
            size=GLOBAL_CONFIG["font_config"]["base_size"]
        ),
        title_font=dict(
            size=GLOBAL_CONFIG["font_config"]["title_size"],
            weight="bold"
        ),
        legend=GLOBAL_CONFIG["legend_config"]["time_series_legend"],
        height=GLOBAL_CONFIG["chart_size"]["bar_chart_height"],
        hovermode="x unified",
        plot_bgcolor="white",
        paper_bgcolor="white"
    )
    
    # 4. 坐标轴配置
    fig.update_yaxes(
        title_font=dict(size=GLOBAL_CONFIG["font_config"]["axis_title_size"]),
        title=y_axis_label,
        gridcolor="#e0e0e0"
    )
    
    fig.update_xaxes(
        title_font=dict(size=GLOBAL_CONFIG["font_config"]["axis_title_size"]),
        title="Region | 区域",
        gridcolor="#e0e0e0"
    )
    
    return fig

def scatter_chart_vaccine_effect(vaccine_effect_df: pd.DataFrame) -> go.Figure:
    """疫苗效果散点图：显示不同年龄组、免疫水平、接种状态的病例数（解决"66+岁不显示"问题）"""
    # 1. 图表基础配置 | Chart basic configuration
    chart_title = "Vaccine Effect: Average Daily New Cases by Age Group, Immunity & Vaccination Status | 疫苗效果：年龄组-免疫水平-接种状态对平均每日新增病例的影响"
    
    # 2. 数据预处理 | Data preprocessing
    # 确保数据有效 | Ensure data validity
    if vaccine_effect_df.empty:
        fig = go.Figure()
        fig.update_layout(
            title=chart_title,
            annotations=[dict(
                text="No valid data available | 无有效数据",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=18, color="red")
            )]
        )
        return fig
    
    # 显式定义年龄组（确保66+岁显示，顺序固定） | Explicitly define age groups (ensure 66+ is shown, fixed order)
    age_groups = ["Child (0-18)", "Adult (19-65)", "Elderly (66+)"]
    immunity_levels = ["Low", "Medium", "High"]
    vaccination_status = ["Unvaccinated", "Vaccinated"]
    
    # 3. 强制分类类型（避免Plotly自动过滤空分组，确保66+岁显示） | Force categorical types (avoid Plotly auto-filtering empty groups)
    vaccine_effect_df = vaccine_effect_df.copy()  # 创建副本避免修改原数据
    
    # 确保所有必要列存在 | Ensure all necessary columns exist
    for col in ["age_group", "immunity_level", "vaccination_status", "daily_new_cases", "transmission_rate"]:
        if col not in vaccine_effect_df.columns:
            vaccine_effect_df[col] = 0 if col in ["daily_new_cases", "transmission_rate"] else "Unknown"
    
    # 设置分类类型 | Set categorical types
    # 完全重写分类处理部分，确保正确的缩进结构
    for col in ["age_group", "immunity_level", "vaccination_status"]:
        # 先确定要使用的分类类别
        if col == "age_group":
            categories = ["Child (0-18)", "Adult (19-65)", "Elderly (66+)", "Unknown"]
        elif col == "immunity_level":
            categories = ["Low", "Medium", "High", "Unknown"]
        elif col == "vaccination_status":
            categories = ["Unvaccinated", "Vaccinated", "Unknown"]
        
        # 首先确保数据不是分类类型，避免类型转换问题
        if pd.api.types.is_categorical_dtype(vaccine_effect_df[col]):
            # 转换为字符串类型进行处理
            vaccine_effect_df[col] = vaccine_effect_df[col].astype(str)
        
        # 填充缺失值
        vaccine_effect_df[col] = vaccine_effect_df[col].fillna("Unknown")
        
        # 然后转换为包含Unknown的分类类型
        vaccine_effect_df[col] = pd.Categorical(
            vaccine_effect_df[col],
            categories=categories,
            ordered=True
        )
    
    # 4. 创建散点图 | Create scatter plot
    fig = px.scatter(
        vaccine_effect_df,
        x="age_group",  # X轴：年龄组（含66+岁）
        y="daily_new_cases",  # Y轴：平均每日新增病例
        color="immunity_level",  # 颜色：免疫水平
        symbol="vaccination_status",  # 符号：接种状态
        # 颜色映射 | Color mapping
        color_discrete_map={
            "Low": GLOBAL_CONFIG["color_scheme"]["Low_Immunity"],
            "Medium": GLOBAL_CONFIG["color_scheme"]["Medium_Immunity"],
            "High": GLOBAL_CONFIG["color_scheme"]["High_Immunity"]
        },
        # 符号映射 | Symbol mapping
        symbol_map=GLOBAL_CONFIG["color_scheme"]["vaccine_symbol"],
        # 强制分类顺序 | Force category order
        category_orders={
            "age_group": age_groups,
            "immunity_level": immunity_levels,
            "vaccination_status": vaccination_status
        },
        # 点大小：由传播率决定（传播率越高，点越大） | Point size determined by transmission rate
        size="transmission_rate",
        size_max=100,  # 最大点大小
        # 标签配置（中英文双注释） | Label configuration (Chinese-English bilingual)
        labels={
            "age_group": "Age Group | 年龄组",
            "daily_new_cases": "Average Daily New Cases | 平均每日新增病例",
            "immunity_level": "Immunity Level | 免疫水平",
            "vaccination_status": "Vaccination Status | 接种状态",
            "transmission_rate": "Transmission Rate | 传播率"
        },
        title=chart_title
    )
    
    # 5. 图表样式配置 | Chart style configuration
    fig.update_layout(
        font=dict(
            family=GLOBAL_CONFIG["font_config"]["family"],
            size=GLOBAL_CONFIG["font_config"]["base_size"]
        ),
        title_font=dict(
            size=GLOBAL_CONFIG["font_config"]["title_size"],
            weight="bold"
        ),
        # 图例配置（垂直，右侧） | Legend configuration
        legend=GLOBAL_CONFIG["legend_config"]["scatter_legend"],
        # 图表大小 | Chart size
        height=GLOBAL_CONFIG["chart_size"]["scatter_chart_height"],
        # Hover模式（显示最近点详细数据） | Hover mode
        hovermode="closest",
        # 背景样式 | Background style
        plot_bgcolor="white",
        paper_bgcolor="white"
    )
    
    # 6. 坐标轴配置（Y轴从0开始，避免负数） | Axis configuration
    fig.update_yaxes(
        title_font=dict(size=GLOBAL_CONFIG["font_config"]["axis_title_size"]),
        title="Average Daily New Cases | 平均每日新增病例",
        range=[0, max(vaccine_effect_df["daily_new_cases"].max() * 1.1, 1)],  # 留10%余量，确保最小范围为1
        gridcolor="#e0e0e0"
    )
    
    fig.update_xaxes(
        title_font=dict(size=GLOBAL_CONFIG["font_config"]["axis_title_size"]),
        title="Age Group | 年龄组",
        gridcolor="#e0e0e0"
    )
    
    # 7. 添加参考线和注释（增强可读性） | Add reference lines and annotations
    # 为每个年龄组添加已接种和未接种的平均水平线 | Add average horizontal lines for vaccinated and unvaccinated groups
    for age_group in age_groups:
        age_data = vaccine_effect_df[vaccine_effect_df["age_group"] == age_group]
        if not age_data.empty:
            # 已接种平均线 | Vaccinated average line
            vac_data = age_data[age_data["vaccination_status"] == "Vaccinated"]
            if not vac_data.empty:
                vac_avg = vac_data["daily_new_cases"].mean()
                fig.add_hline(y=vac_avg, line_dash="dash", line_color="#1f77b4",
                             annotation_text=f"Vaccinated Avg: {vac_avg:.1f}",
                             annotation_position="right")
            
            # 未接种平均线 | Unvaccinated average line
            unvac_data = age_data[age_data["vaccination_status"] == "Unvaccinated"]
            if not unvac_data.empty:
                unvac_avg = unvac_data["daily_new_cases"].mean()
                fig.add_hline(y=unvac_avg, line_dash="dash", line_color="#ff7f0e",
                             annotation_text=f"Unvaccinated Avg: {unvac_avg:.1f}",
                             annotation_position="left")
    
    return fig

def get_data_quality_chart(raw_feature_df: pd.DataFrame) -> go.Figure:
    """数据质量图：显示各字段缺失值比例"""
    # 1. 计算缺失值比例
    missing_value_stats = pd.DataFrame({
        "field_name": raw_feature_df.columns,
        "missing_ratio": [
            raw_feature_df[col].isnull().sum() / len(raw_feature_df) 
            for col in raw_feature_df.columns
        ]
    })
    # 按缺失比例降序排序
    missing_value_stats = missing_value_stats.sort_values("missing_ratio", ascending=False)
    
    # 2. 创建柱状图
    chart_title = "Data Quality: Missing Value Ratio by Field | 数据质量：各字段缺失值比例"
    fig = px.bar(
        missing_value_stats,
        x="field_name",
        y="missing_ratio",
        color="missing_ratio",
        color_continuous_scale="Reds",  # 红色系：缺失越多颜色越深
        labels={
            "field_name": "Dataset Field | 数据集字段",
            "missing_ratio": "Missing Value Ratio | 缺失值比例"
        },
        title=chart_title
    )
    
    # 3. 图表样式配置
    fig.update_layout(
        font=dict(
            family=GLOBAL_CONFIG["font_config"]["family"],
            size=GLOBAL_CONFIG["font_config"]["base_size"]
        ),
        title_font=dict(
            size=GLOBAL_CONFIG["font_config"]["title_size"],
            weight="bold"
        ),
        height=GLOBAL_CONFIG["chart_size"]["quality_chart_height"],
        hovermode="x unified",
        plot_bgcolor="white",
        paper_bgcolor="white"
    )
    
    # 4. 坐标轴配置（X轴标签旋转，避免重叠）
    fig.update_xaxes(
        tickangle=-45,  # 旋转45度
        title_font=dict(size=GLOBAL_CONFIG["font_config"]["axis_title_size"]),
        title="Dataset Field | 数据集字段",
        gridcolor="#e0e0e0"
    )
    
    fig.update_yaxes(
        title_font=dict(size=GLOBAL_CONFIG["font_config"]["axis_title_size"]),
        title="Missing Value Ratio | 缺失值比例",
        tickformat=".1%",  # 显示为百分比
        gridcolor="#e0e0e0"
    )
    
    # 5. 显示缺失比例标签（柱子上方）
    fig.update_traces(
        texttemplate="%{y:.1%}",  # 百分比格式
        textposition="outside",
        textfont=dict(size=GLOBAL_CONFIG["font_config"]["base_size"])
    )
    
    return fig

# 在utils/viz.py中添加新的函数
def bar_chart_vaccine_effect(vaccine_effect_df: pd.DataFrame) -> go.Figure:
    """疫苗效果分组柱状图：更清晰地展示不同年龄组和接种状态的病例数对比"""
    chart_title = "Vaccine Effect: Cases by Age Group and Vaccination Status | 疫苗效果：按年龄组和接种状态分组的病例数"
    
    # 数据预处理
    if vaccine_effect_df.empty:
        fig = go.Figure()
        fig.update_layout(
            title=chart_title,
            annotations=[dict(
                text="No valid data available | 无有效数据",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=18, color="red")
            )]
        )
        return fig
    
    # 确保数据格式正确
    vaccine_effect_df = vaccine_effect_df.copy()
    age_groups = ["Child (0-18)", "Adult (19-65)", "Elderly (66+)"]
    
    # 直接使用颜色值，避免依赖GLOBAL_CONFIG中可能不存在的键
    color_discrete_map = {
        "Unvaccinated": "#FF4136",  # 红色（未接种）
        "Vaccinated": "#2ECC40"      # 绿色（已接种）
    }
    
    # 创建分组柱状图
    fig = px.bar(
        vaccine_effect_df,
        x="age_group",
        y="daily_new_cases",
        color="vaccination_status",
        barmode="group",
        facet_col="immunity_level",  # 按免疫水平分面
        category_orders={
            "age_group": age_groups,
            "immunity_level": ["Low", "Medium", "High"],
            "vaccination_status": ["Unvaccinated", "Vaccinated"]  # 确保接种状态顺序一致
        },
        labels={
            "age_group": "Age Group | 年龄组",
            "daily_new_cases": "Average Daily New Cases | 平均每日新增病例",
            "vaccination_status": "Vaccination Status | 接种状态",
            "immunity_level": "Immunity Level | 免疫水平"
        },
        title=chart_title,
        color_discrete_map=color_discrete_map
    )
    
    # 图表样式配置
    fig.update_layout(
        height=600,  # 增加高度以更好显示
        margin=dict(l=40, r=40, t=60, b=60),
        font=dict(
            family=GLOBAL_CONFIG["font_config"]["family"],
            size=GLOBAL_CONFIG["font_config"]["base_size"]
        ),
        title_font=dict(
            size=GLOBAL_CONFIG["font_config"]["title_size"],
            weight="bold"
        ),
        legend_title_text="Vaccination Status | 接种状态",
        yaxis_title="Average Daily New Cases | 平均每日新增病例",
        xaxis_title="Age Group | 年龄组",
        hovermode="x unified"
    )
    
    # 统一坐标轴设置
    fig.update_yaxes(
        title_font=dict(size=GLOBAL_CONFIG["font_config"]["axis_title_size"]),
        gridcolor="#e0e0e0"
    )
    
    fig.update_xaxes(
        title_font=dict(size=GLOBAL_CONFIG["font_config"]["axis_title_size"]),
        gridcolor="#e0e0e0"
    )
    
    return fig

