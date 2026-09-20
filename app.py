import os
import json
import re
from io import BytesIO

import streamlit as st
from openai import OpenAI
from pypdf import PdfReader

st.set_page_config(
    page_title="AI Policy Project Reviewer",
    page_icon="🧭",
    layout="wide",
)

st.markdown("""
<style>
.block-container {max-width: 1200px; padding-top: 2rem;}
h1 {letter-spacing: -0.03em;}
.card {
    padding: 1rem 1.1rem;
    border: 1px solid #e6e6e6;
    border-radius: 14px;
    margin-bottom: 0.8rem;
    background: #ffffff;
}
.small {color:#666; font-size:0.9rem;}
.badge {
    display:inline-block; padding:0.2rem 0.55rem; border-radius:999px;
    background:#f0f2f6; margin-right:0.35rem; font-size:0.8rem;
}
</style>
""", unsafe_allow_html=True)

st.title("🧭 AI Policy Project Reviewer")
st.caption("From Documents → Decisions → Risks → Red Team")

with st.sidebar:
    st.header("Project AI")
    st.write("把 AI 從「文字生成器」升級成專案品質控制工具。")
    st.divider()
    api_key = st.text_input("OpenAI API Key", type="password",
                            help="只在本次執行使用，不要把 Key 寫進程式碼。")
    model = st.selectbox("Model", ["gpt-5-mini", "gpt-5"], index=0)
    st.divider()
    st.markdown("**Demo 流程**")
    st.markdown("1. 上傳專案文件\n2. AI 結構化分析\n3. Red Team 挑戰\n4. PM 最終判斷")

uploaded = st.file_uploader(
    "上傳專案文件",
    type=["pdf", "txt"],
    help="Demo 建議使用 2～10 頁的政策簡報、會議紀錄或專案報告。"
)

def extract_text(file):
    if file.name.lower().endswith(".txt"):
        return file.getvalue().decode("utf-8", errors="ignore")
    reader = PdfReader(BytesIO(file.getvalue()))
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def build_prompt(document):
    return f"""
你是一名政府智庫的資深專案管理顧問與 Red Team Reviewer。
請分析下面的專案文件。

重要原則：
- 不要自行捏造事實、數字、政策或來源。
- 無法由文件支持的內容，標示為「資訊不足」。
- 區分「文件明確陳述」與「你的分析」。
- 你的任務是協助 PM 發現問題，不是替 PM 做政策決策。

請只輸出合法 JSON，欄位如下：

{{
  "summary": "150字內的 executive summary",
  "decisions": [
    {{"decision":"", "evidence":"", "impact":""}}
  ],
  "actions": [
    {{"action":"", "owner":"未指定", "deadline":"未指定", "priority":"High/Medium/Low"}}
  ],
  "risks": [
    {{"risk":"", "severity":"High/Medium/Low", "reason":"", "mitigation":""}}
  ],
  "evidence_gaps": [
    {{"claim":"", "problem":"", "needed_evidence":""}}
  ],
  "red_team": [
    {{"challenge":"", "why_it_matters":"", "question_for_team":""}}
  ],
  "executive_questions": [
    ""
  ]
}}

專案文件：
---
{document}
---
"""

def analyze(document, api_key, model):
    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=model,
        input=build_prompt(document),
    )
    raw = response.output_text.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)

if not uploaded:
    st.info("👆 先上傳一份 PDF 或 TXT。你可以先用虛構的政策專案文件做 Demo。")
    st.markdown("""
### 這個 Prototype 會做什麼？

| 模組 | PM 價值 |
|---|---|
| Executive Summary | 快速掌握專案脈絡 |
| Decision Log | 找出「到底決定了什麼」 |
| Action Items | 將會議轉成可追蹤事項 |
| Risk Radar | 提前暴露風險 |
| Evidence Gaps | 找出缺乏證據的主張 |
| AI Red Team | 主動攻擊方案盲點 |
| Executive Questions | 模擬主管提問 |
""")
    st.stop()

document = extract_text(uploaded)
st.success(f"已讀取：{uploaded.name}｜約 {len(document):,} 字元")

if not api_key:
    st.warning("請在左側輸入 OpenAI API Key 後開始分析。")
    st.stop()

if st.button("🚀 Analyze Project", type="primary", use_container_width=True):
    with st.spinner("AI 正在進行專案審查與 Red Team 分析…"):
        try:
            result = analyze(document, api_key, model)
            st.session_state["result"] = result
        except Exception as e:
            st.error(f"分析失敗：{e}")
            st.stop()

if "result" in st.session_state:
    r = st.session_state["result"]

    st.header("Executive Summary")
    st.markdown(f'<div class="card">{r["summary"]}</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📌 Decisions", "⚠️ Risks", "🔎 Evidence Gaps", "🔴 Red Team", "🎯 Executive Q&A"]
    )

    with tab1:
        st.subheader("Decision Log")
        for x in r.get("decisions", []):
            st.markdown(f"""
            <div class="card">
            <b>{x["decision"]}</b><br>
            <span class="small">Evidence：{x["evidence"]}</span><br>
            Impact：{x["impact"]}
            </div>
            """, unsafe_allow_html=True)
        st.subheader("Action Items")
        for x in r.get("actions", []):
            st.markdown(
                f'- **{x["action"]}** ｜ Owner: {x["owner"]} ｜ '
                f'Deadline: {x["deadline"]} ｜ Priority: {x["priority"]}'
            )

    with tab2:
        for x in r.get("risks", []):
            st.markdown(f"""
            <div class="card">
            <span class="badge">{x["severity"]}</span><b>{x["risk"]}</b><br>
            原因：{x["reason"]}<br>
            建議：{x["mitigation"]}
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        for x in r.get("evidence_gaps", []):
            st.markdown(f"""
            <div class="card">
            <b>主張：</b>{x["claim"]}<br>
            <b>問題：</b>{x["problem"]}<br>
            <b>需要：</b>{x["needed_evidence"]}
            </div>
            """, unsafe_allow_html=True)

    with tab4:
        st.warning("這一頁刻意不是幫你把報告寫得更漂亮，而是找出它最容易被攻擊的地方。")
        for i, x in enumerate(r.get("red_team", []), 1):
            st.markdown(f"""
            <div class="card">
            <b>Challenge {i}</b><br>
            {x["challenge"]}<br><br>
            <b>Why it matters：</b>{x["why_it_matters"]}<br>
            <b>Question：</b>{x["question_for_team"]}
            </div>
            """, unsafe_allow_html=True)

    with tab5:
        for i, q in enumerate(r.get("executive_questions", []), 1):
            st.markdown(f"### Q{i}. {q}")

    st.divider()
    st.caption("Prototype principle: AI increases cognitive leverage; humans retain final judgment.")
