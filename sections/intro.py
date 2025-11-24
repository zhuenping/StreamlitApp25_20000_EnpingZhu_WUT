"""
项目介绍页面（正常完整版）
- 完整叙事钩子：背景→目标→数据说明→导航
- 符合高分项目的透明性要求
- 新增：个人所属院校Logo展示（武汉理工大学 + EFREI Paris）
"""
import streamlit as st
from utils.io import get_data_caveats

def render_intro():
    """渲染完整项目介绍页面（含个人所属院校Logo）"""
    # 1. 标题与钩子（吸引注意力）
    st.title("Public Health Surveillance Dashboard: Tracking Disease Trends & Vaccine Impact")
    st.subheader("公共卫生监测仪表盘：追踪疾病趋势与疫苗影响")
    st.divider()
    
    # 2. 项目背景（Why it matters，叙事核心）
    st.markdown("### 1. Project Background | 项目背景")
    st.markdown("""
    Public health surveillance is the cornerstone of effective disease prevention and control. 
    In the context of global health challenges, understanding **temporal trends**, **regional differences**, 
    and **vaccine effectiveness** is critical for:
    公共卫生监测是有效防控疾病的基石。在全球健康挑战背景下，理解**时间趋势**、**区域差异**和**疫苗效果**对以下工作至关重要：
    - Early detection of disease outbreaks (e.g., winter peak of respiratory diseases).
      疾病暴发早期检测（如呼吸道疾病冬季高峰）。
    - Rational allocation of healthcare resources (e.g., beds in rural areas).
      医疗资源合理分配（如农村地区床位调配）。
    - Evaluation of public health policies (e.g., vaccine distribution strategies).
      公共卫生政策评估（如疫苗分配策略）。
    - Protection of high-risk populations (e.g., elderly with chronic conditions).
      高危人群保护（如有慢性病的老年人）。
    
    This dashboard leverages a comprehensive public health dataset (2023-2024) to answer these key questions, 
    providing data-driven insights for policymakers.
    本仪表盘基于2023-2024年完整公共卫生数据集，解答上述核心问题，为决策者提供数据驱动的洞察。
    """)
    
    # 3. 项目目标（Learning objectives，高分必备）
    st.markdown("### 2. Project Objectives | 项目目标")
    st.markdown("""
    This dashboard is designed to achieve four core objectives:
    本仪表盘旨在实现四大核心目标：
    1. **Tell a data-driven story**: Guide users from problem identification (e.g., "Why are rural cases higher?") 
       to actionable insights (e.g., "Increase vaccine access in rural areas").
       **讲述数据驱动故事**：引导用户从问题识别（如“为何农村病例更高？”）到可落地洞察（如“提升农村疫苗可及性”）。
    2. **Enable interactive exploration**: Allow users to filter data by year, region, and metric, 
       discovering hidden patterns (e.g., "Winter + Rural + Low SES = Highest cases").
       **支持交互式探索**：用户可按年份、区域、指标过滤数据，发现隐藏模式（如“冬季+农村+低SES=最高病例数”）。
    3. **Ensure transparency**: Document data sources, cleaning rules, and limitations, 
       building trust in analysis results.
       **确保透明度**：记录数据来源、清洗规则和局限性，建立对分析结果的信任。
    4. **Support decision-making**: Translate complex data into clear, actionable recommendations 
       (e.g., "Prioritize vaccination for elderly in rural Low SES regions").
       **支持决策制定**：将复杂数据转化为清晰、可落地的建议（如“优先为农村低SES区域老年人接种”）。
    """)
    
    # 4. 数据集说明（透明性，完整字段解释）
    st.markdown("### 3. Dataset Overview | 数据集概览")
    st.markdown(get_data_caveats())
    
    # 5. 导航指引（用户旅程，提升体验）
    st.markdown("### 4. Dashboard Navigation | 仪表盘导航")
    st.markdown("""
    Use the sidebar to filter data and explore four core sections:
    使用侧边栏过滤数据，探索四大核心板块：
    - **Overview**: High-level KPIs (total cases, average vaccination rate) and time series trends, 
      providing a quick snapshot of public health status.
      **概览**：高层级KPI（总病例数、平均接种率）和时间序列趋势，快速了解公共卫生状况。
    - **Deep Dives**: Detailed analysis of region-SES differences and vaccine effectiveness, 
      revealing hidden patterns behind the data.
      **深度分析**：区域-SES差异和疫苗效果的详细分析，揭示数据背后的隐藏模式。
    - **Conclusions**: Summary of core insights and evidence-based policy recommendations, 
      translating data into action.
      **结论**：核心洞察总结和基于证据的政策建议，将数据转化为行动。
    """)
    
    # 6. 个人所属院校Logo展示（核心修改：突出个人关联，非合作）
    st.divider()
    st.markdown("### 🏫 Affiliation | 所属院校")
    
    # 分栏展示两所院校Logo（居中对齐，大小统一，符合个人多院校关联场景）
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.image(
            "assets/wut_logo.png",  # 武汉理工大学Logo路径
            caption="Wuhan University of Technology | 武汉理工大学",
            width=250,  # 统一宽度，保持美观
            use_column_width=False
        )
    with col2:
        st.image(
            "assets/efrei_logo.png",  # EFREI Paris Logo路径
            caption="EFREI Paris | 法国巴黎电子与信息工程学院",
            width=250,
            use_column_width=False
        )
    
    # 原有项目信息（保持不变，放在Logo下方）
    st.divider()
    st.caption("""
    **Project Info | 项目信息**  
    Author | 作者：Zhu Enping  
    Mentor | 导师：Mano Joseph Mathew  
    Email | 邮箱：1305927014@qq.com  
    Tags | 标签：#EFREIDataStoriesWUT2025 #EFREIParis #DataVisualization #Streamlit #DataStorytelling  
    License | 许可证：Academic Use Only（仅用于学术用途）
    """)