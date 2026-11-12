# LLM 成本估算器

第一个部署到公网的 Streamlit 项目。输入一段文本和模型单价，估算 token 数与调用成本，用来建立写 AI 应用必备的**成本意识**。

## 本地运行

```bash
# 1. 建虚拟环境（每个项目一个，不要把包装进全局 Python）
python -m venv .venv

# 2. 激活（Windows PowerShell）
.venv\Scripts\Activate.ps1
# 如果报 "禁止运行脚本"，先执行一次：
#   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

# 3. 装依赖
pip install -r requirements.txt

# 4. 跑起来
streamlit run app.py
```

浏览器会自动打开 http://localhost:8501 。

## 部署到公网（Streamlit Community Cloud，免费）

1. 在 GitHub 新建仓库 `llm-cost-calculator`，选 **Public**，**不要**勾选 "Add a README"（我们本地已经有了）。
2. 在本地项目目录执行：

   ```bash
   git remote add origin https://github.com/<你的用户名>/llm-cost-calculator.git
   git branch -M main
   git push -u origin main
   ```

   第一次 push 会弹出 Git Credential Manager 的浏览器登录，授权即可。

3. 打开 <https://share.streamlit.io> → **Continue with GitHub** 授权 → **Create app** → **Deploy a public app from GitHub**。
4. 填：Repository = 你的仓库，Branch = `main`，Main file path = `app.py`。
5. 点 **Advanced settings**，Python version 选 **3.12** 或 **3.13**（不要在云端用 3.14，依赖轮子未必齐）。
6. **Deploy**，等 2~5 分钟，拿到 `https://<应用名>.streamlit.app` 链接。

之后每次 `git push`，云端会自动重新部署 —— 这就是 CI/CD 的雏形，你已经白拿了。

> 免费版注意：应用一段时间无人访问会休眠，下次打开需要 30 秒左右唤醒，属正常现象。

## 这个项目练到了什么

| 能力 | 对应位置 |
| --- | --- |
| Python 虚拟环境与依赖管理 | `python -m venv` + `requirements.txt` |
| Git 基本工作流 | `git init / add / commit / push` |
| 敏感信息不入库 | `.gitignore` 屏蔽 `.streamlit/secrets.toml` |
| 一个 Web 界面 | `st.number_input` / `st.metric` / `st.sidebar` |
| 缓存思维 | `@st.cache_data` |
| 成本量化思维 | 单次 / 每天 / 每月三级估算 |

## 下一步（留给自己的 TODO）

- [ ] 用 `tiktoken` 替换粗略估算，量化误差
- [ ] 用 `st.session_state` 记录会话累计成本
- [ ] 单价改从 `st.secrets` 读取，为接入真实 API Key 做准备
- [ ] 接一个真实的 LLM 调用（这个就进入第 1 个月第 2 周的内容了）
