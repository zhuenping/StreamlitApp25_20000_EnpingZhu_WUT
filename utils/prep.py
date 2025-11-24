"""
Complete Data Processing Pipeline | 完整数据处理流程
- Data Cleaning | 数据清洗
- Feature Engineering | 特征工程
- Analysis Table Generation | 分析表生成
- Filter Integration with Default Values | 含默认值的过滤器集成（解决参数缺失问题）
"""
import pandas as pd
import numpy as np
from typing import Dict, Tuple
from utils.io import load_raw_dataset

def clean_raw_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    """数据清洗：处理缺失值、异常值、格式标准化"""
    clean_df = raw_df.copy()
    print("=== Starting Data Cleaning | 开始数据清洗 ===")
    
    # 1. 字段名标准化（小写+下划线，避免大小写冲突）
    clean_df.columns = [col.lower().replace(" ", "_") for col in clean_df.columns]
    print("✅ Field name standardized | 字段名标准化完成")
    
    # 2. 日期字段处理（统一格式，过滤无效日期）
    clean_df["date_of_onset"] = pd.to_datetime(
        clean_df["date_of_onset"],
        errors="coerce",  # 无效日期转为NaT
        format="mixed"    # 自动识别日期格式
    )
    invalid_date_count = clean_df["date_of_onset"].isnull().sum()
    if invalid_date_count > 0:
        clean_df = clean_df.dropna(subset=["date_of_onset"])
        print(f"✅ Filtered {invalid_date_count} invalid dates | 过滤{invalid_date_count}行无效日期，剩余{len(clean_df)}行")
    
    # 3. 分类字段处理（去重、填充缺失值）
    categorical_fields = ["location", "ses", "immunity_level"]
    for field in categorical_fields:
        # 统一格式：首字母大写，去除前后空格
        clean_df[field] = clean_df[field].str.title().str.strip()
        # 填充缺失值：用众数（无众数时用"Unknown"）
        missing_count = clean_df[field].isnull().sum()
        if missing_count > 0:
            mode_value = clean_df[field].mode()[0] if not clean_df[field].mode().empty else "Unknown"
            clean_df[field] = clean_df[field].fillna(mode_value)
            print(f"✅ Filled {missing_count} missing values for '{field}' with mode '{mode_value}' | 填充'{field}'字段{missing_count}个缺失值（众数：{mode_value}）")
    
    # 4. 二进制字段处理（确保0/1编码，填充缺失值）
    binary_fields = ["chronic_conditions", "vaccination_status"]
    for field in binary_fields:
        # 转为数值类型，无效值转为NaN
        clean_df[field] = pd.to_numeric(clean_df[field], errors="coerce")
        # 填充缺失值为0（默认"未患病"/"未接种"）
        clean_df[field] = clean_df[field].fillna(0).astype(int)
        # 过滤非0/1值
        invalid_val_count = len(clean_df[~clean_df[field].isin([0, 1])])
        if invalid_val_count > 0:
            clean_df = clean_df[clean_df[field].isin([0, 1])]
            print(f"✅ Filtered {invalid_val_count} invalid values for '{field}' (only 0/1 allowed) | 过滤'{field}'字段{invalid_val_count}个非0/1值")
    
    # 5. 数值字段处理（异常值过滤+缺失值填充）
    numeric_fields = ["daily_new_cases", "hospital_capacity", "hospitalization_requirement", "age"]
    # 业务默认值（全缺失时使用，避免中位数为NaN）
    default_values = {
        "daily_new_cases": 0,
        "hospital_capacity": 100,  # 医院默认100张床
        "hospitalization_requirement": 10,
        "age": 35  # 成年人默认年龄
    }
    
    for field in numeric_fields:
        # 转为数值类型
        clean_df[field] = pd.to_numeric(clean_df[field], errors="coerce")
        # 计算中位数（全缺失时用默认值）
        median_value = clean_df[field].median()
        if pd.isna(median_value):
            median_value = default_values[field]
            print(f"⚠️ All values missing for '{field}', using default {median_value} | '{field}'全为缺失值，使用默认值{median_value}")
        
        # 填充缺失值
        missing_count = clean_df[field].isnull().sum()
        if missing_count > 0:
            clean_df[field] = clean_df[field].fillna(median_value)
            print(f"✅ Filled {missing_count} missing values for '{field}' with {median_value:.1f} | 填充'{field}'字段{missing_count}个缺失值（值：{median_value:.1f}）")
        
        # 过滤异常值
        if field == "daily_new_cases":
            # 病例数不能为负
            invalid_count = len(clean_df[clean_df[field] < 0])
            clean_df = clean_df[clean_df[field] >= 0]
        elif field == "age":
            # 年龄范围：0-120岁
            invalid_count = len(clean_df[(clean_df[field] < 0) | (clean_df[field] > 120)])
            clean_df = clean_df[(clean_df[field] >= 0) & (clean_df[field] <= 120)]
        elif "capacity" in field or "requirement" in field:
            # 容量/需求不能≤0
            invalid_count = len(clean_df[clean_df[field] <= 0])
            clean_df = clean_df[clean_df[field] > 0]
        
        if invalid_count > 0:
            print(f"✅ Filtered {invalid_count} outliers for '{field}' | 过滤'{field}'字段{invalid_count}个异常值")
    
    # 最终校验：清洗后数据不能为空
    if len(clean_df) == 0:
        raise ValueError("❌ No valid data left after cleaning! Check raw data quality | 数据清洗后无有效数据！请检查原始数据质量")
    
    print(f"=== Data Cleaning Completed | 数据清洗完成 ===")
    print(f"Cleaned Data: {len(clean_df)} rows × {len(clean_df.columns)} columns | 清洗后数据：{len(clean_df)}行 × {len(clean_df.columns)}列")
    return clean_df

