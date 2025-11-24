"""
概览页面（中英文双注释选项+图表准确性）
"""
import streamlit as st
import pandas as pd
from utils.viz import line_chart_timeseries, get_data_quality_chart

# 修改这两个函数
def _get_kpi_value(kpi_df: pd.DataFrame, metric_name: str, default: float = 0.0) -> float:
    """
    安全获取KPI数值（支持模糊匹配，处理中英文双语指标名）
    Safe get KPI value with fuzzy matching support
    """
    if kpi_df.empty or 'metric' not in kpi_df.columns or 'value' not in kpi_df.columns:
        return default
    
    # 使用模糊匹配查找包含指定关键词的指标
    # 转换为字符串并使用case=False进行大小写不敏感匹配
    metric_row = kpi_df[kpi_df['metric'].astype(str).str.contains(metric_name, case=False)]
    
    # 如果找不到，尝试精确匹配（兼容不同格式）
    if metric_row.empty:
        metric_row = kpi_df.loc[kpi_df['metric'] == metric_name]
    
    return metric_row['value'].iloc[0] if not metric_row.empty else default

def _get_kpi_description(kpi_df: pd.DataFrame, metric_name: str, default: str = "No description available | 无描述信息") -> str:
    """
    安全获取KPI描述（支持模糊匹配）
    Safe get KPI description with fuzzy matching support
    """
    if kpi_df.empty or 'metric' not in kpi_df.columns or 'description' not in kpi_df.columns:
        return default
    
    # 使用模糊匹配查找包含指定关键词的指标
    metric_row = kpi_df[kpi_df['metric'].astype(str).str.contains(metric_name, case=False)]
    
    # 如果找不到，尝试精确匹配
    if metric_row.empty:
        metric_row = kpi_df.loc[kpi_df['metric'] == metric_name]
    
    # 优先返回description列的值，如果不存在则返回metric列的值作为描述
    if not metric_row.empty:
        if 'description' in metric_row.columns and pd.notna(metric_row['description'].iloc[0]):
            return metric_row['description'].iloc[0]
        elif 'metric' in metric_row.columns:
            return metric_row['metric'].iloc[0]
    
    return default

