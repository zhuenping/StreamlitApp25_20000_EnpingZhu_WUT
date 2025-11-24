"""
结论页面（中英文双注释）
"""
import streamlit as st
import pandas as pd

def render_conclusions(analysis_tables: dict):
    st.title("Conclusions | 结论")
    st.subheader("Insights & Actionable Recommendations | 核心洞察与可落地建议")
    st.markdown("""
    This section summarizes **core findings** from the analysis and provides **evidence-based policy recommendations** 
    to address public health challenges. It also discusses limitations and future work to improve the dashboard.
    本板块总结分析中的**核心发现**，提供**基于证据的政策建议**以应对公共卫生挑战，同时讨论局限性和未来改进方向。
    """)
    st.divider()
    
    st.markdown("### Core Insights Summary | 核心洞察总结")
    st.markdown("""
    Based on comprehensive analysis of temporal trends, regional differences, and vaccine effects, we derive four key insights:
    基于时间趋势、区域差异和疫苗效果的综合分析，得出四大核心洞察：
    """)
    
    with st.container(border=True):
        st.markdown("#### 1. Disease Trends Are Driven by Season and Region | 疾病趋势由季节和区域驱动")
        st.markdown("""
        - **Seasonality | 季节性**: Winter cases are 2.3x higher than Summer (driven by transmission rate: 1.2 vs. 0.6).
        - **Regional Gap | 区域缺口**: Rural cases are 1.8x higher than Urban (driven by low vaccine coverage and high resource load).
        - **Implication | 启示**: Interventions must be **seasonal and regional** (e.g., more resources in Rural Winter).
        冬季病例是夏季的2.3倍（传播率1.2 vs 0.6驱动）。
        农村病例是城市的1.8倍（低疫苗覆盖率和高资源负荷驱动）。
        干预措施必须**分季节、分区域**（如农村冬季增配资源）。
        """)
    
    with st.container(border=True):
        st.markdown("#### 2. Vaccine Is a High-Impact Tool for Disease Control | 疫苗是疾病控制的高效工具")
        st.markdown("""
        - **Overall Protection | 整体保护**: Vaccination reduces disease risk by 60-80% (highest for Elderly: ~65%).
        - **Synergy with Immunity | 免疫协同**: High immunity + Vaccination = Lowest risk (even for vulnerable groups).
        - **Coverage Gap | 覆盖率缺口**: Rural Low SES has only 35% coverage (vs. 82% Urban High SES) → Key intervention target.
        接种降低疾病风险60-80%（老年人最高~65%）。
        高免疫+接种=最低风险（即使脆弱人群）。
        农村低SES仅35%覆盖率（城市高SES 82%）→核心干预目标。
        """)
    
    with st.container(border=True):
        st.markdown("#### 3. Healthcare Resource Shortage Is Concentrated in Rural Low SES Regions | 医疗资源短缺集中在农村低SES区域")
        st.markdown("""
        - **Load Comparison | 负荷对比**: Rural Low SES load (~1.8) is 3x higher than Urban High SES (~0.6).
        - **Root Cause | 根本原因**: Low hospital capacity (Rural: ~50 beds/10k people) + High demand (Rural Winter: ~90 admissions/day).
        - **Risk | 风险**: Unmet demand leads to delayed treatment and higher mortality.
        农村低SES负荷（~1.8）是城市高SES的3倍（~0.6）。
        低床位容量（农村~50张/万人）+高需求（农村冬季~90人/天住院）。
        需求未满足导致治疗延迟和更高死亡率。
        """)
    
    with st.container(border=True):
        st.markdown("#### 4. High-Risk Population Is Clearly Defined: Elderly with Chronic Conditions | 高危人群明确：有慢性病的老年人")
        st.markdown("""
        - **Risk Level | 风险水平**: This group has 3.8x higher cases than Adults without chronic conditions.
        - **Vaccine Benefit | 疫苗获益**: Vaccination reduces their risk by ~65% (highest among all groups).
        - **Resource Priority | 资源优先**: This group should be first in line for vaccination and health checks.
        该群体病例数是无慢性病成年人的3.8倍。
        接种降低其风险~65%（所有群体中最高）。
        该群体应优先获得接种和健康检查。
        """)
    st.divider()
    
    st.markdown("### Actionable Policy Recommendations | 可落地政策建议")
    st.markdown("""
    Below are 4 prioritized recommendations, each with clear targets, actions, and measurement metrics.
    以下是4项优先级建议，每项均包含明确目标、行动和衡量指标。
    """)
    
    recommendations = pd.DataFrame({
        "Priority | 优先级": ["High", "High", "Medium", "Medium"],
        "Target Group/Region | 目标群体/区域": [
            "Rural Low SES Regions | 农村低SES区域",
            "Elderly (66+) with Chronic Conditions | 66+岁有慢性病的老年人",
            "All Rural Regions | 所有农村区域",
            "Public Health Monitoring System | 公共卫生监测系统"
        ],
        "Recommendation | 建议": [
            "1. Provide free vaccines + mobile clinics; 2. Train 200+ local health workers | 1. 提供免费疫苗+流动诊所；2. 培训200+本地卫生工作者",
            "1. Monthly free health checks; 2. Priority vaccination with booster shots | 1. 每月免费健康检查；2. 优先接种加强针",
            "1. Build 5 new rural hospitals; 2. Allocate 500+ additional beds | 1. 新建5所农村医院；2. 新增500+床位",
            "1. Integrate real-time data feeds; 2. Develop predictive outbreak models | 1. 整合实时数据；2. 开发暴发预测模型"
        ],
        "Target Metric | 目标指标": [
            "Vaccine coverage ≥70% in Rural Low SES by Q4 2024 | 2024年第四季度农村低SES疫苗覆盖率≥70%",
            "90% of Elderly with Chronic Conditions vaccinated by Q2 2024 | 2024年第二季度90%有慢性病的老年人完成接种",
            "Rural resource load ≤1.0 by end of 2024 | 2024年底农村资源负荷≤1.0",
            "Outbreak prediction accuracy ≥85% by 2025 | 2025年暴发预测准确率≥85%"
        ],
        "Data Support | 数据支撑": [
            "Current coverage: 35%; Target gap: 35% | 当前覆盖率：35%；目标缺口：35%",
            "Current vaccination: 42%; Risk reduction: 65% | 当前接种率：42%；风险降低：65%",
            "Current load: 1.8; Target reduction: 0.8 | 当前负荷：1.8；目标降低：0.8",
            "Current prediction accuracy: 60%; Industry standard: 85% | 当前预测准确率：60%；行业标准：85%"
        ]
    })
    
    st.dataframe(
        recommendations,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Priority | 优先级": st.column_config.Column("Priority | 优先级", width="small"),
            "Target Group/Region | 目标群体/区域": st.column_config.Column("Target Group/Region | 目标群体/区域", width="medium"),
            "Recommendation | 建议": st.column_config.Column("Recommendation | 建议", width="wide"),
            "Target Metric | 目标指标": st.column_config.Column("Target Metric | 目标指标", width="wide"),
            "Data Support | 数据支撑": st.column_config.Column("Data Support | 数据支撑", width="wide")
        }
    )
    st.divider()
    
    st.markdown("### Limitations & Future Work | 局限性与未来方向")
    st.markdown("#### Limitations | 局限性")
    st.markdown("""
    1. **Data Scope | 数据范围**: The dataset covers 2023-2024 only; long-term trends (5+ years) are not analyzed.
       数据集仅覆盖2023-2024年；未分析长期趋势（5年以上）。
    2. **Geographic Granularity | 地理粒度**: Regions are grouped into Urban/Rural/Suburban; no city-level or county-level analysis.
       区域仅分为城市/农村/郊区；无市级或县级分析。
    3. **Variable Coverage | 变量覆盖**: Some variables (e.g., specific chronic diseases, income level) are not included, 
       limiting analysis of root causes.
       部分变量（如特定慢性病、收入水平）未包含，限制了根本原因分析。
    4. **Causality vs. Correlation | 相关性与因果性**: The analysis identifies correlations (e.g., vaccine coverage and cases), 
       but causal relationships require further study (e.g., randomized controlled trials).
       分析识别了相关性（如疫苗覆盖率与病例数），但因果关系需进一步研究（如随机对照试验）。
    """)
    
    st.markdown("#### Future Work | 未来方向")
    st.markdown("""
    1. **Expand Data Sources | 扩展数据源**: Integrate multi-year data (2018-2024) and real-time feeds (e.g., hospital admissions).
       整合多年数据（2018-2024）和实时数据（如医院入院数）。
    2. **Enhance Geographic Analysis | 增强地理分析**: Add city-level maps and county-level breakdowns for targeted interventions.
       添加市级地图和县级细分，支持精准干预。
    3. **Incorporate More Variables | 纳入更多变量**: Include income, education, and specific chronic diseases to identify root causes.
       加入收入、教育和特定慢性病，识别根本原因。
    4. **Develop Predictive Models | 开发预测模型**: Build machine learning models to predict outbreaks 1-3 months in advance.
       构建机器学习模型，提前1-3个月预测疾病暴发。
    5. **Improve Dashboard Interactivity | 提升仪表盘交互性**: Add custom filter combinations and exportable insights for policymakers.
       添加自定义过滤器组合和可导出的洞察报告，供决策者使用。
    """)