# 在create_business_features函数中修改resource_load计算
def create_business_features(clean_df: pd.DataFrame) -> pd.DataFrame:
    """特征工程：生成业务所需特征（支撑可视化分析）"""
    feature_df = clean_df.copy()
    print("=== Starting Feature Engineering | 开始特征工程 ===")
    
    # 1. 时间特征（年/月/季节，支撑时间序列分析）
    feature_df["year"] = feature_df["date_of_onset"].dt.year.astype(int)
    feature_df["month"] = feature_df["date_of_onset"].dt.month.astype(int)
    # 季节映射（北半球：12-2月冬季，3-5月春季，6-8月夏季，9-11月秋季）
    season_mapping = {1: "Winter", 2: "Winter", 3: "Spring", 4: "Spring", 5: "Spring",
                      6: "Summer", 7: "Summer", 8: "Summer", 9: "Autumn", 10: "Autumn",
                      11: "Autumn", 12: "Winter"}
    feature_df["season"] = feature_df["month"].map(season_mapping)
    print("✅ Time features generated: year, month, season | 生成时间特征：年份、月份、季节")
    
    # 2. 年龄组特征（支撑疫苗效果的年龄差异分析，确保66+岁分组）
    feature_df["age_group"] = pd.cut(
        feature_df["age"],
        bins=[0, 18, 65, 120],  # 明确划分：儿童(0-18)、成人(19-65)、老人(66+)
        labels=["Child (0-18)", "Adult (19-65)", "Elderly (66+)"],
        include_lowest=True  # 包含左边界（0岁）
    )
    print("✅ Age group feature generated: Child (0-18), Adult (19-65), Elderly (66+) | 生成年龄组特征：儿童、成人、老人")
    
    # 3. 疫苗覆盖率特征（区域-年度维度，支撑疫苗效果分析）
    vaccine_coverage = feature_df.groupby(["year", "location"])["vaccination_status"].apply(
        lambda x: (x == 1).sum() / len(x) if len(x) > 0 else 0  # 接种率=接种人数/总人数
    ).reset_index(name="vaccine_coverage")
    # 合并回主表
    feature_df = pd.merge(
        feature_df,
        vaccine_coverage,
        on=["year", "location"],
        how="left"
    )
    # 保留3位小数，填充缺失值为0
    feature_df["vaccine_coverage"] = np.round(feature_df["vaccine_coverage"].fillna(0), 3)
    print("✅ Vaccine coverage feature generated | 生成疫苗覆盖率特征")
    
    # 4. 医疗资源负荷特征（支撑资源紧张度分析）
    # 优化：优先使用数据中的实际值，添加安全检查，确保计算准确性
    if "resource_utilization" in feature_df.columns and not feature_df["resource_utilization"].isnull().all():
        # 如果数据中已有资源利用率字段且不全为空，直接使用并标准化到合理范围
        feature_df["resource_load"] = np.clip(feature_df["resource_utilization"] / 100, 0, 5)  # 确保范围在0-5之间
        print("✅ Resource load feature generated from existing resource_utilization | 从现有字段生成资源负荷特征")
    else:
        # 否则使用住院需求/医院容量的计算
        # 添加安全检查，避免除以0
        feature_df["resource_load"] = np.where(
            feature_df["hospital_capacity"] > 0,  # 安全检查
            feature_df["hospitalization_requirement"] / feature_df["hospital_capacity"],
            0  # 默认值
        )
    # 保留3位小数，限制最大值为5（避免极端值影响）
    feature_df["resource_load"] = np.round(feature_df["resource_load"], 3).clip(upper=5)
    print(f"✅ Resource load feature generated | 生成资源负荷特征：平均值={feature_df['resource_load'].mean():.3f}，范围={feature_df['resource_load'].min():.3f}-{feature_df['resource_load'].max():.3f}")
    
    # 5. 传播率特征（季节维度，支撑传播趋势分析）
    season_transmission_mapping = {"Winter": 1.2, "Spring": 0.9, "Summer": 0.6, "Autumn": 0.8}
    feature_df["transmission_rate"] = feature_df["season"].map(season_transmission_mapping)
    # 保留2位小数
    feature_df["transmission_rate"] = np.round(feature_df["transmission_rate"], 2)
    print("✅ Transmission rate feature generated | 生成季节传播率特征")
    
    print("=== Feature Engineering Completed | 特征工程完成 ===")
    print(f"Feature Data: {len(feature_df)} rows × {len(feature_df.columns)} columns | 特征后数据：{len(feature_df)}行 × {len(feature_df.columns)}列")
    return feature_df

