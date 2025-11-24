"""
Complete Data I/O Utilities | 完整数据输入输出工具
- Raw Data Loading | 原始数据加载
- File Encoding Detection | 文件编码检测
- Data Caveats & Documentation | 数据说明文档
"""
import pandas as pd
import os
import chardet
from typing import Dict, Optional  # 新增：导入Dict类型

# 核心字段定义（确保原始数据包含这些字段）
REQUIRED_FIELDS = [
    "Date_of_Onset",    # 发病日期
    "Location",         # 区域
    "SES",              # 社会经济水平
    "Chronic_Conditions",# 慢性病状态
    "Vaccination_Status",# 接种状态
    "Daily_New_Cases",  # 每日新增病例
    "Hospital_Capacity",# 医院容量
    "Hospitalization_Requirement",# 住院需求
    "Immunity_Level",   # 免疫水平
    "Age"               # 年龄
]

def detect_file_encoding(file_path: str) -> str:
    """检测文件编码（解决中文/特殊字符乱码问题）"""
    try:
        with open(file_path, "rb") as file:
            # 读取前10000字节用于编码检测
            raw_data = file.read(10000)
            # 检测编码
            encoding_result = chardet.detect(raw_data)
        # 返回编码（默认utf-8）
        detected_encoding = encoding_result["encoding"] or "utf-8"
        print(f"🔍 Detected file encoding: {detected_encoding} | 检测到文件编码：{detected_encoding}")
        return detected_encoding
    except Exception as e:
        raise RuntimeError(f"Failed to detect file encoding: {str(e)} | 检测文件编码失败：{str(e)}") from e

def load_raw_dataset(data_dir: str = "data", file_name: str = "public_health_surveillance_dataset.csv") -> pd.DataFrame:
    """加载原始数据集（校验路径、字段、数据质量）"""
    # 1. 构建数据路径
    project_root = os.getcwd()
    data_file_path = os.path.join(project_root, data_dir, file_name)
    
    # 2. 校验文件是否存在
    if not os.path.exists(data_file_path):
        raise FileNotFoundError(
            f"❌ Raw dataset not found! Expected path: {data_file_path} | 原始数据集未找到！预期路径：{data_file_path}\n"
            f"Please place the CSV file in the '{data_dir}' folder at the project root. | 请将CSV文件放入项目根目录的'{data_dir}'文件夹。"
        )
    
    # 3. 检测文件编码并读取数据
    try:
        file_encoding = detect_file_encoding(data_file_path)
        # 读取CSV文件（解析日期字段）
        raw_df = pd.read_csv(
            data_file_path,
            encoding=file_encoding,
            parse_dates=["Date_of_Onset"],  # 自动解析日期
            low_memory=False  # 处理大文件时避免类型推断错误
        )
    except Exception as e:
        raise RuntimeError(
            f"❌ Failed to load raw dataset: {str(e)} | 加载原始数据集失败：{str(e)}\n"
            f"Suggestions | 建议：\n"
            f"1. Check if the CSV format is valid (no extra commas/newlines). | 检查CSV格式是否有效（无多余逗号/换行）。\n"
            f"2. Verify the file encoding (try 'utf-8' or 'gbk'). | 验证文件编码（尝试'utf-8'或'gbk'）。"
        ) from e
    
    # 4. 校验核心字段是否齐全
    missing_fields = [field for field in REQUIRED_FIELDS if field not in raw_df.columns]
    if missing_fields:
        raise ValueError(
            f"❌ Missing required fields in raw dataset: {missing_fields} | 原始数据集缺失核心字段：{missing_fields}\n"
            f"Required fields must include: {REQUIRED_FIELDS} | 核心字段必须包含：{REQUIRED_FIELDS}"
        )
    
    # 5. 校验数据量（避免过小数据集）
    min_data_rows = 500
    if len(raw_df) < min_data_rows:
        raise ValueError(
            f"❌ Raw dataset is too small (only {len(raw_df)} rows). Minimum required: {min_data_rows} rows. | 原始数据集过小（仅{len(raw_df)}行）。最低要求：{min_data_rows}行\n"
            f"Please use a dataset with sufficient sample size for reliable analysis. | 请使用样本量足够的数据集以确保分析可靠性。"
        )
    
    # 6. 打印加载成功信息
    print(f"✅ Raw dataset loaded successfully! | 原始数据集加载成功！")
    print(f"Dataset Size: {len(raw_df)} rows × {len(raw_df.columns)} columns | 数据集大小：{len(raw_df)}行 × {len(raw_df.columns)}列")
    print(f"Date Range: {raw_df['Date_of_Onset'].min().date()} ~ {raw_df['Date_of_Onset'].max().date()} | 日期范围：{raw_df['Date_of_Onset'].min().date()} ~ {raw_df['Date_of_Onset'].max().date()}")
    
    return raw_df

