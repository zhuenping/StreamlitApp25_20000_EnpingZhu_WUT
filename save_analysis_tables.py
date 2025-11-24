"""
Pre-generate and Save Analysis Tables | 预生成并保存分析表
- Automatically load raw data, process it, and save analysis tables to local files
  自动加载原始数据、处理数据，并将分析表保存到本地文件
- Support overwriting existing files and path customization
  支持覆盖现有文件和路径自定义
"""
import os
import pickle
from typing import Optional
from utils.prep import get_processed_data  # 调用数据处理函数（已支持默认参数）

def save_analysis_tables(
    output_dir: str = "data",
    output_filename: str = "preprocessed_analysis_tables.pkl",
    overwrite: bool = True,
    year_filter: Optional[list] = None,
    region_filter: Optional[list] = None
) -> None:
    """
    预生成分析表并保存到本地
    
    Args:
        output_dir: 输出目录（默认：项目根目录下的data文件夹）
        output_filename: 输出文件名（默认：preprocessed_analysis_tables.pkl）
        overwrite: 是否覆盖现有文件（默认：True）
        year_filter: 年份过滤列表（默认：None，使用全量年份）
        region_filter: 区域过滤列表（默认：None，使用全量区域）
    """
    # 打印任务开始信息
    print("=" * 60)
    print("📊 Starting Pre-generation of Public Health Analysis Tables | 开始预生成公共卫生分析表")
    print("=" * 60)
    
    # 1. 校验输出目录（不存在则创建）
    project_root = os.getcwd()
    output_full_path = os.path.join(project_root, output_dir, output_filename)
    output_dir_path = os.path.join(project_root, output_dir)
    
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path, exist_ok=True)
        print(f"📁 Created output directory: {output_dir_path} | 创建输出目录：{output_dir_path}")
    else:
        print(f"📁 Output directory already exists: {output_dir_path} | 输出目录已存在：{output_dir_path}")
    
    # 2. 校验文件是否已存在（若不允许覆盖则退出）
    if os.path.exists(output_full_path) and not overwrite:
        raise FileExistsError(
            f"❌ File already exists: {output_full_path} | 文件已存在：{output_full_path}\n"
            f"Set 'overwrite=True' to replace it | 请设置'overwrite=True'以覆盖文件"
        )
    
    # 3. 调用数据处理函数（无需手动传参，使用默认值：全量数据）
    print("\n🔄 Starting data processing (using default filters: all years + all regions) | 开始数据处理（使用默认过滤：全量年份+全量区域）")
    try:
        # 调用get_processed_data，未传参则自动使用全量年份和区域
        _, analysis_tables = get_processed_data(
            year_filter=year_filter,
            region_filter=region_filter
        )
        print("✅ Data processing completed successfully | 数据处理成功完成")
    except Exception as e:
        raise RuntimeError(f"❌ Data processing failed: {str(e)} | 数据处理失败：{str(e)}") from e
    
    # 4. 保存分析表到本地（使用pickle格式）
    print(f"\n💾 Saving analysis tables to: {output_full_path} | 正在保存分析表到：{output_full_path}")
    try:
        with open(output_full_path, "wb") as f:
            pickle.dump(analysis_tables, f, protocol=pickle.HIGHEST_PROTOCOL)
        print(f"✅ Analysis tables saved successfully! | 分析表保存成功！")
    except Exception as e:
        raise RuntimeError(f"❌ Failed to save analysis tables: {str(e)} | 保存分析表失败：{str(e)}") from e
    
    # 5. 打印保存完成的详细信息
    print("\n" + "=" * 60)
    print("📋 Saved Analysis Tables Summary | 已保存分析表汇总")
    print("=" * 60)
    for table_name, table_data in analysis_tables.items():
        print(f"• {table_name}: {len(table_data)} rows × {len(table_data.columns)} columns | {table_name}表：{len(table_data)}行 × {len(table_data.columns)}列")
    print("=" * 60)
    print("🎉 Pre-generation of analysis tables completed! | 分析表预生成任务完成！")
    print("=" * 60)

if __name__ == "__main__":
    """脚本入口：直接运行时使用默认配置"""
    try:
        save_analysis_tables(
            output_dir="data",          # 输出目录：data文件夹
            output_filename="preprocessed_analysis_tables.pkl",  # 输出文件名
            overwrite=True,            # 允许覆盖现有文件
            # 此处未传year_filter和region_filter，自动使用全量数据
        )
    except Exception as e:
        print(f"\n❌ Task failed: {str(e)} | 任务失败：{str(e)}")
        exit(1)  # 非0退出码标识失败