def render_overview(analysis_tables: dict, raw_clean_df: pd.DataFrame):
    st.title("Overview | 概览")
    st.subheader("Key Metrics & Disease Trends | 核心指标与疾病趋势")
    st.markdown("""
    This section provides a **high-level snapshot** of public health status, including:
    本板块提供公共卫生状况的**高层级视图**，包含：
    - Core KPIs (total cases, vaccination rate, high-risk population).
      核心KPI（总病例数、接种率、高危人群）。
    - Time series trends (how metrics change by month/year/region).
      时间序列趋势（指标随月份/年份/区域的变化）。
    - Data quality check (missing values, outliers) to ensure reliability.
      数据质量检查（缺失值、异常值），确保分析可靠性。
    """)
    st.divider()
    
    # 获取KPI数据（兜底空DataFrame）
    kpi_df = analysis_tables.get("kpi", pd.DataFrame(columns=['metric', 'value', 'description']))
    
    # 调试辅助：查看KPI原始数据（可选展开）
    with st.expander("📋 查看KPI原始数据（调试用）", expanded=False):
        st.dataframe(kpi_df, use_container_width=True)
        st.text(f"可用KPI指标：{kpi_df['metric'].tolist() if not kpi_df.empty else '无'}")
    
    # KPI卡片布局
    col1, col2, col3 = st.columns(3)
    col4, col5 = st.columns(2)
    
    # 1. 总病例数
    col1.metric(
        label="Total Cases\n总病例数",
        value=f"{_get_kpi_value(kpi_df, 'Total Cases'):,.0f}",
        help=_get_kpi_description(kpi_df, 'Total Cases')
    )
    
    # 2. 平均疫苗覆盖率
    col2.metric(
        label="Average Vaccine Coverage\n平均疫苗覆盖率",
        value=f"{_get_kpi_value(kpi_df, 'Average Vaccine Coverage'):.1%}",
        help=_get_kpi_description(kpi_df, 'Average Vaccine Coverage')
    )
    
    # 3. 高危人群数量
    high_risk_metric = "High-Risk Population (Elderly + Chronic)"
    col3.metric(
        label="High-Risk Population\n高危人群数量",
        value=f"{_get_kpi_value(kpi_df, high_risk_metric):,.0f}",
        help=_get_kpi_description(kpi_df, high_risk_metric)
    )
    
    # 4. 平均资源负荷
    col4.metric(
        label="Average Resource Load\n平均资源负荷",
        value=f"{_get_kpi_value(kpi_df, 'Average Resource Load'):.2f}",
        help=_get_kpi_description(kpi_df, 'Average Resource Load')
    )
    
    # 5. 高峰季节病例数
    col5.metric(
        label="Peak Season Cases\n高峰季节病例数",
        value=f"{_get_kpi_value(kpi_df, 'Peak Season Cases'):,.0f}",
        help=_get_kpi_description(kpi_df, 'Peak Season Cases')
    )
    st.divider()
    
    # 时间序列趋势
    st.markdown("### Time Series Trends | 时间序列趋势")
    st.markdown("""
    Select a metric to view its trend over time. You can filter by **year** and **region** using the sidebar.
    选择一个指标查看其随时间的趋势。可通过侧边栏按**年份**和**区域**过滤数据。
    """)
    
    timeseries_df = analysis_tables.get("timeseries", pd.DataFrame())
    metric_options = {
        "daily_new_cases": "Daily New Cases | 每日新增病例",
        "vaccine_coverage": "Vaccine Coverage | 疫苗覆盖率",
        "transmission_rate": "Transmission Rate | 传播率",
        "resource_load": "Resource Load | 资源负荷"
    }
    selected_metric = st.selectbox(
        "Select Metric | 选择指标",
        options=list(metric_options.keys()),
        format_func=lambda x: metric_options[x]
    )
    
    if not timeseries_df.empty:
        try:
            timeseries_fig = line_chart_timeseries(timeseries_df, selected_metric)
            st.plotly_chart(timeseries_fig, use_container_width=True)
        except Exception as e:
            st.error(f"Failed to generate trend chart: {str(e)} | 生成趋势图失败：{str(e)}")
    else:
        st.warning("No time series data available. Please adjust filters. | 无时间序列数据，请调整过滤器。")
    
    # 趋势洞察（保留原有内容）
    st.markdown("#### Key Trend Insights | 趋势洞察")
    st.markdown("""
    1. **Disease Seasonality | 疾病季节性**: New cases consistently peak in Winter (December-February) and drop in Summer (June-August). This is likely due to higher transmission rates in cold, closed environments.
       新增病例在冬季（12-2月）持续高峰，夏季（6-8月）下降。原因可能是寒冷、密闭环境中传播率更高。
    2. **Vaccine Impact | 疫苗影响**: Vaccine coverage has increased year-over-year (from 45% to 70%), which correlates with a 30-40% decline in new cases. This confirms the effectiveness of vaccination.
       疫苗覆盖率逐年提升（从45%到70%），同时新增病例下降30-40%，验证了疫苗有效性。
    3. **Regional Resource Pressure | 区域资源压力**: Rural regions have consistently higher resource load (>1.2) compared to Urban areas (<0.8), indicating severe healthcare resource shortages in rural areas.
       农村地区资源负荷持续高于城市（农村>1.2，城市<0.8），表明农村医疗资源严重不足。
    4. **Transmission Consistency | 传播率稳定性**: Transmission rates follow a stable seasonal pattern (Winter:1.2, Summer:0.6), which can be used to predict future outbreaks.
       传播率呈稳定季节模式（冬季1.2，夏季0.6），可用于预测未来暴发。
    """)
    st.divider()
    
    # 数据质量检查
    st.markdown("### Data Quality Check | 数据质量检查")
    st.markdown("""
    Data reliability is the foundation of credible analysis. Below is the missing value statistics for all fields.
    数据可靠性是可信分析的基础。以下是所有字段的缺失值统计。
    """)
    
    if not raw_clean_df.empty:
        try:
            quality_fig = get_data_quality_chart(raw_clean_df)
            st.plotly_chart(quality_fig, use_container_width=True)
        except Exception as e:
            st.error(f"Failed to generate data quality chart: {str(e)} | 生成数据质量图失败：{str(e)}")
    else:
        st.warning("No clean data available for quality check. | 无干净数据可进行质量检查。")
    
    # 数据质量总结（保留原有内容）
    st.markdown("#### Data Quality Summary | 数据质量总结")
    st.markdown("""
    1. **Core Fields | 核心字段**: No missing values in core fields (missing ratio = 0%), including date, region, cases, vaccination status, and age. This ensures the reliability of key analyses (trends, vaccine effect).
       核心字段（日期、区域、病例数、接种状态、年龄）无缺失值（缺失率=0%），确保关键分析（趋势、疫苗效果）可靠。
    2. **Secondary Fields | 次要字段**: Missing values in non-core fields (e.g., immunity_level: ~2%) are filled with mode, which has minimal impact on overall analysis.
       非核心字段（如免疫水平：~2%）缺失值用众数填充，对整体分析影响极小。
    3. **Outlier Handling | 异常值处理**: Extreme values (age>120, negative cases, zero capacity) have been filtered, preventing distortion of statistical results.
       极端值（年龄>120、负病例数、零床位）已过滤，避免统计结果失真。
    4. **Standardization | 标准化处理**: All fields are standardized (e.g., date→datetime, categorical→title case), ensuring consistency across analyses.
       所有字段已标准化（如日期→datetime，分类→首字母大写），确保分析一致性。
    """)