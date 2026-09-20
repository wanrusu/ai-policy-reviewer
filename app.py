import streamlit as st

st.set_page_config(
    page_title="Policy Intelligence Dashboard",
    page_icon="🧭",
    layout="wide"
)

# -----------------------------
# UI STYLE
# -----------------------------
st.markdown("""
<style>
.block-container {
    max-width: 1250px;
    padding-top: 2rem;
}

.main-title {
    font-size: 2.3rem;
    font-weight: 750;
    letter-spacing: -0.04em;
}

.subtitle {
    color: #666;
    font-size: 1rem;
    margin-bottom: 1.5rem;
}

.demo-badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 20px;
    background: #fff3cd;
    color: #664d03;
    font-size: 0.85rem;
    font-weight: 600;
}

.card {
    padding: 1.1rem;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    background: white;
    margin-bottom: 0.8rem;
}

.red-card {
    padding: 1.1rem;
    border-left: 5px solid #dc3545;
    border-radius: 10px;
    background: #fff8f8;
    margin-bottom: 0.8rem;
}

.small {
    color: #6b7280;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:

    st.title("🧭 Project AI")

    mode = st.radio(
        "Analysis Mode",
        ["🧪 Demo Mode", "🤖 Live AI"]
    )

    st.divider()

    st.markdown("### AI PM Workflow")

    st.markdown("""
    **01｜Understand**  
    建立專案脈絡

    **02｜Structure**  
    萃取決策與行動

    **03｜Challenge**  
    Red Team 找盲點

    **04｜Decide**  
    PM 做最終判斷
    """)

    st.divider()

    st.caption(
        "AI supports analysis. "
        "Final judgment remains with the project manager."
    )


# -----------------------------
# HEADER
# -----------------------------
st.markdown(
    '<div class="main-title">Policy Intelligence Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'From Documents → Decisions → Risks → Red Team'
    '</div>',
    unsafe_allow_html=True
)

if mode == "🧪 Demo Mode":
    st.markdown(
        '<span class="demo-badge">'
        '🧪 DEMO MODE · Sample Analysis'
        '</span>',
        unsafe_allow_html=True
    )

st.write("")


# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload project document",
    type=["txt", "pdf"],
    help="Demo Mode 不會將文件傳送至 AI API。"
)


if uploaded_file is None:

    st.info(
        "請上傳測試文件。Demo Mode 將展示預先設計的政策專案分析結果。"
    )

    st.stop()


# -----------------------------
# ANALYZE
# -----------------------------
if st.button(
    "🚀 Analyze Project",
    type="primary",
    use_container_width=True
):

    st.session_state["analyzed"] = True


if "analyzed" not in st.session_state:
    st.stop()


# -----------------------------
# PROJECT HEALTH
# -----------------------------
st.divider()

st.subheader("Project Health")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Decisions",
    "3"
)

c2.metric(
    "Risks",
    "5",
    "2 High"
)

c3.metric(
    "Evidence Gaps",
    "4",
    "Needs Review"
)

c4.metric(
    "Action Items",
    "6"
)


# -----------------------------
# EXECUTIVE SUMMARY
# -----------------------------
st.subheader("Executive Summary")

st.markdown("""
<div class="card">

本計畫擬導入生成式 AI 協助地方政府處理民眾諮詢、
行政文件與內部知識查詢。

目前已提出初步導入規模、預算與預期效益，
但在效益估算、KPI、執行單位承諾及風險評估方面，
仍存在需要進一步驗證的資訊缺口。

</div>
""", unsafe_allow_html=True)


# -----------------------------
# TABS
# -----------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([

    "📌 Decisions",
    "⚠️ Risk Radar",
    "🔎 Evidence Gaps",
    "🔴 Red Team",
    "🎯 Executive Questions"

])


# -----------------------------
# DECISIONS
# -----------------------------
with tab1:

    st.markdown("### Decision Intelligence")

    st.markdown("""
<div class="card">

<b>Decision 01</b><br>
第一階段規劃導入 20 個行政服務窗口。

<br><br>

<span class="small">
Status：初步規劃，參與單位尚待確認
</span>

</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="card">

<b>Decision 02</b><br>
第一年完成系統建置及相關人員培訓。

<br><br>

<span class="small">
Evidence：專案文件明確陳述
</span>

</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="card">

<b>Decision 03</b><br>
初步規劃經費為新台幣 2,000 萬元。

<br><br>

<span class="small">
Validation：預算估算依據尚未提供
</span>

</div>
""", unsafe_allow_html=True)


# -----------------------------
# RISKS
# -----------------------------
with tab2:

    st.markdown("### Risk Radar")

    st.error(
        "HIGH｜效益估算風險：行政效率提升 30% 缺乏基準值與驗證方式。"
    )

    st.error(
        "HIGH｜執行風險：實際參與地方政府及責任分工尚未確認。"
    )

    st.warning(
        "MEDIUM｜KPI 尚未定義，可能造成專案完成後無法客觀評估成效。"
    )

    st.warning(
        "MEDIUM｜2,000 萬元預算尚未看到成本結構與估算依據。"
    )

    st.warning(
        "MEDIUM｜文件認定技術風險可控，但尚未提供風險評估證據。"
    )


# -----------------------------
# EVIDENCE
# -----------------------------
with tab3:

    st.markdown("### Evidence Gap Detector")

    st.markdown("""
<div class="card">

<b>Claim</b><br>
「導入 AI 後可提升行政效率 30%」

<br><br>

<b>Evidence Gap</b><br>
尚未提供現況處理時間、Pilot 結果或比較基準。

<br><br>

<b>Needed Evidence</b><br>
Baseline、Pilot Data、Before / After Measurement

</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="card">

<b>Claim</b><br>
「AI 將提升民眾滿意度」

<br><br>

<b>Evidence Gap</b><br>
尚未定義滿意度衡量方式。

<br><br>

<b>Needed Evidence</b><br>
Survey KPI、Service Quality Metrics

</div>
""", unsafe_allow_html=True)


# -----------------------------
# RED TEAM
# -----------------------------
with tab4:

    st.markdown("### 🔴 AI Red Team")

    st.caption(
        "目的不是美化方案，而是在正式審查前主動尋找弱點。"
    )

    st.markdown("""
<div class="red-card">

<b>Challenge 01｜30% 從哪裡來？</b>

<br><br>

如果沒有 Pilot 或既有行政流程的 Baseline，
「提升效率 30%」目前較接近假設，而非可驗證結論。

<br><br>

<b>Red Team Question：</b><br>
如果審查委員要求提出 30% 的計算依據，
團隊目前能提供什麼證據？

</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="red-card">

<b>Challenge 02｜為什麼需要 2,000 萬？</b>

<br><br>

文件提供總預算，但尚未呈現模型、
系統整合、人員訓練與維運成本結構。

<br><br>

<b>Red Team Question：</b><br>
如果預算被刪減 30%，哪些工作仍然必須保留？

</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="red-card">

<b>Challenge 03｜誰真正承諾參與？</b>

<br><br>

「部分地方政府表示支持」不等於正式參與承諾。

<br><br>

<b>Red Team Question：</b><br>
目前有哪些單位已確認人力、資料與導入時程？

</div>
""", unsafe_allow_html=True)


# -----------------------------
# EXECUTIVE QUESTIONS
# -----------------------------
with tab5:

    st.markdown("### Executive Meeting Simulator")

    questions = [

        "為什麼這個計畫現在一定要做？",

        "行政效率提升 30% 的證據是什麼？",

        "為什麼需要 2,000 萬元？",

        "如果地方政府參與度不足，Plan B 是什麼？",

        "一年後我們用什麼 KPI 判斷這個專案成功？"

    ]

    for i, q in enumerate(questions, 1):

        st.markdown(
            f"### Q{i}. {q}"
        )


# -----------------------------
# FOOTER
# -----------------------------
st.divider()

st.caption(
    "Prototype v0.2 | "
    "AI-assisted Project Review | "
    "Demo data only"
)