"""
LLM 成本估算器 —— 你的第一个可公网访问的项目。

学习要点（建议对照代码逐条读一遍，这比看教程有用）：
1. Streamlit 的执行模型：用户每次交互，整个脚本会从上到下重跑一遍。
2. 所以不要在脚本里做"只该做一次"的重活 —— 用 @st.cache_data 缓存。
3. 需要跨重跑保存的状态放 st.session_state（本文件还用不到，但要知道）。
4. 布局用 st.sidebar / st.columns / st.metric，几行就出一个像样的页面。
"""

import math

import streamlit as st

# set_page_config 必须是第一个 streamlit 调用
st.set_page_config(page_title="LLM 成本估算器", page_icon="💰", layout="centered")


@st.cache_data
def estimate_tokens(text: str) -> int:
    """
    粗略估算 token 数。注意：这是估算，不是精确值。
      - 中文汉字：约 1 字 ≈ 0.7 token
      - 其它字符：约 1 字符 ≈ 0.3 token
    真实 token 数请以 API 返回的 usage 字段为准（这是面试会问的细节）。
    """
    zh = sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")
    other = len(text) - zh
    return max(1, math.ceil(zh * 0.7 + other * 0.3))


st.title("💰 LLM 成本估算器")
st.caption(
    "输入一段文本和单价，估算 token 数与调用成本。"
    "建立『成本意识』——这是 AI 应用工程师和『只会调 API 的人』的区别之一。"
)

# ---------------- 侧边栏：参数 ----------------
with st.sidebar:
    st.header("单价设置")
    st.caption("价格请以官方价目表为准。这里刻意不内置具体价格，避免写死后过期误导。")

    price_in = st.number_input(
        "输入价格（元 / 百万 token）", min_value=0.0, value=1.0, step=0.1, format="%.4f"
    )
    price_out = st.number_input(
        "输出价格（元 / 百万 token）", min_value=0.0, value=4.0, step=0.1, format="%.4f"
    )
    out_ratio = st.slider("输出长度 ≈ 输入的几倍", 0.1, 3.0, 0.5, 0.1)
    calls_per_day = st.number_input("每天调用次数", min_value=1, value=100, step=10)

# ---------------- 主体：输入 ----------------
default_text = (
    "请把下面这段会议记录总结成 3 条待办事项，并标注负责人：\n"
    "今天讨论了知识库问答系统的检索效果问题。张三负责把切分策略从固定长度改成按标题递归切分，"
    "李四负责补齐 50 条评测问题，下周三之前给出初版评测报告。"
)
text = st.text_area("要发送给模型的文本", value=default_text, height=180)

# ---------------- 计算 ----------------
in_tokens = estimate_tokens(text)
out_tokens = max(1, int(in_tokens * out_ratio))

cost_one = (in_tokens * price_in + out_tokens * price_out) / 1_000_000
cost_day = cost_one * calls_per_day
cost_month = cost_day * 30

# ---------------- 展示 ----------------
c1, c2, c3 = st.columns(3)
c1.metric("估算输入 token", f"{in_tokens:,}")
c2.metric("估算输出 token", f"{out_tokens:,}")
c3.metric("单次成本", f"¥{cost_one:.6f}")

c4, c5 = st.columns(2)
c4.metric("每天成本（按设定次数）", f"¥{cost_day:.4f}")
c5.metric("每月成本（30 天）", f"¥{cost_month:.2f}")

if cost_month > 1000:
    st.warning("月成本超过 1000 元，先想清楚：能不能用小模型？能不能压缩 prompt？能不能做缓存？")

st.divider()

with st.expander("为什么这个估算可能不准（点开看，面试会问）"):
    st.markdown(
        """
- 不同厂商的分词器不同，同一个中文句子在不同模型上 token 数能差 20% 以上。
- 实际计费还包含 **system prompt**、**对话历史**、**工具定义**，这些都会重复计费。
- 输出 token 通常比输入贵得多（常见 2~4 倍），所以**控制输出长度**往往比压缩输入更省钱。
- 缓存（相同问题不重复调用）、批处理、小模型路由，都能把成本砍掉一个数量级。
"""
    )

with st.expander("留给你自己的作业（做完这一步才算学会）"):
    st.markdown(
        """
1. 把 `estimate_tokens` 换成真正的 tokenizer（如 `tiktoken`），对比估算误差。
2. 加一个 `st.session_state` 计数器，记录"本次会话一共估算了多少成本"。
3. 把单价改成从 `st.secrets` 读取 —— 为以后放 API Key 做准备（**密钥绝不能写进代码**）。
"""
    )

st.caption("第一个公网项目 · 用 Streamlit 部署 · 源码见 GitHub")
