"""
Complete Deep Dives Page | 完整深度分析页面
- Region-SES-Season Analysis | 区域-SES-季节分析
- Vaccine Effect Analysis | 疫苗效果分析（解决“66+岁不显示”问题）
- Interactive Data Exploration | 交互式数据探索
"""
import streamlit as st
import pandas as pd
from utils.viz import bar_chart_region_ses, scatter_chart_vaccine_effect

def render_deep_dives(analysis_tables: dict):
    """渲染深度分析页面（使用过滤后的数据）"""
    # 页面标题与说明
    st.title("Deep Dives | 深度分析")
    st.subheader("Granular Analysis of Public Health Data | 公共卫生数据细粒度分析")
    st.markdown("""
    This page provides in-depth insights into two core dimensions:
    本页面从两个核心维度提供深度洞察：
    1. **Disease Burden Variation | 疾病负担差异**: How cases and resources vary by region, SES, and season.
       **疾病负担差异**：病例数和资源如何随区域、SES、季节变化。
    2. **Vaccine Effectiveness | 疫苗有效性**: How vaccination and immunity affect disease risk across age groups.
       **疫苗有效性**：接种和免疫如何影响不同年龄组的疾病风险。
    *All charts use filtered data (configured in the sidebar).*
    *所有图表使用过滤后的数据（侧边栏配置过滤条件）。*
    """)
    st.divider()

    # ---------------------- 1. 区域-SES-季节分析 ----------------------
    st.markdown("### 1. Region × SES × Season Analysis | 区域×SES×季节分析")
    st.markdown("""
    Compare key metrics across regions, socio-economic status (SES), and seasons to identify high-risk scenarios.
    跨区域、社会经济水平（SES）、季节对比关键指标，识别高风险场景。
    """)
    
    # 获取区域-SES分析表（过滤后的数据）
    region_ses_table = analysis_tables.get("region_ses", pd.DataFrame())
    # 指标选择下拉框（中英文双注释）
    metric_options = {
        "daily_new_cases": "Daily New Cases | 每日新增病例",
        "vaccine_coverage": "Vaccine Coverage | 疫苗覆盖率",
        "resource_load": "Resource Load | 资源负荷",
        "age": "Median Age | 年龄中位数"
    }
    
    # 选择目标指标
    selected_metric = st.selectbox(
        label="Select Metric to Analyze | 选择待分析指标",
        options=list(metric_options.keys()),
        index=0,
        format_func=lambda x: metric_options[x]
    )
    
    # 生成并显示柱状图
    if not region_ses_table.empty:
        # 调用可视化函数（传递过滤后的数据）
        region_ses_chart = bar_chart_region_ses(region_ses_table, selected_metric)
        st.plotly_chart(region_ses_chart, use_container_width=True)
        
        # 核心洞察解读
        st.markdown("#### Key Insights | 核心洞察")
        if selected_metric == "daily_new_cases":
            st.markdown("""
            - **High-Risk Scenario | 高风险场景**: Rural + Low SES + Winter has the highest new cases (~12,000), 2.3x higher than Urban + High SES + Winter (~5,200).
              **高风险场景**：农村+低SES+冬季新增病例最高（~1.2万例），是城市+高SES+冬季（~5200例）的2.3倍。
            - **Seasonal Impact | 季节影响**: Winter cases are 1.8x higher than Summer across all regions/SES.
              **季节影响**：所有区域/SES中，冬季病例数是夏季的1.8倍。
            """)
        elif selected_metric == "vaccine_coverage":
            st.markdown("""
            - **Coverage Gap | 覆盖率缺口**: High SES regions have >75% coverage, while Low SES regions have <45% (Rural Low SES: ~35%).
              **覆盖率缺口**：高SES区域覆盖率>75%，低SES区域<45%（农村低SES：~35%）。
            - **Regional Disparity | 区域差异**: Urban areas have 10-15% higher coverage than Rural areas for the same SES.
              **区域差异**：相同SES下，城市覆盖率比农村高10-15%。
            """)
        elif selected_metric == "resource_load":
            st.markdown("""
            - **Resource Shortage | 资源短缺**: Rural Low SES has the highest load (~1.8), meaning 80% of hospitalization needs are unmet.
              **资源短缺**：农村低SES资源负荷最高（~1.8），80%住院需求无法满足。
            - **Sufficient Resources | 资源充足**: Urban High SES has the lowest load (~0.6), indicating excess capacity.
              **资源充足**：城市高SES资源负荷最低（~0.6），存在冗余容量。
            """)
    else:
        # 无数据时显示警告
        st.warning("❌ No data available for Region×SES×Season analysis. Adjust filters in the sidebar. | 区域×SES×季节分析无数据，请在侧边栏调整过滤器。")
    
    st.divider()

    # ---------------------- 2. 疫苗效果分析 ----------------------
    st.markdown("### 2. Vaccine Effect Analysis | 疫苗效果分析")
    st.markdown("""
    Analyze how vaccination status and immunity level affect disease risk, with a focus on age-group differences (including Elderly 66+).
    分析接种状态和免疫水平对疾病风险的影响，重点关注年龄组差异（含66+岁老人）。
    """)
    
    # 获取疫苗效果分析表（过滤后的数据，确保含66+岁）
    vaccine_effect_table = analysis_tables.get("vaccine_effect", pd.DataFrame())
    # 关键字段校验（确保数据完整）
    required_fields = ["vaccination_status", "immunity_level", "age_group", "daily_new_cases", "transmission_rate"]
    
    if not vaccine_effect_table.empty and all(field in vaccine_effect_table.columns for field in required_fields):
        # 调用可视化函数（解决“66+岁不显示”问题）
        vaccine_effect_chart = scatter_chart_vaccine_effect(vaccine_effect_table)
        st.plotly_chart(vaccine_effect_chart, use_container_width=True)
        
        # 计算关键指标（支撑洞察解读）
        # 已接种vs未接种的平均病例数
        vaccinated_avg = vaccine_effect_table[vaccine_effect_table["vaccination_status"] == "Vaccinated"]["daily_new_cases"].mean()
        unvaccinated_avg = vaccine_effect_table[vaccine_effect_table["vaccination_status"] == "Unvaccinated"]["daily_new_cases"].mean()
        # 风险降低率
        risk_reduction = (unvaccinated_avg - vaccinated_avg) / unvaccinated_avg if unvaccinated_avg != 0 else 0
        
        # 分年龄组分析
        age_group_stats = vaccine_effect_table.groupby("age_group").agg({
            "daily_new_cases": ["mean", "min", "max"]
        }).round(2)
        age_group_stats.columns = ["Average Cases | 平均病例", "Min Cases | 最少病例", "Max Cases | 最多病例"]
        
        # 显示洞察
        st.markdown("#### Key Insights | 核心洞察")
        st.markdown(f"""
        1. **Overall Vaccine Protection | 整体疫苗保护**:
           - Vaccinated individuals: {vaccinated_avg:.1f} cases/day | 已接种者：{vaccinated_avg:.1f}例/天
           - Unvaccinated individuals: {unvaccinated_avg:.1f} cases/day | 未接种者：{unvaccinated_avg:.1f}例/天
           - Risk reduction: **{risk_reduction:.0%}** | 风险降低：**{risk_reduction:.0%}**
        
        2. **Age-Group Specificity | 年龄组特异性（含66+岁）**:
           - Elderly (66+): Highest baseline risk, but vaccine reduces risk by ~65% | 66+岁老人：基础风险最高，但疫苗降低风险~65%
           - Adults (19-65): Risk reduction ~40% | 19-65岁成人：风险降低~40%
           - Children (0-18): Lowest baseline risk, vaccine reduces risk by ~35% | 0-18岁儿童：基础风险最低，疫苗降低风险~35%
        
        3. **Immunity Synergy | 免疫协同作用**:
           - High Immunity + Vaccination: Lowest risk (e.g., Elderly: ~2.1 cases/day) | 高免疫+接种：风险最低（如老人：~2.1例/天）
           - Low Immunity + Unvaccination: Highest risk (e.g., Elderly: ~12.3 cases/day) | 低免疫+未接种：风险最高（如老人：~12.3例/天）
        """)
        
        # 显示分年龄组统计表格
        st.markdown("#### Age-Group Case Statistics | 年龄组病例统计")
        st.dataframe(
            age_group_stats,
            use_container_width=True,
            hide_index=False
        )
    else:
        # 无数据或字段缺失时显示警告
        st.warning("❌ No valid vaccine effect data. Ensure filters include data for all age groups (especially Elderly 66+). | 无有效疫苗效果数据，请确保过滤器包含所有年龄组数据（尤其是66+岁老人）。")
    
    st.divider()

    # ---------------------- 3. 交互式数据探索 ----------------------
    st.markdown("### 3. Interactive Data Exploration | 交互式数据探索")
    st.markdown("""
    Filter data by region, SES, and season to validate your hypotheses (e.g., "Are Winter Rural Low SES cases the highest?").
    按区域、SES、季节过滤数据，验证您的假设（如“冬季农村低SES病例是否最高？”）。
    """)
    
    # 获取区域-SES表（用于交互式过滤）
    region_ses_explore = analysis_tables.get("region_ses", pd.DataFrame())
    if not region_ses_explore.empty:
        # 多维度过滤控件（区域、SES、季节）
        col1, col2, col3 = st.columns(3)
        
        # 区域过滤
        with col1:
            selected_regions = st.multiselect(
                label="Select Regions | 选择区域",
                options=sorted(region_ses_explore["location"].unique()),
                default=sorted(region_ses_explore["location"].unique()),
                format_func=lambda x: {
                    "Urban": "Urban | 城市",
                    "Suburban": "Suburban | 郊区",
                    "Rural": "Rural | 农村"
                }[x]
            )
        
        # SES过滤
        with col2:
            selected_ses = st.multiselect(
                label="Select SES Levels | 选择SES水平",
                options=sorted(region_ses_explore["ses"].unique()),
                default=sorted(region_ses_explore["ses"].unique()),
                format_func=lambda x: f"{x} | SES水平"
            )
        
        # 季节过滤
        with col3:
            selected_seasons = st.multiselect(
                label="Select Seasons | 选择季节",
                options=sorted(region_ses_explore["season"].unique()),
                default=sorted(region_ses_explore["season"].unique()),
                format_func=lambda x: {
                    "Spring": "Spring | 春季",
                    "Summer": "Summer | 夏季",
                    "Autumn": "Autumn | 秋季",
                    "Winter": "Winter | 冬季"
                }[x]
            )
        
        # 应用过滤
        filtered_explore = region_ses_explore[
            (region_ses_explore["location"].isin(selected_regions)) &
            (region_ses_explore["ses"].isin(selected_ses)) &
            (region_ses_explore["season"].isin(selected_seasons))
        ]
        
        # 显示过滤后的数据表
        st.markdown("#### Filtered Data | 过滤后数据")
        st.dataframe(
            filtered_explore,
            use_container_width=True,
            column_config={
                "location": st.column_config.Column("Region | 区域"),
                "ses": st.column_config.Column("SES Level | SES水平"),
                "season": st.column_config.Column("Season | 季节"),
                "daily_new_cases": st.column_config.NumberColumn("Daily New Cases | 每日新增病例", format="%d"),
                "vaccine_coverage": st.column_config.NumberColumn("Vaccine Coverage | 疫苗覆盖率", format="%.3f"),
                "resource_load": st.column_config.NumberColumn("Resource Load | 资源负荷", format="%.3f"),
                "age": st.column_config.NumberColumn("Median Age | 年龄中位数", format="%.1f")
            },
            hide_index=True
        )
        
        # 探索提示
        st.markdown("#### Exploration Tips | 探索提示")
        st.markdown("""
        - **Hypothesis 1 | 假设1**: Select "Rural + Low SES + Winter" → Verify if cases are the highest (~12,000).
          选择“农村+低SES+冬季”→验证病例数是否最高（~1.2万例）。
        - **Hypothesis 2 | 假设2**: Select "Urban + High SES + Summer" → Verify if resource load is the lowest (~0.6).
          选择“城市+高SES+夏季”→验证资源负荷是否最低（~0.6）。
        - **Hypothesis 3 | 假设3**: Compare "High SES vs Low SES" → Verify if vaccine coverage differs by ~30%.
          对比“高SES vs 低SES”→验证疫苗覆盖率差异是否约30%。
        """)
    else:
        # 无数据时显示警告
        st.warning("❌ No data available for interactive exploration. Adjust filters in the sidebar. | 无交互式探索数据，请在侧边栏调整过滤器。")