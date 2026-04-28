import streamlit as st
from utils.openai_client import client
from utils.prompts import system_prompt
from utils.session_manager import save_session, generate_session_time


def render_chat_area():
    st.text(f"当前会话: {st.session_state.current_session}")
    for message in st.session_state.messages:
        st.chat_message(message['role']).write(message['content'])

    prompt = st.chat_input("请输入你的问题：")
    if prompt:
        st.chat_message("user").write(prompt)
        print("--------> 调用AI大模型, 提示词：", prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=st.session_state.model,
            messages=[
                {"role": "system", "content": system_prompt % st.session_state.domin},
                *st.session_state.messages
            ],
            temperature=st.session_state.temperature,
            max_tokens=st.session_state.max_tokens,
            extra_body={"enable_thinking": st.session_state.deep_thinking},
            stream=True,
            stream_options={
                "include_usage": True
            }
        )

        response_message = st.empty()
        full_response = ""
        full_reasoning = ""
        is_answering = False

        for chunk in response:
            if not chunk.choices:
                print("\n" + "=" * 20 + "Token 消耗" + "=" * 20 + "\n")
                print("输入Token：", chunk.usage.prompt_tokens, "输出Token：", chunk.usage.completion_tokens,
                      "总计Token：", chunk.usage.total_tokens)
                continue

            delta = chunk.choices[0].delta

            if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
                if not is_answering:
                    full_reasoning += delta.reasoning_content
                    response_message.chat_message("assistant").write(f"**思考过程：**\n{full_reasoning}")

            if hasattr(delta, "content") and delta.content is not None:
                if not is_answering:
                    is_answering = True
                content = delta.content
                full_response += content
                display_content = f"**思考过程：**\n{full_reasoning}\n\n---\n\n**回复：**\n{full_response}" if full_reasoning else full_response
                response_message.chat_message("assistant").write(display_content)

        if full_reasoning:
            saved_content = f"**思考过程：**\n{full_reasoning}\n\n---\n\n**回复：**\n{full_response}"
        else:
            saved_content = full_response
        st.session_state.messages.append({"role": "assistant", "content": saved_content})

        # 生成新的会话标识(仅第一次对话时生效)
        if len(st.session_state.messages) == 2:
            session_time = st.session_state.current_session
            session_summary = full_response.replace("\n", " ").strip()[:20]
            session_summary = session_summary.replace("\\", " ").replace("/", " ").replace(":", " ").replace("*", " ").replace("?", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ")
            session_summary_name = f"{session_summary}..." if len(full_response.replace("\n", " ").strip()) > 20 else session_summary
            st.session_state.current_session = session_summary_name + '_' + session_time

        save_session()
        st.rerun()