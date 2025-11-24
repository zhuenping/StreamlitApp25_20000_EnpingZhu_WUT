import pandas as pd

def prepare_analysis_data(raw_data):
    """准备分析所需的数据表格（强制生成所有KPI指标，避免缺失）"""
    # 确保原始数据为空时也能生成KPI（默认值0）
    total_cases = len(raw_data) if not raw_data.empty else 0
    success_cases = len(raw_data[raw_data['status'] == 'Success']) if not raw_data.empty else 0
    avg_value = raw_data['value'].mean() if not raw_data.empty and 'value' in raw_data.columns else 0.0
    unique_categories = raw_data['category'].nunique() if not raw_data.empty and 'category' in raw_data.columns else 0
    failed_cases = len(raw_data[raw_data['status'] == 'Failed']) if not raw_data.empty else 0
    pending_cases = len(raw_data[raw_data['status'] == 'Pending']) if not raw_data.empty else 0
    
    # 强制生成所有需要的KPI指标（确保不会缺失）
    kpi_data = [
        {'metric': 'Total Cases', 'value': total_cases},
        {'metric': 'Success Cases', 'value': success_cases},
        {'metric': 'Average Value', 'value': avg_value},
        {'metric': 'Unique Categories', 'value': unique_categories},
        {'metric': 'Failed Cases', 'value': failed_cases},
        {'metric': 'Pending Cases', 'value': pending_cases}
    ]
    kpi_df = pd.DataFrame(kpi_data)
    
    # 生成样本数据（空数据兜底）
    if not raw_data.empty and all(col in raw_data.columns for col in ['case_id', 'date', 'category', 'value', 'status']):
        sample_data = raw_data[['case_id', 'date', 'category', 'value', 'status']].copy()
        sample_data['date'] = sample_data['date'].dt.strftime('%Y-%m-%d %H:%M') if 'date' in sample_data.columns else ''
    else:
        sample_data = pd.DataFrame(columns=['case_id', 'date', 'category', 'value', 'status'])
    
    # 生成详细统计数据（空数据兜底）
    if not raw_data.empty and all(col in raw_data.columns for col in ['category', 'case_id', 'value']):
        category_stats = raw_data.groupby('category').agg({
            'case_id': 'count',
            'value': ['mean', 'max', 'min']
        }).round(2)
        category_stats.columns = ['案例数', '平均值', '最大值', '最小值']
        category_stats.reset_index(inplace=True)
    else:
        category_stats = pd.DataFrame(columns=['category', '案例数', '平均值', '最大值', '最小值'])
    
    return {
        'kpi': kpi_df,
        'sample_data': sample_data,
        'category_stats': category_stats
    }

def generate_kpi_df(raw_data):
    """单独生成KPI数据框（备用函数，同样强制生成指标）"""
    total_cases = len(raw_data) if not raw_data.empty else 0
    success_cases = len(raw_data[raw_data['status'] == 'Success']) if not raw_data.empty else 0
    avg_value = raw_data['value'].mean() if not raw_data.empty and 'value' in raw_data.columns else 0.0
    unique_categories = raw_data['category'].nunique() if not raw_data.empty and 'category' in raw_data.columns else 0
    
    return pd.DataFrame([
        {'metric': 'Total Cases', 'value': total_cases},
        {'metric': 'Success Cases', 'value': success_cases},
        {'metric': 'Average Value', 'value': avg_value},
        {'metric': 'Unique Categories', 'value': unique_categories}
    ])