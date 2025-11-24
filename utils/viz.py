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

def line_chart_timeseries(timeseries_df: pd.DataFrame, target_metric: str) -> go.Figure:
    """时间序列线图：显示不同区域、不同年份的指标趋势"""
    # 1. 指标标签映射（中英文双注释）
    metric_label_map = {
        "daily_new_cases": "Daily New Cases | 每日新增病例",
        "vaccine_coverage": "Vaccine Coverage | 疫苗覆盖率",
        "transmission_rate": "Transmission Rate | 传播率",
        "resource_load": "Resource Load | 资源负荷"
    }
    y_axis_label = metric_label_map.get(target_metric, target_metric.replace("_", " ").title())
    year_range = f"{timeseries_df['year'].min()}-{timeseries_df['year'].max()}"
    chart_title = f"Trend of {y_axis_label} by Region & Year ({year_range}) | 区域&年份{y_axis_label}趋势"
    
    # 2. 创建线图（按年份分面，确保12个月完整显示）
    fig = px.line(
        timeseries_df,
        x="month",
        y=target_metric,
        color="location",
        facet_row="year",  # 按年份垂直分面，便于对比
        color_discrete_map={
            "Urban": GLOBAL_CONFIG["color_scheme"]["Urban"],
            "Suburban": GLOBAL_CONFIG["color_scheme"]["Suburban"],
            "Rural": GLOBAL_CONFIG["color_scheme"]["Rural"]
        },
        # 强制分类顺序（确保月份1-12完整，区域顺序固定）
        category_orders={
            "location": ["Urban", "Suburban", "Rural"],
            "month": list(range(1, 13))  # 显式包含12月
        },
        labels={
            "month": "Month | 月份",
            "location": "Region | 区域",
            target_metric: y_axis_label
        },
        title=chart_title
    )
    
    # 3. 图表样式配置
    fig.update_layout(
        # 字体配置
        font=dict(
            family=GLOBAL_CONFIG["font_config"]["family"],
            size=GLOBAL_CONFIG["font_config"]["base_size"]
        ),
        title_font=dict(
            size=GLOBAL_CONFIG["font_config"]["title_size"],
            weight="bold"
        ),
        # 图例配置（水平，底部）
        legend=GLOBAL_CONFIG["legend_config"]["time_series_legend"],
        # 图表大小
        height=GLOBAL_CONFIG["chart_size"]["time_series_height"],
        # Hover模式（显示同一月份所有区域数据）
        hovermode="x unified",
        # 背景样式
        plot_bgcolor="white",
        paper_bgcolor="white"
    )
    
    # 4. 坐标轴配置（确保显示Month 12）
    fig.update_xaxes(
        tickmode="array",
        tickvals=list(range(1, 13)),  # 1-12月
        ticktext=[f"Month {i} | 月份{i}" for i in range(1, 13)],  # 显示“Month 12 | 月份12”
        title_font=dict(size=GLOBAL_CONFIG["font_config"]["axis_title_size"]),
        title="Month | 月份",
        gridcolor="#e0e0e0"  # 浅色网格线
    )
    
    fig.update_yaxes(
        title_font=dict(size=GLOBAL_CONFIG["font_config"]["axis_title_size"]),
        title=y_axis_label,
        gridcolor="#e0e0e0"
    )
    
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
    """疫苗效果散点图：显示不同年龄组、免疫水平、接种状态的病例数（解决“66+岁不显示”问题）"""
    # 1. 图表基础配置
    chart_title = "Vaccine Effect: Average Daily New Cases by Age Group, Immunity & Vaccination Status | 疫苗效果：年龄组-免疫水平-接种状态对平均每日新增病例的影响"
    # 显式定义年龄组（确保66+岁显示，顺序固定）
    age_groups = ["Child (0-18)", "Adult (19-65)", "Elderly (66+)"]
    immunity_levels = ["Low", "Medium", "High"]
    vaccination_status = ["Unvaccinated", "Vaccinated"]
    
    # 2. 强制分类类型（避免Plotly自动过滤空分组，确保66+岁显示）
    vaccine_effect_df["age_group"] = pd.Categorical(
        vaccine_effect_df["age_group"],
        categories=age_groups,
        ordered=True
    )
    vaccine_effect_df["immunity_level"] = pd.Categorical(
        vaccine_effect_df["immunity_level"],
        categories=immunity_levels,
        ordered=True
    )
    vaccine_effect_df["vaccination_status"] = pd.Categorical(
        vaccine_effect_df["vaccination_status"],
        categories=vaccination_status,
        ordered=True
    )
    
    # 3. 创建散点图
    fig = px.scatter(
        vaccine_effect_df,
        x="age_group",  # X轴：年龄组（含66+岁）
        y="daily_new_cases",  # Y轴：平均每日新增病例
        color="immunity_level",  # 颜色：免疫水平
        symbol="vaccination_status",  # 符号：接种状态
        # 颜色映射
        color_discrete_map={
            "Low": GLOBAL_CONFIG["color_scheme"]["Low_Immunity"],
            "Medium": GLOBAL_CONFIG["color_scheme"]["Medium_Immunity"],
            "High": GLOBAL_CONFIG["color_scheme"]["High_Immunity"]
        },
        # 符号映射
        symbol_map=GLOBAL_CONFIG["color_scheme"]["vaccine_symbol"],
        # 强制分类顺序
        category_orders={
            "age_group": age_groups,
            "immunity_level": immunity_levels,
            "vaccination_status": vaccination_status
        },
        # 点大小：由传播率决定（传播率越高，点越大）
        size="transmission_rate",
        size_max=100,  # 最大点大小
        # 标签配置（中英文双注释）
        labels={
            "age_group": "Age Group | 年龄组",
            "daily_new_cases": "Average Daily New Cases | 平均每日新增病例",
            "immunity_level": "Immunity Level | 免疫水平",
            "vaccination_status": "Vaccination Status | 接种状态",
            "transmission_rate": "Transmission Rate | 传播率"
        },
        title=chart_title
    )
    
    # 4. 图表样式配置
    fig.update_layout(
        font=dict(
            family=GLOBAL_CONFIG["font_config"]["family"],
            size=GLOBAL_CONFIG["font_config"]["base_size"]
        ),
        title_font=dict(
            size=GLOBAL_CONFIG["font_config"]["title_size"],
            weight="bold"
        ),
        # 图例配置（垂直，右侧）
        legend=GLOBAL_CONFIG["legend_config"]["scatter_legend"],
        # 图表大小
        height=GLOBAL_CONFIG["chart_size"]["scatter_chart_height"],
        # Hover模式（显示最近点详细数据）
        hovermode="closest",
        # 背景样式
        plot_bgcolor="white",
        paper_bgcolor="white"
    )
    
    # 5. 坐标轴配置（Y轴从0开始，避免负数）
    fig.update_yaxes(
        title_font=dict(size=GLOBAL_CONFIG["font_config"]["axis_title_size"]),
        title="Average Daily New Cases | 平均每日新增病例",
        range=[0, vaccine_effect_df["daily_new_cases"].max() * 1.1],  # 留10%余量
        gridcolor="#e0e0e0"
    )
    
    fig.update_xaxes(
        title_font=dict(size=GLOBAL_CONFIG["font_config"]["axis_title_size"]),
        title="Age Group | 年龄组",
        gridcolor="#e0e0e0"
    )
    
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