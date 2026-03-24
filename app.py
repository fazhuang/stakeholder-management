import streamlit as st
import pandas as pd

# 配置页面
st.set_page_config(page_title="干系人管理分析表", layout="wide")

st.title("👥 干系人参与度评估矩阵 (Stakeholder Engagement)")
st.caption("PMP/软考项目管理 - 核心工具")

# 初始化缓存数据，代替原本 Flask 的内存列表
if 'stakeholders' not in st.session_state:
    st.session_state.stakeholders = []

ENGAGEMENT_LEVELS = ['不觉察', '抵触', '中立', '支持', '领导']

# 左侧表单 - 添加干系人
with st.sidebar:
    st.header("➕ 添加新干系人")
    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("姓名")
        role = st.text_input("角色")
        power = st.selectbox("权力 (Power)", ["高", "低"], index=0)
        interest = st.selectbox("利益 (Interest)", ["高", "低"], index=0)
        current_eng = st.selectbox("当前期望 (Current)", ENGAGEMENT_LEVELS, index=0)
        desired_eng = st.selectbox("期望目标 (Desired)", ENGAGEMENT_LEVELS, index=3)
        
        submitted = st.form_submit_button("添加干系人")
        if submitted and name and role:
            # 找到最大的 ID
            next_id = 1 if not st.session_state.stakeholders else max(s['id'] for s in st.session_state.stakeholders) + 1
            st.session_state.stakeholders.append({
                'id': next_id,
                'name': name,
                'role': role,
                'power': power,
                'interest': interest,
                'current_eng': current_eng,
                'desired_eng': desired_eng
            })
            st.success(f"成功添加 {name}!")
            st.rerun()

# 核心数据展示区
st.subheader("📋 当前干系人名册与状态")

if st.session_state.stakeholders:
    # 转换为 DataFrame 方便表格展示
    df = pd.DataFrame(st.session_state.stakeholders)
    # 针对前端优化的表格展示（隐藏主键ID）
    st.dataframe(
        df[['name', 'role', 'power', 'interest', 'current_eng', 'desired_eng']].rename(columns={
            'name': '姓名', 'role': '角色', 'power': '权力', 
            'interest': '利益', 'current_eng': '当前状态', 'desired_eng': '期望状态'
        }), 
        use_container_width=True
    )
    
    st.divider()
    
    # 删除功能
    st.subheader("🗑️ 数据维护")
    col1, col2 = st.columns([2, 8])
    with col1:
        del_id = st.selectbox("选择要删除的人员", 
                              [s['id'] for s in st.session_state.stakeholders], 
                              format_func=lambda x: next(s['name'] for s in st.session_state.stakeholders if s['id'] == x))
        if st.button("删除该记录", type="primary"):
            st.session_state.stakeholders = [s for s in st.session_state.stakeholders if s['id'] != del_id]
            st.success("删除成功！")
            st.rerun()
else:
    st.info("目前暂无干系人数据。请在左侧“添加新干系人”部分输入数据。")