# 在generate_analysis_tables函数中修改region_ses_table生成
def generate_analysis_tables(feature_df: pd.DataFrame, year_filter: list, region_filter: list) -> Dict[str, pd.DataFrame]:
    """生成分析表（集成过滤器，应用年份和区域筛选）"""
    analysis_tables = {}
    print("=== Starting Analysis Table Generation | 开始生成分析表 ===")
    
    # 应用过滤器（年份+区域）
    filtered_df = feature_df.copy()
    if year_filter:
        filtered_df = filtered_df[filtered_df["year"].isin(year_filter)]
        print(f"🔍 Filtered by years: {year_filter} | 按年份过滤：{year_filter}")
    if region_filter:
        filtered_df = filtered_df[filtered_df["location"].isin(region_filter)]
        print(f"🔍 Filtered by regions: {region_filter} | 按区域过滤：{region_filter}")
    
    # 校验过滤后数据是否为空
    if len(filtered_df) == 0:
        raise ValueError("❌ No data left after filtering! Adjust filter criteria | 过滤后无数据！请调整过滤条件")
    
    # 1. 时间序列表（年-月-区域维度，支撑概览页趋势图）
    # 修改generate_analysis_tables函数中的timeseries_table生成部分
    timeseries_table = filtered_df.groupby(["year", "month", "location"]).agg({
    "daily_new_cases": "sum",          # 月新增病例总数
    "transmission_rate": "mean",       # 月平均传播率
    "vaccine_coverage": "mean",         # 月平均疫苗覆盖率
    "resource_load": "mean"            # 月平均资源负荷
    }).reset_index().sort_values(["year", "month", "location"])
    
    # 添加缺失的date列
    timeseries_table["date"] = pd.to_datetime(
    timeseries_table["year"].astype(str) + '-' + timeseries_table["month"].astype(str) + '-01'
    )
    analysis_tables["timeseries"] = timeseries_table
    print(f"✅ Time series table generated: {len(timeseries_table)} rows | 生成时间序列表：{len(timeseries_table)}行")
    
    # 2. 区域-SES表（区域-SES-季节维度，支撑深度分析页柱状图）
    region_ses_table = filtered_df.groupby(["location", "ses", "season"]).agg({
        "daily_new_cases": "sum",          # 季节病例总数
        "vaccine_coverage": "mean",         # 季节平均疫苗覆盖率
        "resource_load": "mean",            # 季节平均资源负荷
        "age": "median"                    # 季节年龄中位数
    }).reset_index()
    
    # 添加样本量列，用于参考
    sample_size = filtered_df.groupby(["location", "ses", "season"]).size().reset_index(name="sample_size")
    region_ses_table = pd.merge(region_ses_table, sample_size, on=["location", "ses", "season"])
    
    analysis_tables["region_ses"] = region_ses_table
    print(f"✅ Region-SES table generated: {len(region_ses_table)} rows | 生成区域-SES表：{len(region_ses_table)}行")
    
    # 3. 疫苗效果表（核心：接种状态-免疫水平-年龄组维度，确保66+岁显示）
    vaccine_effect_df = filtered_df.dropna(subset=["vaccination_status", "immunity_level", "age_group"])
    vaccine_effect_table = vaccine_effect_df.groupby(
        ["vaccination_status", "immunity_level", "age_group"],
        observed=True  # 解决分类字段聚合警告
    ).agg({
        "daily_new_cases": "mean",         # 平均每日新增病例（Y轴）
        "transmission_rate": "mean"        # 平均传播率（点大小）
    }).reset_index()
    # 接种状态映射为可读性标签（0→未接种，1→已接种）
    vaccine_effect_table["vaccination_status"] = vaccine_effect_table["vaccination_status"].map({
        0: "Unvaccinated",
        1: "Vaccinated"
    })
    analysis_tables["vaccine_effect"] = vaccine_effect_table
    print(f"✅ Vaccine effect table generated: {len(vaccine_effect_table)} rows | 生成疫苗效果表：{len(vaccine_effect_table)}行")
    
    # 4. KPI表（全局核心指标，支撑概览页指标卡） - 移除高危人群统计
    total_cases = filtered_df["daily_new_cases"].sum()
    avg_vaccine_coverage = np.round(filtered_df["vaccine_coverage"].fillna(0).mean(), 3)
    avg_resource_load = np.round(filtered_df["resource_load"].fillna(0).mean(), 3)
    # 高峰季节病例数（单季节最大病例数）
    peak_season_cases = filtered_df.groupby("season")["daily_new_cases"].sum().max() if not filtered_df.empty else 0
    
    kpi_table = pd.DataFrame({
        "metric": [
            "Total Cases | 总病例数",
            "Average Vaccine Coverage | 平均疫苗覆盖率",
            "Average Resource Load | 平均资源负荷",
            "Peak Season Cases | 高峰季节病例数"
        ],
        "value": [total_cases, avg_vaccine_coverage, avg_resource_load, peak_season_cases],
        "unit": [
            "Cases | 例",
            "Ratio | 比例",
            "Ratio | 比例",
            "Cases | 例"
        ],
        "description": [
            "Total new cases in filtered data | 过滤后数据中的总新增病例数",
            "Average vaccination rate across regions/years | 所有区域/年份的平均疫苗接种率",
            "Average ratio of hospitalization requirement to capacity | 住院需求与医院容量的平均比例",
            "Maximum number of cases in any season | 任意季节的最大病例数"
        ]
    })
    analysis_tables["kpi"] = kpi_table
    print("✅ KPI table generated | 生成KPI表")
    
    # 5. 原始特征表（支撑数据质量检查）
    analysis_tables["raw_feature"] = filtered_df
    print(f"✅ Raw feature table retained: {len(filtered_df)} rows | 保留原始特征表：{len(filtered_df)}行")
    
    print("=== Analysis Table Generation Completed | 分析表生成完成 ===")
    print(f"Total tables generated: {len(analysis_tables)} | 共生成{len(analysis_tables)}个分析表")
    return analysis_tables

