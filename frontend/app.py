from __future__ import annotations

import os
from typing import Any

import pandas as pd
import requests
import streamlit as st

API_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Sales Memory Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

    :root {
        --bg:          #f8f9fc;
        --white:       #ffffff;
        --surface:     #f1f3f8;
        --border:      #e2e6ef;
        --border-light:#edf0f7;
        --accent:      #2563eb;
        --accent-light:#eff4ff;
        --accent-dark: #1d4ed8;
        --green:       #16a34a;
        --green-light: #f0fdf4;
        --amber:       #d97706;
        --amber-light: #fffbeb;
        --red:         #dc2626;
        --red-light:   #fef2f2;
        --text:        #111827;
        --text-muted:  #6b7280;
        --text-light:  #9ca3af;
        --shadow-sm:   0 1px 3px rgba(0,0,0,.06), 0 1px 2px rgba(0,0,0,.04);
        --shadow:      0 4px 12px rgba(0,0,0,.06), 0 1px 3px rgba(0,0,0,.04);
        --shadow-md:   0 8px 24px rgba(0,0,0,.08), 0 2px 6px rgba(0,0,0,.04);
        --radius:      10px;
        --radius-sm:   7px;
        --radius-lg:   14px;
    }

    /* ── Base ── */
    html, body, .stApp {
        background: var(--bg) !important;
        font-family: 'Inter', sans-serif !important;
        color: var(--text) !important;
    }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container {
        padding: 2rem 2.5rem 4rem !important;
        max-width: 1300px;
    }

    /* ── Sidebar shell ── */
    section[data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid var(--border) !important;
    }
    section[data-testid="stSidebar"] * {
        font-family: 'Inter', sans-serif !important;
    }
    /* hide the real radio widget completely */
    section[data-testid="stSidebar"] .stRadio {
        display: none !important;
    }

    /* ── Custom nav item ── */
    .nav-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 9px 12px;
        border-radius: 8px;
        cursor: pointer;
        font-size: .875rem;
        font-weight: 500;
        color: #4b5563;
        margin-bottom: 2px;
        transition: background .15s, color .15s;
        text-decoration: none;
        border: 1px solid transparent;
    }
    .nav-item:hover {
        background: #f3f4f6;
        color: #111827;
    }
    .nav-item.active {
        background: #eff6ff;
        color: #1d4ed8;
        font-weight: 600;
        border-color: #dbeafe;
    }
    .nav-icon {
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 7px;
        font-size: 14px;
        flex-shrink: 0;
        background: #f3f4f6;
    }
    .nav-item.active .nav-icon {
        background: #dbeafe;
    }
    .nav-label { flex: 1; letter-spacing: -.01em; }

    /* nav section group label */
    .nav-group-label {
        font-size: .67rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .1em;
        color: #9ca3af;
        padding: 0 12px;
        margin: 14px 0 5px;
    }

    /* nav divider */
    .nav-divider {
        height: 1px;
        background: #f3f4f6;
        margin: 10px 0;
    }

    /* sidebar footer */
    .sidebar-footer {
        position: absolute;
        bottom: 0; left: 0; right: 0;
        padding: 12px 16px;
        border-top: 1px solid #f3f4f6;
        background: #fafafa;
    }
    .sidebar-footer-text {
        font-size: .72rem;
        color: #9ca3af;
        line-height: 1.5;
    }
    .backend-badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        font-size: .68rem;
        background: #f3f4f6;
        border: 1px solid #e5e7eb;
        color: #6b7280;
        padding: 2px 7px;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
        margin-top: 4px;
    }
    .status-live {
        display: inline-block;
        width: 6px; height: 6px;
        border-radius: 50%;
        background: #22c55e;
        flex-shrink: 0;
    }

    /* ── Headings ── */
    h1, h2, h3, h4 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: var(--text) !important;
        letter-spacing: -.3px !important;
    }
    h1 { font-size: 1.75rem !important; font-weight: 700 !important; }
    h2 { font-size: 1.2rem  !important; font-weight: 700 !important; }
    h3 { font-size: 1rem    !important; font-weight: 600 !important; }

    p, li, span, div { color: var(--text) !important; }

    /* ── Metric cards ── */
    [data-testid="stMetric"] {
        background: var(--white) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-lg) !important;
        padding: 1.25rem 1.5rem !important;
        box-shadow: var(--shadow-sm) !important;
        transition: box-shadow .2s !important;
    }
    [data-testid="stMetric"]:hover {
        box-shadow: var(--shadow-md) !important;
    }
    [data-testid="stMetricLabel"] {
        color: var(--text-muted) !important;
        font-size: .72rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: .08em !important;
    }
    [data-testid="stMetricValue"] {
        color: var(--accent) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
    }

    /* ── Primary button ── */
    .stButton > button {
        background: var(--accent) !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        font-size: .875rem !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        padding: .55rem 1.4rem !important;
        box-shadow: 0 1px 3px rgba(37,99,235,.25) !important;
        transition: background .15s, box-shadow .15s, transform .1s !important;
        cursor: pointer !important;
    }
    .stButton > button:hover {
        background: var(--accent-dark) !important;
        box-shadow: 0 4px 12px rgba(37,99,235,.3) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }

    /* sidebar seed button override — subtle ghost style */
    section[data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        color: #6b7280 !important;
        border: 1px solid #e5e7eb !important;
        box-shadow: none !important;
        font-weight: 500 !important;
        font-size: .82rem !important;
        padding: .45rem 1rem !important;
        text-align: left !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #f3f4f6 !important;
        color: #374151 !important;
        box-shadow: none !important;
        transform: none !important;
    }

    /* ── Form fields ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: var(--white) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: .875rem !important;
        box-shadow: var(--shadow-sm) !important;
        transition: border-color .15s, box-shadow .15s !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(37,99,235,.12) !important;
        outline: none !important;
    }
    .stSelectbox > div > div {
        background: var(--white) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text) !important;
        box-shadow: var(--shadow-sm) !important;
    }
    label, .stSelectbox label, .stTextInput label, .stTextArea label {
        color: var(--text-muted) !important;
        font-size: .8rem !important;
        font-weight: 600 !important;
        letter-spacing: .02em !important;
        text-transform: none !important;
    }

    /* ── Expanders ── */
    .streamlit-expanderHeader {
        background: var(--white) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: .875rem !important;
        font-weight: 600 !important;
        padding: .7rem 1rem !important;
        box-shadow: var(--shadow-sm) !important;
    }
    .streamlit-expanderContent {
        background: var(--white) !important;
        border: 1px solid var(--border) !important;
        border-top: none !important;
        border-radius: 0 0 var(--radius-sm) var(--radius-sm) !important;
        padding: 1rem !important;
    }

    /* ── Alerts ── */
    .stSuccess {
        background: var(--green-light) !important;
        border: 1px solid #bbf7d0 !important;
        border-radius: var(--radius-sm) !important;
        color: #166534 !important;
    }
    .stWarning {
        background: var(--amber-light) !important;
        border: 1px solid #fde68a !important;
        border-radius: var(--radius-sm) !important;
        color: #92400e !important;
    }
    .stError {
        background: var(--red-light) !important;
        border: 1px solid #fecaca !important;
        border-radius: var(--radius-sm) !important;
        color: #991b1b !important;
    }
    .stInfo {
        background: var(--accent-light) !important;
        border: 1px solid #bfdbfe !important;
        border-radius: var(--radius-sm) !important;
        color: #1e40af !important;
    }

    /* ── Dataframe ── */
    .stDataFrame {
        border-radius: var(--radius) !important;
        border: 1px solid var(--border) !important;
        box-shadow: var(--shadow-sm) !important;
        overflow: hidden !important;
    }

    /* ── Code blocks ── */
    .stCode, pre, code {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color: #1e40af !important;
        font-size: .82rem !important;
    }

    /* ── Divider / HR ── */
    hr { border-color: var(--border) !important; margin: 1.2rem 0 !important; }

    /* ── Captions ── */
    .stCaption, small { color: var(--text-muted) !important; font-size: .8rem !important; }

    /* ── Spinner ── */
    .stSpinner > div { border-top-color: var(--accent) !important; }

    /* ─── Custom components ─── */

    /* Page header */
    .page-header {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        padding: 1.5rem 1.75rem;
        background: var(--white);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-sm);
        margin-bottom: 1.75rem;
    }
    .page-header-icon {
        font-size: 1.5rem;
        width: 44px;
        height: 44px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--accent-light);
        border-radius: 10px;
        flex-shrink: 0;
    }
    .page-header-text h1 {
        margin: 0 0 .2rem !important;
        font-size: 1.35rem !important;
    }
    .page-header-text p {
        margin: 0;
        color: var(--text-muted) !important;
        font-size: .875rem;
    }

    /* Section label */
    .section-label {
        font-size: .72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .1em;
        color: var(--text-light);
        padding-bottom: .5rem;
        border-bottom: 1px solid var(--border-light);
        margin: 1.6rem 0 1rem;
    }

    /* Tags / pills */
    .tag {
        display: inline-block;
        background: var(--accent-light);
        color: var(--accent) !important;
        border: 1px solid #bfdbfe;
        font-size: .7rem;
        font-weight: 600;
        padding: .18rem .6rem;
        border-radius: 20px;
        margin: .1rem .1rem;
        letter-spacing: .02em;
    }

    /* Status dot */
    .status-dot {
        display: inline-block;
        width: 7px; height: 7px;
        border-radius: 50%;
        margin-right: 5px;
        vertical-align: middle;
    }
    .dot-green  { background: var(--green); }
    .dot-amber  { background: var(--amber); }
    .dot-blue   { background: var(--accent); }

    /* Activity card */
    .activity-card {
        background: var(--white);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: .875rem 1.1rem;
        margin-bottom: .5rem;
        box-shadow: var(--shadow-sm);
        transition: box-shadow .15s;
    }
    .activity-card:hover { box-shadow: var(--shadow); }
    .op-badge {
        font-size: .68rem;
        font-weight: 700;
        letter-spacing: .08em;
        text-transform: uppercase;
        padding: .18rem .55rem;
        border-radius: 4px;
    }
    .op-retain { background: #eff4ff; color: #2563eb; border: 1px solid #bfdbfe; }
    .op-recall { background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }
    .op-reflect{ background: #fffbeb; color: #d97706; border: 1px solid #fde68a; }
    .op-other  { background: var(--surface); color: var(--text-muted); border: 1px solid var(--border); }

    /* Compare columns */
    .compare-header {
        font-size: .75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .08em;
        padding: .3rem .7rem;
        border-radius: 5px;
        display: inline-block;
        margin-bottom: .6rem;
    }
    .compare-bad  { background: var(--red-light);   color: #991b1b; border: 1px solid #fecaca; }
    .compare-good { background: var(--green-light);  color: #166534; border: 1px solid #bbf7d0; }

    /* Sidebar brand */
    .sidebar-brand {
        padding: .25rem 0 1rem;
    }
    .sidebar-brand-name {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1rem;
        font-weight: 800;
        color: var(--text) !important;
        letter-spacing: -.3px;
    }
    .sidebar-brand-sub {
        font-size: .7rem;
        color: var(--text-light) !important;
        letter-spacing: .03em;
        margin-top: 1px;
    }

    /* Memory item */
    .memory-item {
        background: var(--white);
        border: 1px solid var(--border);
        border-left: 3px solid var(--accent);
        border-radius: var(--radius-sm);
        padding: .9rem 1.1rem;
        margin-bottom: .6rem;
        box-shadow: var(--shadow-sm);
    }

    /* Form card wrapper */
    .form-card {
        background: var(--white);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        box-shadow: var(--shadow-sm);
        margin-bottom: 1rem;
    }

    /* Health card */
    .health-row {
        display: flex;
        gap: .6rem;
        flex-wrap: wrap;
        margin: .5rem 0 1rem;
    }
    .health-chip {
        display: flex;
        align-items: center;
        gap: .4rem;
        background: var(--white);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: .3rem .85rem;
        font-size: .78rem;
        font-weight: 600;
        box-shadow: var(--shadow-sm);
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #c4cad6; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def api_get(path: str) -> Any:
    r = requests.get(f"{API_URL}{path}", timeout=45)
    r.raise_for_status()
    return r.json()


def api_post(path: str, payload: dict[str, Any] | None = None) -> Any:
    r = requests.post(f"{API_URL}{path}", json=payload or {}, timeout=60)
    r.raise_for_status()
    return r.json()


def page_header(icon: str, title: str, subtitle: str = "") -> None:
    st.markdown(
        f"""
        <div class="page-header">
          <div class="page-header-icon">{icon}</div>
          <div class="page-header-text">
            <h1>{title}</h1>
            <p>{subtitle}</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section(label: str) -> None:
    st.markdown(f'<div class="section-label">{label}</div>', unsafe_allow_html=True)


def tags_html(tags: list[str]) -> str:
    return "".join(f'<span class="tag">{t}</span>' for t in tags)


def memory_badge(mode: str | None = None, fallback: bool | None = None) -> None:
    if fallback is True or (mode and "fallback" in mode.lower()):
        st.warning("Memory mode: Local fallback — configure HINDSIGHT_API_KEY to enable cloud memory.")
    else:
        st.success(f"Memory mode: {mode or 'Hindsight Cloud'}")


def source_badge(source: str | None, warning: str | None = None) -> None:
    if source == "hindsight":
        st.success("Memory source: Hindsight Cloud")
    elif source == "fallback":
        st.warning("Memory source: local fallback")
    else:
        st.info(f"Memory source: {source or 'unknown'}")
    if warning:
        st.warning(warning)


def load_prospects() -> list[dict[str, Any]]:
    try:
        return api_get("/prospects")
    except requests.RequestException:
        return []


def prospect_picker(label: str = "Select prospect") -> dict[str, Any] | None:
    prospects = load_prospects()
    if not prospects:
        st.info("No prospects yet. Seed demo data or log an interaction first.")
        return None
    labels = [f"{p['company']}  —  {p['name']}  ({p['role_title']})" for p in prospects]
    idx = st.selectbox(label, range(len(prospects)), format_func=lambda i: labels[i])
    return prospects[idx]


def show_memory_items(memories: list[dict[str, Any]]) -> None:
    if not memories:
        st.info("No recalled memories returned yet.")
        return
    for i, item in enumerate(memories, 1):
        mem_type = item.get("type", "memory")
        with st.expander(f"Memory {i}  ·  {mem_type}"):
            st.write(item.get("text", item))
            row = st.columns(3)
            if item.get("tags"):
                row[0].markdown(tags_html(item["tags"]), unsafe_allow_html=True)
            if item.get("score") is not None:
                row[1].caption(f"Relevance score: **{item['score']}**")
            if item.get("created_at"):
                row[2].caption(item["created_at"])
            if item.get("metadata"):
                st.json(item["metadata"])


# ── Pages ─────────────────────────────────────────────────────────────────────

def dashboard_page() -> None:
    page_header("🧠", "Sales Memory Agent", "Deal-aware sales intelligence · retain · recall · reflect")

    try:
        stats = api_get("/dashboard")
    except requests.RequestException as exc:
        st.error(f"Backend not reachable at `{API_URL}`. Start FastAPI first.\n\n{exc}")
        return

    memory_badge(fallback=stats["fallback_mode"])
    health = stats.get("memory_health", {})

    section("Hindsight Memory Status")
    chips = [
        ("Enabled",    health.get("hindsight_enabled"), "dot-blue"),
        ("Configured", health.get("configured"),        "dot-blue"),
        ("Reachable",  health.get("reachable"),         "dot-green"),
        ("Fallback",   health.get("fallback_enabled"),  "dot-amber"),
    ]
    html = '<div class="health-row">'
    for label, val, dot_cls in chips:
        yes = bool(val)
        dot = dot_cls if yes else "dot-amber"
        text = "Yes" if yes else "No"
        html += (
            f'<div class="health-chip">'
            f'<span class="status-dot {dot}"></span>'
            f'<span>{label}: <strong>{text}</strong></span>'
            f'</div>'
        )
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

    if health.get("bank_id"):
        st.caption(f"Bank ID: `{health['bank_id']}`")
    if health.get("last_error"):
        st.warning(health["last_error"])

    section("Overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("Prospects",          stats["prospects"])
    c2.metric("Interactions",        stats["interactions"])
    c3.metric("Retained Memories",   stats["retained_memories"])

    left, right = st.columns([1, 2], gap="large")

    with left:
        section("Top Objections")
        if stats["top_objections"]:
            st.dataframe(pd.DataFrame(stats["top_objections"]), hide_index=True, use_container_width=True)
        else:
            st.info("No objections captured yet.")

    with right:
        section("Recent Memory Activity")
        for item in stats["recent_activity"]:
            op = item["operation"].lower()
            op_cls = {"retain": "op-retain", "recall": "op-recall", "reflect": "op-reflect"}.get(op, "op-other")
            t_html = tags_html(item.get("tags", []))
            st.markdown(
                f"""
                <div class="activity-card">
                  <span class="op-badge {op_cls}">{item['operation'].upper()}</span>&nbsp;
                  <strong>{item['company']}</strong> / {item['prospect_name']}
                  <br>
                  <span style="font-size:.78rem;color:#9ca3af;">{item['created_at']}</span>
                  &nbsp;&nbsp;{t_html}
                </div>
                """,
                unsafe_allow_html=True,
            )


def log_interaction_page() -> None:
    page_header("📝", "Log Interaction", "Record a meeting and retain memory for future deal intelligence.")

    with st.form("interaction_form"):
        section("Prospect Details")
        c1, c2, c3 = st.columns(3)
        prospect_name       = c1.text_input("Prospect name")
        company             = c2.text_input("Company")
        role_title          = c3.text_input("Role / Title")

        section("Interaction Details")
        interaction_type = st.selectbox(
            "Interaction type",
            ["Discovery call", "Demo", "Security review", "Pricing call", "Procurement update", "Sales interaction"],
        )
        meeting_notes = st.text_area("Meeting notes", height=130, placeholder="Summarise what happened in this meeting…")

        section("Deal Intelligence")
        c4, c5 = st.columns(2)
        objections           = c4.text_input("Objections raised")
        competitor_mentioned = c5.text_input("Competitor mentioned")

        c6, c7 = st.columns(2)
        budget   = c6.text_input("Budget")
        timeline = c7.text_input("Timeline")

        decision_makers = st.text_input("Decision makers")
        next_steps      = st.text_input("Next steps")
        deal_id         = st.text_input("Deal ID (optional)")

        submitted = st.form_submit_button("Save & Retain Memory", type="primary", use_container_width=True)

    if submitted:
        payload = {
            "prospect_name": prospect_name, "company": company, "role_title": role_title,
            "interaction_type": interaction_type, "meeting_notes": meeting_notes,
            "objections": objections, "competitor_mentioned": competitor_mentioned,
            "budget": budget, "timeline": timeline,
            "decision_makers": decision_makers, "next_steps": next_steps,
            "deal_id": deal_id or None,
        }
        try:
            result = api_post("/interactions", payload)
            if result["memory_status"] == "retained":
                st.success("Interaction saved. Memory retained in Hindsight.")
            elif result["memory_status"] == "fallback":
                st.warning("Interaction saved. Memory retained in local fallback.")
            else:
                st.error("Interaction saved, but memory retain failed.")
            if result.get("memory_warning"):
                st.warning(result["memory_warning"])
            if result.get("memory_error"):
                st.error(result["memory_error"])
            section("Retained Payload Preview")
            st.code(result.get("retained_payload", {}).get("preview", ""), language="text")
            with st.expander("Full JSON response"):
                st.json(result)
        except requests.RequestException as exc:
            st.error(f"Could not save interaction: {exc}")


def sales_brief_page() -> None:
    page_header("📊", "Sales Brief", "Generate a deal-aware briefing document using recalled memory.")
    prospect = prospect_picker()
    if prospect and st.button("Generate Brief", type="primary"):
        with st.spinner("Recalling memories and generating brief…"):
            result = api_get(f"/prospects/{prospect['id']}/brief")
        memory_badge(result["memory_mode"])
        source_badge(result.get("memory_source"), result.get("memory_warning"))
        section("Recalled Memories")
        show_memory_items(result["recalled_memories"])
        section("Generated Brief")
        st.markdown(result["content"])


def followup_page() -> None:
    page_header("✉️", "Follow-up Email", "See how memory transforms a generic template into a personalised message.")
    prospect = prospect_picker()
    if prospect and st.button("Generate Follow-up", type="primary"):
        with st.spinner("Personalising from recalled history…"):
            result = api_get(f"/prospects/{prospect['id']}/followup")
        memory_badge(result["memory_mode"])
        source_badge(result.get("memory_source"), result.get("memory_warning"))

        generic = _generic_email(result["prospect"]["company"])
        left, right = st.columns(2, gap="large")
        with left:
            st.markdown('<span class="compare-header compare-bad">Without Memory</span>', unsafe_allow_html=True)
            st.code(generic, language="markdown")
        with right:
            st.markdown('<span class="compare-header compare-good">With Hindsight Memory</span>', unsafe_allow_html=True)
            st.code(result["content"], language="markdown")

        section("Memory Used")
        show_memory_items(result["recalled_memories"])


def before_after_page() -> None:
    page_header("🔬", "Before vs After Demo", "Side-by-side contrast — generic assistant vs memory-aware agent.")
    prospect = prospect_picker()
    if prospect and st.button("Run Comparison", type="primary"):
        result = api_get(f"/demo/before-after/{prospect['id']}")
        memory_badge(result["memory_mode"])
        source_badge(result.get("memory_source"), result.get("memory_warning"))

        left, right = st.columns(2, gap="large")
        with left:
            st.markdown('<span class="compare-header compare-bad">Without Memory</span>', unsafe_allow_html=True)
            st.code(result["without_memory"], language="markdown")
        with right:
            st.markdown('<span class="compare-header compare-good">With Hindsight Memory</span>', unsafe_allow_html=True)
            st.code(result["with_hindsight_memory"], language="markdown")

        section("Recall Activity")
        show_memory_items(result["recalled_memories"])


def inspector_page() -> None:
    page_header("🔍", "Memory Inspector", "Browse retained and recalled memory items by prospect or globally.")
    prospect = prospect_picker("Filter by prospect")
    if prospect:
        result = api_get(f"/prospects/{prospect['id']}/memory")
        source_badge(result.get("memory_source"), result.get("memory_warning"))
        section("Recalled Memories")
        show_memory_items(result.get("recalled_memories", []))
        activities = result.get("activity", [])
    else:
        activities = api_get("/memory")

    if not activities:
        st.info("No memory activity yet.")
        return

    section("Activity Log")
    for item in activities:
        op = item["operation"].lower()
        op_cls = {"retain": "op-retain", "recall": "op-recall", "reflect": "op-reflect"}.get(op, "op-other")
        with st.expander(f"{item['operation'].upper()}  ·  {item['company']}  ·  {item['created_at']}"):
            c1, c2 = st.columns(2)
            c1.write(f"**Prospect:** {item['prospect_name']}")
            c1.write(f"**Company:** {item['company']}")
            c1.write(f"**Deal ID:** {item['deal_id']}")
            c2.write(f"**Provider:** {item['provider']}")
            c2.write(f"**Fallback mode:** {item['fallback_mode']}")
            st.markdown(tags_html(item.get("tags", [])), unsafe_allow_html=True)
            st.write("**Content sent / query**")
            st.text(item["content"])
            st.write("**Provider result**")
            st.text(item["result"])


# ── Utilities ─────────────────────────────────────────────────────────────────

def _generic_email(company: str) -> str:
    return (
        f"Subject: Following up on our conversation\n\n"
        f"Hi there,\n\n"
        f"Thanks for taking the time to speak with us about {company}. "
        f"I wanted to follow up and see whether you had any questions about our solution. "
        f"We would be happy to schedule a demo and discuss next steps at your convenience.\n\n"
        f"Best regards,\nSales Team"
    )


def seed_button() -> None:
    if st.sidebar.button("🌱  Seed Demo Data", use_container_width=True):
        try:
            result = api_post("/seed")
            st.sidebar.success(f"✓ Seeded {result['created_interactions']} interactions.")
        except requests.RequestException as exc:
            st.sidebar.error(f"Seed failed: {exc}")


# ── Navigation ────────────────────────────────────────────────────────────────

PAGES = {
    "Dashboard":          dashboard_page,
    "Log Interaction":    log_interaction_page,
    "Sales Brief":        sales_brief_page,
    "Follow-up Email":    followup_page,
    "Before vs After":    before_after_page,
    "Memory Inspector":   inspector_page,
}

NAV_ITEMS = [
    ("Dashboard",        "📊", "Overview & stats"),
    ("Log Interaction",  "📝", "Record a meeting"),
    ("Sales Brief",      "📄", "Generate briefing"),
    ("Follow-up Email",  "✉️",  "Write personalised email"),
    ("Before vs After",  "⚡", "Compare with/without memory"),
    ("Memory Inspector", "🔍", "Browse memory store"),
]

# ── Sidebar brand ──
st.sidebar.markdown(
    """
    <div style="padding: 20px 16px 4px;">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
        <div style="width:34px;height:34px;background:#eff6ff;border-radius:9px;
                    display:flex;align-items:center;justify-content:center;font-size:17px;">🧠</div>
        <div>
          <div style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;
                      font-size:.95rem;color:#111827;letter-spacing:-.3px;">Sales Memory</div>
          <div style="font-size:.68rem;color:#9ca3af;letter-spacing:.02em;">Powered by Hindsight</div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown('<div class="nav-divider"></div>', unsafe_allow_html=True)

# ── Hidden real radio (drives state) ──
page = st.sidebar.radio("Navigation", list(PAGES.keys()), label_visibility="collapsed")

# ── Visual nav items ──
st.sidebar.markdown('<div class="nav-group-label">Main Menu</div>', unsafe_allow_html=True)

for key, icon, desc in NAV_ITEMS:
    is_active = page == key
    active_cls = " active" if is_active else ""
    st.sidebar.markdown(
        f"""
        <div class="nav-item{active_cls}">
          <div class="nav-icon">{icon}</div>
          <div class="nav-label">{key}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.sidebar.markdown('<div class="nav-divider" style="margin-top:12px;"></div>', unsafe_allow_html=True)

# ── Seed button ──
st.sidebar.markdown('<div class="nav-group-label">Tools</div>', unsafe_allow_html=True)
seed_button()

# ── Footer ──
st.sidebar.markdown(
    f"""
    <div style="padding: 14px 16px 8px; margin-top: 8px;">
      <div style="font-size:.7rem;color:#9ca3af;">Backend endpoint</div>
      <div class="backend-badge"><span class="status-live"></span>{API_URL}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

PAGES[page]()