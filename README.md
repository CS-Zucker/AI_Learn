# AI\_Learn

\##AI\_Step01

1.1. **LLM基础交互**

API调用：使用\`requests\`或\`httpx\`直接调用大模型API（如润道、通义千问、GPT-4等），理解HTTP请求结构、认证机制及流式传输（Streaming）。

对话逻辑：实现命令行多轮对话机器人，手动管理\`messages\`上下文列表，理解Token计数与截断机制。

1.2. **Prompt工程：**

设计SystemPrompt赋予模型角色。

学习Few-Shot提示词技巧。

重点：优化提示词使模型稳定输出JSON格式数据，并编写解析代码。

1.3. **第一阶段交付物：**

项目：一个具备特定业务角色（如：技术文档助手）的命令行对话机器人。

要求：支持多轮对话，能够稳定输出结构化JSON，代码提交至Git仓库。

***

AI\_Step01/

├── ai\_partner.py              # 主入口文件

├── utils/

│       ├── session\_manager.py     # 会话管理（创建、保存、加载、删除）

│       ├── openai\_client.py       # OpenAI客户端配置

│       └── prompts.py             # 系统提示词定义

└── ui/

         ├── sidebar.py             # 侧边栏UI组件

         └── chat\_area.py           # 聊天区域UI组件
