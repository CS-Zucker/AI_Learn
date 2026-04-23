import streamlit as st
import os
from openai import OpenAI
from datetime import datetime
import json


client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'),base_url="https://api.deepseek.com")

# 生成会话标识函数
def generate_session_name():
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S")

# 保存会话信息函数
def save_session():
    if st.session_state.current_session:
            # 构建新的会话对象
            session_data = {
                "current_session": st.session_state.current_session,
                "nick_name": st.session_state.nick_name,
                "nature": st.session_state.nature,
                "messages": st.session_state.messages
            }

            # 如果sessions目录不存在，则创建
            if not os.path.exists("sessions"):
                os.mkdir("sessions")

            # 保存会话信息
            with open(f"sessions/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)

# 加载所有会话列表信息
def load_sessions():
    session_list = []
    # 加载sessions目录下的所有文件
    if os.path.exists("sessions"):
        file_list = os.listdir("sessions")
        for filename in file_list:
            if filename.endswith(".json"):
                session_list.append(filename[:-5])
    session_list.sort(reverse=True)
    return session_list

# 加载指定会话信息函数
def load_session(session_name):
    try: 
        if os.path.exists(f"sessions/{session_name}.json"):
            with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.messages = session_data["messages"]
                st.session_state.current_session = session_data["current_session"]
                st.session_state.nick_name = session_data["nick_name"]
                st.session_state.nature = session_data["nature"]
    except Exception:
        st.error("加载会话信息失败") 

# 删除会话信息函数
def delete_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            os.remove(f"sessions/{session_name}.json")
            # 如果删除的是当前会话，则更新会话列表
            if session_name == st.session_state.current_session:
                st.session_state.current_session = generate_session_name()
                st.session_state.messages = []
    except Exception:
        st.error("删除会话失败")
    



# 系统提示词
system_prompt = """
        你叫 %s，现在是用户的真实伴侣，请完全带入伴侣角色。
        规则：
            1. 每次只会1条消息。
            2. 禁止任何场景或状态描述性文字。
            3. 匹配用户的语言。
            4. 回复简短，像微信聊天一样。
            5. 禁止使用任何图片。
            6. 有需要的话可以使用任何emoji。
        伴侣性格：
            - %s。
        你必须严格遵守上述规则来回复用户。
    """


# ---------页面配置
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🤖",
    # 布局
    layout="wide",
    # 侧边栏
    initial_sidebar_state="expanded",
    menu_items={}
)

# 标题
st.title("AI智能伴侣")

# Logo
st.logo(r"resource\img\ai_logo2.jpeg")


# 初始化聊天
if 'messages' not in st.session_state:
    st.session_state.messages = []
# 昵称
if 'nick_name' not in st.session_state:
    st.session_state.nick_name = "小A"
# 性格
if 'nature' not in st.session_state:
    st.session_state.nature = "活泼开朗"
# 会话标识
if "current_session" not in st.session_state:
    st.session_state.current_session = generate_session_name()


# 展示聊天消息
st.text(f"当前会话: {st.session_state.current_session}")
for message in st.session_state.messages: #{"role": "user", "content": prompt}
    st.chat_message(message['role']).write(message['content'])


# 聊天消息输入框
prompt = st.chat_input("请输入你的问题：")
if prompt:  # 输入框有内容时，转化为bool
    st.chat_message("user").write(prompt)
    print("--------> 调用AI大模型, 提示词：", prompt)
    # 保存用户输入
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 调用AI大模型
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt % (st.session_state.nick_name, st.session_state.nature)},
            *st.session_state.messages
        ],
        stream=True
    )

    # # 输出大模型结果(非流式输出)
    # print("<-------- 大模型返回的结果：", response.choices[0].message.content)
    # st.chat_message("assitant").write(response.choices[0].message.content)

    # 输出大模型结果(流式输出)
    response_message = st.empty()
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None: 
            content = chunk.choices[0].delta.content
            full_response += content
            response_message.chat_message("assistant").write(full_response)

    # 保存大模型模型返回的结果
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # 保存会话信息
    save_session()




# 侧边栏
st.sidebar.title("AI智能伴侣")
with st.sidebar:
    # 会话信息
    st.subheader("AI控制面板")

    # 新建会话
    if st.button("新建会话", width="stretch", icon="✏️"):
        # 1.保存会话信息
        save_session()

        # 2.创建新的会话
        if st.session_state.messages:  # 如果有消息，则保存
            st.session_state.messages = []
            st.session_state.current_session = generate_session_name()
            save_session()
            st.rerun()


    # 会话历史
    st.text("会话历史")
    session_list = load_sessions()
    for session in session_list:
        col1, col2 = st.columns([5, 1])
        with col1:
            # 加载会话信息
            if st.button(session, key=f"load_{session}", width="stretch", icon="📖", type="primary" if session == st.session_state.current_session else "secondary"):
                load_session(session)
                st.rerun()
        with col2:
            # 删除会话
            if st.button("", key=f"delete_{session}", width="stretch", icon="❌️"):
                delete_session(session)
                st.rerun()

    # 分隔线
    st.divider()

    # 伴侣信息
    st.subheader("伴侣信息")

    # 昵称输入框
    nick_name = st.text_input("昵称：", placeholder="请输入昵称", value=st.session_state.nick_name)
    if nick_name:  
        st.session_state.nick_name = nick_name

    # 性格输入框
    nature = st.text_input("性格：", placeholder="请输入性格", value=st.session_state.nature)
    if nature:  
        st.session_state.nature = nature