# 在数据处理流程中，确保为时间序列数据创建必要的时间列
def get_processed_data(year_filter=None, region_filter=None):
    try:
        # 步骤1：加载原始数据
        raw_data = load_raw_dataset()
        # 步骤2：数据清洗
        cleaned_data = clean_raw_data(raw_data)
        # 步骤3：特征工程
        feature_data = create_business_features(cleaned_data)
        
        # 步骤4：处理默认过滤参数（未传入则使用全量数据）
        if year_filter is None:
            year_filter = feature_data["year"].unique().tolist()
            print(f"ℹ️ No year filter provided, using all years: {year_filter} | 未提供年份过滤，使用所有年份：{year_filter}")
        if region_filter is None:
            region_filter = feature_data["location"].unique().tolist()
            print(f"ℹ️ No region filter provided, using all regions: {region_filter} | 未提供区域过滤，使用所有区域：{region_filter}")
        
        # 步骤5：生成分析表（应用过滤）
        analysis_tables = generate_analysis_tables(feature_data, year_filter, region_filter)
        
        return feature_data, analysis_tables
    except Exception as e:
        # 捕获异常并重新抛出（附加上下文）
        raise RuntimeError(f"End-to-end data processing failed: {str(e)} | 端到端数据处理失败：{str(e)}") from e