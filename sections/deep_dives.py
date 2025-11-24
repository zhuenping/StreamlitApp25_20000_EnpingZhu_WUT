"""
Complete Deep Dives Page | 完整深度分析页面
- Region-SES-Season Analysis | 区域-SES-季节分析
- Vaccine Effect Analysis | 疫苗效果分析（解决"66+岁不显示"问题）
- Interactive Data Exploration | 交互式数据探索
"""
import streamlit as st
import pandas as pd
import plotly.express as px  # 添加这行导入
from utils.viz import bar_chart_region_ses, scatter_chart_vaccine_effect, bar_chart_vaccine_effect

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
        
        # 动态计算洞察数据
        if not region_ses_table.empty:
            # 找出最大值和最小值组合
            max_value_row = region_ses_table.loc[region_ses_table[selected_metric].idxmax()]
            min_value_row = region_ses_table.loc[region_ses_table[selected_metric].idxmin()]
            
            # 季节性比较
            winter_data = region_ses_table[region_ses_table["season"] == "Winter"][selected_metric].mean()
            summer_data = region_ses_table[region_ses_table["season"] == "Summer"][selected_metric].mean()
            season_ratio = winter_data / summer_data if summer_data != 0 else 1
            
            if selected_metric == "daily_new_cases":
                st.markdown(f"""
                - **High-Risk Scenario | 高风险场景**: {max_value_row['location']} + {max_value_row['ses']} SES + {max_value_row['season']}的病例数最高 ({max_value_row[selected_metric]:,.0f})，比{min_value_row['location']} + {min_value_row['ses']} SES + {min_value_row['season']}高{max_value_row[selected_metric]/min_value_row[selected_metric]:.1f}倍。
                - **Seasonal Impact | 季节影响**: 在所有区域/SES中，{max_value_row['season']}的病例数比{min_value_row['season']}高{season_ratio:.1f}倍。
                """)
            elif selected_metric == "vaccine_coverage":
                high_ses_avg = region_ses_table[region_ses_table["ses"] == "High"][selected_metric].mean()
                low_ses_avg = region_ses_table[region_ses_table["ses"] == "Low"][selected_metric].mean()
                coverage_diff = high_ses_avg - low_ses_avg
                st.markdown(f"""
                - **Coverage Gap | 覆盖率缺口**: High SES areas have a coverage rate of {high_ses_avg:.1%}, while low SES areas have {low_ses_avg:.1%}, with a gap of {coverage_diff:.1%}. | 高SES区域覆盖率为{high_ses_avg:.1%}，低SES区域为{low_ses_avg:.1%}，差距为{coverage_diff:.1%}。
                - **Regional Disparity | 区域差异**: {max_value_row['location']} area has the highest coverage rate ({max_value_row[selected_metric]:.1%}), while {min_value_row['location']} area has the lowest ({min_value_row[selected_metric]:.1%}). | {max_value_row['location']}地区覆盖率最高 ({max_value_row[selected_metric]:.1%})，而{min_value_row['location']}地区最低 ({min_value_row[selected_metric]:.1%})。
                """)
            elif selected_metric == "resource_load":
                st.markdown(f"""
                - **Resource Shortage | 资源短缺**: {max_value_row['location']} + {max_value_row['ses']} SES has the highest resource load ({max_value_row[selected_metric]:.2f}), indicating significant resource pressure. | {max_value_row['location']} + {max_value_row['ses']} SES资源负荷最高 ({max_value_row[selected_metric]:.2f})，表明资源压力显著。
                - **Sufficient Resources | 资源充足**: {min_value_row['location']} + {min_value_row['ses']} SES has the lowest resource load ({min_value_row[selected_metric]:.2f}), indicating excess capacity. | {min_value_row['location']} + {min_value_row['ses']} SES资源负荷最低 ({min_value_row[selected_metric]:.2f})，表明容量过剩。
                """)
        else:
            # 默认洞察（无数据时显示） | Default insights (when no data)
            if selected_metric == "daily_new_cases":
                st.markdown("""
                - **High-Risk Scenario | 高风险场景**: Rural + Low SES + Winter typically has the highest number of cases. | 农村+低SES+冬季通常病例数最高。
                - **Seasonal Impact | 季节影响**: In all regions/SES, winter cases are typically higher than summer cases. | 在所有区域/SES中，冬季病例数通常高于夏季。
                """)
            elif selected_metric == "vaccine_coverage":
                st.markdown("""
                - **Coverage Gap | 覆盖率缺口**: High SES areas typically have higher coverage rates than low SES areas. | 高SES区域通常比低SES区域覆盖率高。
                - **Regional Disparity | 区域差异**: Urban areas typically have higher coverage rates than rural areas. | 城市地区通常比农村地区覆盖率高。
                """)
            elif selected_metric == "resource_load":
                st.markdown("""
                - **Resource Shortage | 资源短缺**: Rural low SES typically has the highest resource load. | 农村低SES通常资源负荷最高。
                - **Sufficient Resources | 资源充足**: Urban high SES typically has the lowest resource load. | 城市高SES通常资源负荷最低。
                """)
    else:
        # 无数据时显示警告 | Show warning when no data available
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
        # 调用可视化函数
        vaccine_effect_chart = bar_chart_vaccine_effect(vaccine_effect_table)
        st.plotly_chart(vaccine_effect_chart, use_container_width=True)
        
        # 计算关键指标（支撑洞察解读）
        vaccinated_data = vaccine_effect_table[vaccine_effect_table["vaccination_status"] == "Vaccinated"]
        unvaccinated_data = vaccine_effect_table[vaccine_effect_table["vaccination_status"] == "Unvaccinated"]
        
        # 安全计算平均病例数
        vaccinated_avg = vaccinated_data["daily_new_cases"].mean() if not vaccinated_data.empty else 0
        unvaccinated_avg = unvaccinated_data["daily_new_cases"].mean() if not unvaccinated_data.empty else 0
        
        # 风险降低率计算（修复计算逻辑）
        if unvaccinated_avg <= 0:
            risk_reduction = 0
            st.warning("⚠️ 数据异常：未接种组病例数为0或负数，无法计算准确的风险降低率。 | Warning: Abnormal data - unvaccinated cases are zero or negative, cannot calculate accurate risk reduction.")
        elif vaccinated_avg > unvaccinated_avg * 1.05:  # 设置合理阈值，避免微小差异触发警告
            risk_reduction = (unvaccinated_avg - vaccinated_avg) / unvaccinated_avg
            st.warning(f"⚠️ 数据异常：已接种组病例数({vaccinated_avg:.1f})高于未接种组({unvaccinated_avg:.1f})。请检查数据质量或考虑其他影响因素。 | Warning: Abnormal data - vaccinated cases higher than unvaccinated, possible data error or other influencing factors.")
        else:
            risk_reduction = (unvaccinated_avg - vaccinated_avg) / unvaccinated_avg
        
        # 分年龄组分析 - 动态计算各年龄组的风险降低率
        age_group_stats = vaccine_effect_table.groupby("age_group").agg({
            "daily_new_cases": ["mean", "min", "max"]
        }).round(2)
        age_group_stats.columns = ["Average Cases | 平均病例", "Min Cases | 最少病例", "Max Cases | 最多病例"]
        
        # 动态计算各年龄组的疫苗效果
        age_group_effects = {}
        for age_group in ["Child (0-18)", "Adult (19-65)", "Elderly (66+)"]:
            age_group_data = vaccine_effect_table[vaccine_effect_table["age_group"] == age_group]
            if not age_group_data.empty:
                vac_data = age_group_data[age_group_data["vaccination_status"] == "Vaccinated"]
                unvac_data = age_group_data[age_group_data["vaccination_status"] == "Unvaccinated"]
                
                vac_cases = vac_data["daily_new_cases"].mean() if not vac_data.empty else 0
                unvac_cases = unvac_data["daily_new_cases"].mean() if not unvac_data.empty else 0
                
                age_group_effect = ((unvac_cases - vac_cases) / unvac_cases * 100) if unvac_cases != 0 else 0
                age_group_effects[age_group] = age_group_effect
        
        # 免疫协同作用分析 - 动态计算最低和最高风险组
        if not vaccine_effect_table.empty:
            lowest_risk_group = vaccine_effect_table.sort_values("daily_new_cases").iloc[0]
            highest_risk_group = vaccine_effect_table.sort_values("daily_new_cases", ascending=False).iloc[0]
        else:
            # 设置默认值避免错误
            lowest_risk_group = pd.Series({"immunity_level": "High", "vaccination_status": "Vaccinated", "daily_new_cases": 0})
            highest_risk_group = pd.Series({"immunity_level": "Low", "vaccination_status": "Unvaccinated", "daily_new_cases": 0})
        
        # 显示洞察 | Display insights
        st.markdown("#### Key Insights | 核心洞察")
        
        # 确保显示核心洞察内容
        st.markdown(f"""
        1. **Overall Vaccine Protection | 整体疫苗保护**:
           - Vaccinated individuals: {vaccinated_avg:.1f} cases/day | 已接种者：{vaccinated_avg:.1f}例/天
           - Unvaccinated individuals: {unvaccinated_avg:.1f} cases/day | 未接种者：{unvaccinated_avg:.1f}例/天
           - Risk reduction: **{risk_reduction:.0%}** | 风险降低：**{risk_reduction:.0%}**
        
        2. **Age-Group Specificity | 年龄组特异性（含66+岁）**:
           - Elderly (66+): Vaccine reduces risk by **{age_group_effects.get('Elderly (66+)', 0):.0f}%** | 66+岁老人：疫苗降低风险**{age_group_effects.get('Elderly (66+)', 0):.0f}%**
           - Adults (19-65): Vaccine reduces risk by **{age_group_effects.get('Adult (19-65)', 0):.0f}%** | 19-65岁成人：疫苗降低风险**{age_group_effects.get('Adult (19-65)', 0):.0f}%**
           - Children (0-18): Vaccine reduces risk by **{age_group_effects.get('Child (0-18)', 0):.0f}%** | 0-18岁儿童：疫苗降低风险**{age_group_effects.get('Child (0-18)', 0):.0f}%**
        
        3. **Immunity Synergy | 免疫协同作用**:
           - Lowest Risk: {lowest_risk_group['immunity_level']} Immunity + {lowest_risk_group['vaccination_status']} with {lowest_risk_group['daily_new_cases']:.1f} cases/day | 最低风险：{lowest_risk_group['immunity_level']}免疫+{lowest_risk_group['vaccination_status']}，{lowest_risk_group['daily_new_cases']:.1f}例/天
           - Highest Risk: {highest_risk_group['immunity_level']} Immunity + {highest_risk_group['vaccination_status']} with {highest_risk_group['daily_new_cases']:.1f} cases/day | 最高风险：{highest_risk_group['immunity_level']}免疫+{highest_risk_group['vaccination_status']}，{highest_risk_group['daily_new_cases']:.1f}例/天
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
    按区域、SES、季节过滤数据，验证您的假设（如"冬季农村低SES病例是否最高？"）。
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
          选择"农村+低SES+冬季"→验证病例数是否最高（~1.2万例）。
        - **Hypothesis 2 | 假设2**: Select "Urban + High SES + Summer" → Verify if resource load is the lowest (~0.6).
          选择"城市+高SES+夏季"→验证资源负荷是否最低（~0.6）。
        - **Hypothesis 3 | 假设3**: Compare "High SES vs Low SES" → Verify if vaccine coverage differs by ~30%.
          对比"高SES vs 低SES"→验证疫苗覆盖率差异是否约30%。
        """)
    else:
        # 无数据时显示警告
        st.warning("❌ No data available for interactive exploration. Adjust filters in the sidebar. | 无交互式探索数据，请在侧边栏调整过滤器。")
    # 交互式数据探索模块结束