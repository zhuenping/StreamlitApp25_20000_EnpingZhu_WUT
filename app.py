import streamlit as st
import pandas as pd
from utils.prep import get_processed_data
from sections import intro, overview, deep_dives, conclusions

# 页面基础配置
st.set_page_config(
    page_title="Public Health Surveillance Dashboard | 公共卫生监测仪表盘",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 侧边栏核心功能：过滤器 + 页面导航
with st.sidebar:
    # 添加学校图标到侧边栏顶部
    st.image(
        "assets/wut_logo.png",  # 武汉理工大学Logo路径
        use_container_width=True  # 自适应侧边栏宽度
    )
    st.image(
        "assets/efrei_logo.png",  # EFREI Paris Logo路径
        use_container_width=True  # 自适应侧边栏宽度
    )
    st.divider()
    
    # 1. 数据过滤器（年份+区域，解决"过滤器无作用"问题）
    st.title("Data Filters | 数据过滤器")
    st.markdown("Filter data by time and region to focus on specific scenarios. | 按时间和区域过滤数据，聚焦特定场景。")
    
    # 年份选择（默认包含2023-2024，可根据实际数据集调整）
    available_years = [2023, 2024]
    selected_years = st.multiselect(
        label="Select Years | 选择年份",
        options=available_years,
        default=available_years,
        format_func=lambda x: f"{x} Year | 年份"
    )
    
    # 区域选择（默认包含所有区域）
    available_regions = ["Urban", "Suburban", "Rural"]
    selected_regions = st.multiselect(
        label="Select Regions | 选择区域",
        options=available_regions,
        default=available_regions,
        format_func=lambda x: {
            "Urban": "Urban | 城市",
            "Suburban": "Suburban | 郊区",
            "Rural": "Rural | 农村"
        }[x]
    )
    
    st.divider()  # 分割线
    
    # 2. 页面导航
    st.title("Page Navigation | 页面导航")
    selected_page = st.radio(
        label="Go to | 前往",
        options=[
            "Introduction | 介绍",
            "Overview | 概览",
            "Deep Dives | 深度分析",
            "Conclusions | 结论"
        ],
        index=0  # 默认显示介绍页
    )
    
    st.divider()
    
    # 3. 版权信息
    st.caption("""
    Developed by | 开发：Zhu Enping 
    Data Source | 数据来源：2023-2024 Public Health Surveillance Records  
    Contact | 联系：1305927014@qq.com
    """)

# 核心逻辑：加载并过滤数据（传递过滤器参数）
try:
    # 调用数据处理函数，传入年份和区域过滤器
    feature_df, analysis_tables = get_processed_data(
        year_filter=selected_years,
        region_filter=selected_regions
    )
    
    # 数据校验：确保analysis_tables结构完整
    required_keys = ['kpi', 'timeseries']
    for key in required_keys:
        if key not in analysis_tables:
            analysis_tables[key] = pd.DataFrame()  # 兜底空DataFrame
    
    # 显示加载成功提示
    st.success(f"✅ Data loaded successfully! Filtered by: Years {selected_years}, Regions {selected_regions} | 数据加载成功！过滤条件：年份{selected_years}，区域{selected_regions}")
    
    # 调试辅助：查看数据结构（可选展开）
    with st.expander("🔍 查看数据结构（调试用）", expanded=False):
        st.subheader("Analysis Tables Keys | 分析表格关键字段")
        st.write(list(analysis_tables.keys()))
        st.subheader("KPI Data Preview | KPI数据预览")
        st.dataframe(analysis_tables['kpi'].head(), use_container_width=True)
        st.subheader("Feature Data Preview | 特征数据预览")
        st.dataframe(feature_df.head(), use_container_width=True)
        
except Exception as e:
    # 显示错误提示并终止运行
    st.error(f"❌ Data processing failed: {str(e)} | 数据处理失败：{str(e)}")
    st.stop()

# 页面渲染逻辑（根据侧边栏选择显示对应页面）
if selected_page == "Introduction | 介绍":
    intro.render_intro()
elif selected_page == "Overview | 概览":
    # 传递analysis_tables和feature_df（对应overview的raw_clean_df参数）
    overview.render_overview(analysis_tables, feature_df)
elif selected_page == "Deep Dives | 深度分析":
    deep_dives.render_deep_dives(analysis_tables)
elif selected_page == "Conclusions | 结论":
    conclusions.render_conclusions(analysis_tables)