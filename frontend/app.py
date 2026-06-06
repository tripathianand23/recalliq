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

def load_css():
    with open(".streamlit/static/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


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


def html_table(df: pd.DataFrame) -> str:
    """Render a DataFrame as a clean HTML table — avoids Glide canvas color clashes."""
    rows_html = ""
    for _, row in df.iterrows():
        cells = "".join(
            f'<td style="padding:9px 14px;border-bottom:1px solid #f3f4f6;'
            f'color:#374151;font-size:.875rem;background:#ffffff;">'
            f'{val}</td>'
            for val in row
        )
        rows_html += f"<tr>{cells}</tr>"

    headers = "".join(
        f'<th style="padding:10px 14px;background:#f0f4fa;color:#4b5563;'
        f'font-size:.75rem;font-weight:700;text-transform:uppercase;'
        f'letter-spacing:.06em;border-bottom:2px solid #e2e6ef;'
        f'white-space:nowrap;">{col}</th>'
        for col in df.columns
    )

    return (
        f'<div style="border:1px solid #e2e6ef;border-radius:10px;overflow:hidden;'
        f'box-shadow:0 1px 3px rgba(0,0,0,.07);margin-bottom:.5rem;">'
        f'<table style="width:100%;border-collapse:collapse;background:#ffffff;">'
        f'<thead><tr>{headers}</tr></thead>'
        f'<tbody>{rows_html}</tbody>'
        f'</table></div>'
    )


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
    if st.sidebar.button("🌱  Seed Demo Data", use_container_width=True, key="seed_btn"):
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
    ("Dashboard",        "📊"),
    ("Log Interaction",  "📝"),
    ("Sales Brief",      "📄"),
    ("Follow-up Email",  "✉️"),
    ("Before vs After",  "⚡"),
    ("Memory Inspector", "🔍"),
]

if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

st.sidebar.markdown(
    """
    <div style="padding:20px 4px 8px;">
      <div style="display:flex;align-items:center;gap:10px;">
        <div style="width:36px;height:36px;background:#eff6ff;border-radius:10px;
                    display:flex;align-items:center;justify-content:center;font-size:18px;
                    flex-shrink:0;">🧠</div>
        <div>
          <div style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;
                      font-size:.97rem;color:#111827;letter-spacing:-.3px;line-height:1.2;">
            Sales Memory</div>
          <div style="font-size:.68rem;color:#9ca3af;margin-top:1px;">
            Powered by Hindsight</div>
        </div>
      </div>
    </div>
    <div class="nav-divider"></div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown('<div class="nav-group-label">Main Menu</div>', unsafe_allow_html=True)

for key, icon in NAV_ITEMS:
    is_active = st.session_state.current_page == key
    btn_type = "primary" if is_active else "secondary"
    label = f"{icon}  {key}"
    if st.sidebar.button(
        label,
        key=f"nav_{key}",
        use_container_width=True,
        type=btn_type,
    ):
        st.session_state.current_page = key
        st.rerun()

st.sidebar.markdown('<div class="nav-divider" style="margin-top:8px;"></div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="nav-group-label">Tools</div>', unsafe_allow_html=True)
seed_button()

st.sidebar.markdown(
    f"""
    <div style="padding:14px 4px 8px;margin-top:4px;">
      <div style="font-size:.68rem;color:#9ca3af;margin-bottom:4px;">Backend endpoint</div>
      <div class="backend-badge"><span class="status-live"></span>{API_URL}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

PAGES[st.session_state.current_page]()
