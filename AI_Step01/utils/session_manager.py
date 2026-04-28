import os
import json
import streamlit as st
from datetime import datetime

# 生成会话时间戳
def generate_session_time():
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S")

# 保存会话信息
def save_session():
    if st.session_state.current_session:
        session_data = {
            "current_session": st.session_state.current_session,
            "messages": st.session_state.messages,
            "model": st.session_state.model,
            "max_tokens": st.session_state.max_tokens,
            "temperature": st.session_state.temperature,
            "domin": st.session_state.domin,
            "deep_thinking": st.session_state.deep_thinking
        }

        if not os.path.exists("sessions"):
            os.mkdir("sessions")

        with open(f"sessions/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)

# 加载会话列表
def load_sessions():
    session_list_with_time = []
    if os.path.exists("sessions"):
        file_list = os.listdir("sessions")
        for filename in file_list:
            if filename.endswith(".json"):
                # 提取文件名中的"会话名称和时间戳" ("abcdefg..._2026-04-28 10-11-54")
                session_name = filename[:-5]
                try:
                    # 提取时间戳（YYYY-MM-DD_HH-MM-SS）
                    timestamp_str = session_name.split('_')[-1]
                    # 解析时间戳为 datetime 对象
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H-%M-%S")
                except Exception:
                    # 如果时间戳格式错误，使用默认值
                    # 1970-01-01 00:00:00 是一个早于所有实际时间的默认值
                    timestamp = datetime(1970, 1, 1)
                session_list_with_time.append({"timestamp": timestamp, "session_name": session_name})
    # 按时间戳排序（最近的在前）
    session_list_with_time.sort(key=lambda x: x["timestamp"], reverse=True)
    session_list = [item["session_name"] for item in session_list_with_time]
    return session_list

# 加载指定会话信息
def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
                if "messages" in session_data:
                    st.session_state.messages = session_data["messages"]
                if "current_session" in session_data:
                    st.session_state.current_session = session_data["current_session"]
                if "model" in session_data:
                    st.session_state.model = session_data["model"]
                if "max_tokens" in session_data:
                    st.session_state.max_tokens = session_data["max_tokens"]
                if "temperature" in session_data:
                    st.session_state.temperature = session_data["temperature"]
                if "domin" in session_data:
                    st.session_state.domin = session_data["domin"]
                if "deep_thinking" in session_data:
                    st.session_state.deep_thinking = session_data["deep_thinking"]
                st.rerun()
    except Exception:
        st.error("加载会话信息失败")

# 删除指定会话
def delete_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            os.remove(f"sessions/{session_name}.json")
            if session_name == st.session_state.current_session:
                st.session_state.current_session = generate_session_time()
                st.session_state.messages = []
    except Exception:
        st.error("删除会话失败")