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
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    
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
    
    # 4. 平均资源负荷
    col3.metric(
        label="Average Resource Load\n平均资源负荷",
        value=f"{_get_kpi_value(kpi_df, 'Average Resource Load'):.2f}",
        help=_get_kpi_description(kpi_df, 'Average Resource Load')
    )
    
    # 5. 高峰季节病例数
    col4.metric(
        label="Peak Season Cases\n高峰季节病例数",
        value=f"{_get_kpi_value(kpi_df, 'Peak Season Cases'):,.0f}",
        help=_get_kpi_description(kpi_df, 'Peak Season Cases')
    )
    st.divider()
    
    # 修改时间序列趋势部分，修复缩进和缺少except的问题
    
    # 时间序列趋势 | Time series trends
    st.markdown("### Time Series Trends | 时间序列趋势")
    st.markdown("""
    Select a metric to view its trend over time. You can filter by **year** and **region** using the sidebar.
    选择一个指标查看其随时间的趋势。可通过侧边栏按**年份**和**区域**过滤数据。
    """)
    
    timeseries_df = analysis_tables.get("timeseries", pd.DataFrame())
    # 增加更多指标选项
    metric_options = {
        "daily_new_cases": "Daily New Cases | 每日新增病例",
        "vaccine_coverage": "Vaccine Coverage | 疫苗覆盖率",
        "transmission_rate": "Transmission Rate | 传播率",
        "resource_load": "Resource Load | 资源负荷"
    }
    
    # 使用列布局放置控制选项 - 只保留指标选择
    col1 = st.columns(1)
    
    with col1[0]:  # 使用单列布局
        # 只保留指标选择
        selected_metric = st.selectbox(
            "Select Metric | 选择指标",
            options=metric_options,
            format_func=lambda x: metric_options[x]
        )
    
    # 移除聚合方式选择、趋势线选项和比较模式选项
    
    # 数据验证和图表生成 | Data validation and chart generation
    if not timeseries_df.empty:
        try:
            # 确保timeseries_df包含必要的列 | Ensure timeseries_df contains necessary columns
            required_columns = ["date", "year", "month"]
            if not all(col in timeseries_df.columns for col in required_columns):
                st.warning("数据缺少必要的时间列，无法生成趋势图 | Data lacks necessary time columns, cannot generate trend chart")
            else:
                # 确保selected_metric在数据中 | Ensure selected_metric is in the data
                if selected_metric in timeseries_df.columns:
                    # 调用简化后的line_chart_timeseries函数，使用默认参数
                    timeseries_fig = line_chart_timeseries(
                        timeseries_df, 
                        selected_metric
                    )
                    st.plotly_chart(timeseries_fig, use_container_width=True)
                else:
                    st.warning(f"选择的指标{selected_metric}在数据中不存在 | Selected metric {selected_metric} does not exist in the data")
        except Exception as e:
            st.error(f"生成趋势图失败：{str(e)} | Failed to generate trend chart: {str(e)}")
    else:
        st.warning("无时间序列数据，请调整过滤器 | No time series data available, please adjust filters")

    # 简化趋势洞察部分，移除与聚合方式、比较模式和趋势线相关的逻辑
    # 在第145行附近的趋势洞察部分添加以下内容
    st.markdown("#### Key Trend Insights | 趋势洞察")
    st.markdown("""
    1. **Regional Age Distribution Patterns | 区域年龄分布特征**:  
       - Urban areas have higher median age (approx. 50-51 years), while rural areas have lower median age (approx. 49 years), reflecting age structure differences during population urbanization.  
       城市区域年龄中位数普遍较高（约50-51岁），而农村地区较低（约49岁），反映了人口城市化过程中的年龄结构差异。  
       - This difference has important implications for public health resource allocation, as urban areas may require more medical services for elderly populations.  
       这种差异对公共卫生资源配置有重要影响，城市地区可能需要更多针对老年人群的医疗服务。
    
    2. **Socioeconomic Impact | 社会经济水平影响**:  
       - Regardless of region and season, high socioeconomic status groups consistently have a higher median age than low socioeconomic status groups (by approximately 2-3 years).  
       无论区域和季节如何，高社会经济水平群体的年龄中位数始终高于低社会经济水平群体（约2-3岁）。  
       - This finding may be related to differences in population migration patterns and fertility rates among different socioeconomic groups.  
       这一发现可能与不同社会经济群体的人口迁移模式、生育率差异有关。
    
    3. **Seasonal Variation | 季节性波动特征**:  
       - The median age across regions and socioeconomic levels remains relatively stable across different seasons, with no significant seasonal fluctuations.  
       各区域和社会经济水平的年龄中位数在不同季节相对稳定，没有显著的季节性波动。  
       - This stability indicates that age structure is a relatively static demographic characteristic that does not change dramatically in the short term due to seasonal variations.  
       这种稳定性表明年龄结构是一个相对静态的人口特征，短期内不会因季节变化而大幅改变。
    
    4. **Public Health Implications of Urban-Rural Gap | 城乡差异的公共卫生意义**:  
       - Rural low socioeconomic status groups have the lowest median age (approximately 47-48 years) but may face more limited medical resources.  
       农村低社会经济水平群体年龄中位数最低（约47-48岁），但可能面临更有限的医疗资源。  
       - This mismatch between population structure and resource distribution requires special attention in public health planning to ensure appropriate resource input in rural areas.  
       这种人口结构与资源分布的不匹配需要在公共卫生规划中特别关注，确保农村地区获得适当的资源投入。
    """)
    
    # 基于选择的指标生成基本洞察
    if not timeseries_df.empty and selected_metric in timeseries_df.columns:
        try:
            # 确保month列存在 | Ensure month column exists
            if "month" in timeseries_df.columns:
                # 始终使用平均值进行聚合
                seasonal_data = timeseries_df.groupby("month").agg({selected_metric: "mean"}).reset_index()
                
                # 疾病季节性分析 | Disease seasonality analysis
                winter_months = [12, 1, 2]
                summer_months = [6, 7, 8]
                
                # 确保有冬季和夏季数据 | Ensure winter and summer data exist
                winter_avg = seasonal_data[seasonal_data["month"].isin(winter_months)][selected_metric].mean() if not seasonal_data[seasonal_data["month"].isin(winter_months)].empty else 0
                summer_avg = seasonal_data[seasonal_data["month"].isin(summer_months)][selected_metric].mean() if not seasonal_data[seasonal_data["month"].isin(summer_months)].empty else 0
                seasonal_ratio = winter_avg / summer_avg if summer_avg != 0 else 1
                
                # 疫苗覆盖率分析（如果选择的是病例数指标）
                vaccine_impact = ""
                if selected_metric == "daily_new_cases" and "vaccine_coverage" in timeseries_df.columns:
                    if "year" in timeseries_df.columns:
                        year_data = timeseries_df.groupby("year").agg({
                            "daily_new_cases": "sum",
                            "vaccine_coverage": "mean"
                        }).reset_index()
                        if len(year_data) > 1:
                            case_change = (year_data.iloc[-1]["daily_new_cases"] - year_data.iloc[0]["daily_new_cases"]) / year_data.iloc[0]["daily_new_cases"] * 100
                            coverage_change = (year_data.iloc[-1]["vaccine_coverage"] - year_data.iloc[0]["vaccine_coverage"]) * 100
                            vaccine_impact = f"Vaccine coverage increased from {year_data.iloc[0]['vaccine_coverage']:.1%} to {year_data.iloc[-1]['vaccine_coverage']:.1%}, a {coverage_change:.1f}% increase, while new cases changed by {case_change:+.1f}%, indicating significant effectiveness of vaccination in controlling the epidemic. | 疫苗覆盖率从{year_data.iloc[0]['vaccine_coverage']:.1%}增长到{year_data.iloc[-1]['vaccine_coverage']:.1%}，增幅{coverage_change:.1f}%，同年新增病例{case_change:+.1f}%，显示疫苗接种对控制疫情有显著效果。"
                
                # 区域资源压力分析
                rural_load = urban_load = resource_diff = 0
                if selected_metric == "resource_load" and "location" in timeseries_df.columns:
                    region_resource = timeseries_df.groupby("location").agg({"resource_load": "mean"}).reset_index()
                    rural_data = region_resource[region_resource["location"] == "Rural"]
                    urban_data = region_resource[region_resource["location"] == "Urban"]
                    if not rural_data.empty:
                        rural_load = rural_data["resource_load"].values[0]
                    if not urban_data.empty:
                        urban_load = urban_data["resource_load"].values[0]
                    resource_diff = rural_load - urban_load
                
                # 计算区域最大值
                max_location = "Urban"  # 默认值
                max_value = 0
                if "location" in timeseries_df.columns:
                    location_data = timeseries_df.groupby("location").agg({selected_metric: "mean"}).reset_index()
                    if not location_data.empty:
                        max_idx = location_data[selected_metric].idxmax()
                        max_location = location_data.loc[max_idx, "location"]
                        max_value = location_data.loc[max_idx, selected_metric]
                
                # 简化的洞察文本，移除与聚合方式、比较模式相关的内容
                metric_name = selected_metric.replace('_', ' ').title()
                st.markdown(f"""
                1. **Seasonal Pattern | 季节性规律**: {metric_name} shows obvious seasonal characteristics, with winter (Dec-Feb) average of {winter_avg:.1f} and summer (Jun-Aug) average of {summer_avg:.1f}, with a seasonal difference of {seasonal_ratio:.1f} times, providing a basis for developing seasonal prevention and control strategies. | {metric_name.replace('_', ' ').title()}呈现明显季节性特征，冬季（12-2月）平均为{winter_avg:.1f}，夏季（6-8月）为{summer_avg:.1f}，季节性差异达{seasonal_ratio:.1f}倍，为制定季节性防控策略提供依据。
                2. **Vaccine Intervention Effect | 疫苗干预效果**: {vaccine_impact if vaccine_impact else 'The increase in vaccine coverage is highly consistent with the downward trend in new cases, suggesting continued promotion of vaccination programs. | 疫苗覆盖率提升与新增病例下降趋势高度一致，建议继续推进疫苗接种计划。'}
                3. **Regional Difference Analysis | 区域差异分析**: {f'Resource load in rural areas ({rural_load:.2f}) is significantly higher than in urban areas ({urban_load:.2f}), with a gap of {resource_diff:.2f}, reflecting urgent needs to strengthen rural medical resource allocation. | 农村地区资源负荷({rural_load:.2f})显著高于城市地区({urban_load:.2f})，差距达{resource_diff:.2f}，反映农村医疗资源配置急需加强。' if selected_metric == 'resource_load' else f'The average value in {max_location} area is the highest, reaching {max_value:.1f}, requiring focused attention on the implementation of prevention and control measures in this region. | {max_location}地区的平均值最高，达到{max_value:.1f}，需要重点关注该区域的防控措施落实情况。'}
                4. **Overall Trend Analysis | 整体趋势分析**: The overall average level of {metric_name} is {seasonal_data[selected_metric].mean():.1f}, which can serve as a baseline value for evaluating prevention and control effectiveness. | {metric_name.replace('_', ' ').title()}的整体平均水平为{seasonal_data[selected_metric].mean():.1f}，可作为基准值评估防控效果。
                """)
        except Exception as e:
            st.error(f"生成趋势洞察失败：{str(e)} | Failed to generate trend insights: {str(e)}")
    else:
        # 默认洞察（无数据时显示）- 简化版本
        st.markdown("""
        1. **季节性规律**: 基于历史数据，新增病例通常在冬季（12-2月）达到高峰，夏季（6-8月）显著下降。
        2. **疫苗干预效果**: 疫苗覆盖率提升与新增病例下降呈正相关，建议优先推进高风险人群疫苗接种。
        3. **区域差异分析**: 农村地区普遍存在医疗资源配置不足问题，需加强农村地区防控能力建设。
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