def get_data_caveats() -> str:
    """获取数据集说明文档（中英文双注释）"""
    return """
    ### Dataset Caveats & Documentation | 数据集说明与文档
    #### 1. Data Source | 数据来源
    - Public health surveillance records from 2023 to 2024, covering Urban, Suburban, and Rural regions.
      2023-2024年公共卫生监测记录，覆盖城市、郊区、农村三类区域。
    - Collected from multiple regional health departments (de-identified to protect privacy).
      数据来自多个区域卫生部门（已去标识化，保护隐私）。

    #### 2. Key Field Definitions | 核心字段定义
    | Field Name | 字段名称 | Definition | 定义 |
    |------------|----------|------------|------|
    | Date_of_Onset | 发病日期 | Date when the patient was diagnosed (core time dimension). | 患者确诊日期（核心时间维度）。 |
    | Location | 区域 | Region type (Urban/Suburban/Rural, case-insensitive). | 区域类型（城市/郊区/农村，不区分大小写）。 |
    | SES | 社会经济水平 | Socio-Economic Status (High/Medium/Low, based on household income). | 社会经济水平（高/中/低，基于家庭收入）。 |
    | Chronic_Conditions | 慢性病状态 | Whether the patient has chronic diseases (1=Yes, 0=No). | 患者是否有慢性病（1=是，0=否）。 |
    | Vaccination_Status | 接种状态 | Whether the patient is vaccinated (1=Vaccinated, 0=Unvaccinated). | 患者是否接种疫苗（1=已接种，0=未接种）。 |
    | Daily_New_Cases | 每日新增病例 | Number of new confirmed cases per day (non-negative). | 每日新增确诊病例数（非负）。 |
    | Hospital_Capacity | 医院容量 | Total hospital beds in the region (≥10 beds). | 区域内医院总床位数（≥10张）。 |
    | Hospitalization_Requirement | 住院需求 | Number of patients requiring hospitalization per day (non-negative). | 每日需要住院的患者数（非负）。 |
    | Immunity_Level | 免疫水平 | Individual immunity level (High/Medium/Low, based on medical tests). | 个人免疫水平（高/中/低，基于医学检测）。 |
    | Age | 年龄 | Patient's age (0-120 years). | 患者年龄（0-120岁）。 |

    #### 3. Data Cleaning Rules | 数据清洗规则
    - **Invalid Dates | 无效日期**: Rows with unparseable dates (e.g., "2023/13/01") are filtered out. | 无法解析的日期（如“2023/13/01”）已过滤。
    - **Outliers | 异常值**: Rows with age >120, negative cases, or zero hospital capacity are removed. | 年龄>120、负病例数、零床位的行已删除。
    - **Missing Values | 缺失值**: 
      - Categorical fields (e.g., Location) filled with mode. | 分类字段（如区域）用众数填充。
      - Numeric fields (e.g., Age) filled with median (or default values if all missing). | 数值字段（如年龄）用中位数填充（全缺失时用默认值）。

    #### 4. Ethics & Limitations | 伦理与局限性
    - **Ethics | 伦理**: All data is aggregated and de-identified; no personal information is included. | 所有数据已聚合和去标识化，不含个人信息。
    - **Limitations | 局限性**: 
      - Data only covers 2023-2024 (no long-term trend analysis). | 数据仅覆盖2023-2024年（无长期趋势分析）。
      - No county-level granularity (only regional-level data). | 无县级粒度（仅区域级数据）。
    """

def save_processed_data(processed_data: Dict[str, pd.DataFrame], output_dir: str = "data", file_name: str = "processed_analysis_tables.pkl") -> None:
    """保存处理后的分析表（可选，用于离线复用）"""
    import pickle  # 延迟导入，避免未使用时加载
    
    # 构建输出路径
    project_root = os.getcwd()
    output_file_path = os.path.join(project_root, output_dir, file_name)
    
    # 创建输出目录（不存在则创建）
    if not os.path.exists(os.path.join(project_root, output_dir)):
        os.makedirs(os.path.join(project_root, output_dir), exist_ok=True)
        print(f"📁 Created output directory: {os.path.join(project_root, output_dir)} | 创建输出目录：{os.path.join(project_root, output_dir)}")
    
    # 保存数据
    try:
        with open(output_file_path, "wb") as output_file:
            pickle.dump(processed_data, output_file, protocol=pickle.HIGHEST_PROTOCOL)
        print(f"✅ Processed data saved to: {output_file_path} | 处理后数据已保存至：{output_file_path}")
    except Exception as e:
        raise RuntimeError(f"❌ Failed to save processed data: {str(e)} | 保存处理后数据失败：{str(e)}") from e