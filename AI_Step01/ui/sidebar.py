import streamlit as st
from utils.session_manager import save_session, load_session, delete_session, load_sessions, generate_session_time


def render_sidebar():
    with st.sidebar:
        st.subheader("控制面板")

        if st.button("新建会话", width="stretch", icon="✏️"):
            # 如果当前会话有消息，先保存会话
            if st.session_state.messages:
                save_session()
            # 重置会话状态
            st.session_state.messages = []
            st.session_state.current_session = generate_session_time()
            st.session_state.model = "deepseek-v4-pro"
            st.session_state.max_tokens = 4096
            st.session_state.temperature = 0.7
            st.session_state.domin = "软件开发"
            st.session_state.deep_thinking = True
            st.rerun()

        st.text("会话历史")
        session_list = load_sessions()
        for session in session_list:
            col1, col2 = st.columns([5, 1])
            with col1:
                if st.button(session, key=f"load_{session}", width="stretch", icon="📖",
                            type="primary" if session == st.session_state.current_session else "secondary"):
                    load_session(session)
                    st.rerun()
            with col2:
                if st.button("", key=f"delete_{session}", width="stretch", icon="❌️"):
                    delete_session(session)
                    st.rerun()

        st.divider()

        st.subheader("技术文档助手配置")

        model_options = ["deepseek-v4-pro", "qwen3.6-plus", "kimi-k2.6"]
        model_index = model_options.index(st.session_state.model) if st.session_state.model in model_options else 0
        selected_model = st.selectbox("模型选择：", model_options, index=model_index)
        st.session_state.model = selected_model

        max_tokens = st.slider("最大Token限制：", min_value=1024, max_value=8192,
                               value=st.session_state.max_tokens, step=512)
        st.session_state.max_tokens = max_tokens

        temperature = st.slider("温度参数：", min_value=0.0, max_value=1.0,
                                value=st.session_state.temperature, step=0.1)
        st.session_state.temperature = temperature

        domins = ["软件开发", "人工智能", "网络安全", "数据库"]
        domin_index = domins.index(st.session_state.domin) if st.session_state.domin in domins else 0
        selected_domin = st.selectbox("技术领域：", domins, index=domin_index)
        st.session_state.domin = selected_domin

        deep_thinking = st.checkbox("深度思考", value=st.session_state.deep_thinking)
        st.session_state.deep_thinking = deep_thinking