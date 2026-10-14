"""
CampusPass - UI Components and Styles
Provides design system tokens, custom dark theme CSS, badges, and layout helpers.
"""

from typing import Any
import streamlit as st

CUSTOM_CSS = """
<style>
/* -------------------------------------------------------------
   CampusPass Design System - Modern Dark & Emerald Aesthetic
------------------------------------------------------------- */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg-main: #0B0E14;
    --bg-surface: #131722;
    --bg-card: #181D2A;
    --bg-card-hover: #1E2435;
    --border-subtle: #262D3D;
    --border-light: #323B4E;
    --text-primary: #F3F4F6;
    --text-secondary: #9CA3AF;
    --text-muted: #6B7280;
    --emerald-primary: #10B981;
    --emerald-hover: #059669;
    --emerald-subtle: rgba(16, 185, 129, 0.12);
    --emerald-border: rgba(16, 185, 129, 0.3);
    --amber-subtle: rgba(245, 158, 11, 0.12);
    --amber-text: #FBBF24;
    --rose-subtle: rgba(244, 63, 94, 0.12);
    --rose-text: #FB7185;
    --blue-subtle: rgba(59, 130, 246, 0.12);
    --blue-text: #60A5FA;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text-primary);
}

/* App Background */
.stApp {
    background-color: var(--bg-main);
}

/* Streamlit Header & Toolbar adjustment */
header[data-testid="stHeader"] {
    background-color: rgba(11, 14, 20, 0.85);
    backdrop-filter: blur(8px);
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: var(--bg-surface);
    border-right: 1px solid var(--border-subtle);
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Custom Card Container */
.cp-card {
    background-color: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1rem;
    transition: all 0.2s ease-in-out;
}

.cp-card:hover {
    border-color: var(--border-light);
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.4);
}

.cp-card-featured {
    border-top: 3px solid var(--emerald-primary);
}

/* Status Badges */
.cp-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.25rem 0.65rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.025em;
    text-transform: uppercase;
}

.cp-badge-emerald {
    background-color: var(--emerald-subtle);
    color: #34D399;
    border: 1px solid var(--emerald-border);
}

.cp-badge-amber {
    background-color: var(--amber-subtle);
    color: var(--amber-text);
    border: 1px solid rgba(245, 158, 11, 0.3);
}

.cp-badge-rose {
    background-color: var(--rose-subtle);
    color: var(--rose-text);
    border: 1px solid rgba(244, 63, 94, 0.3);
}

.cp-badge-blue {
    background-color: var(--blue-subtle);
    color: var(--blue-text);
    border: 1px solid rgba(59, 130, 246, 0.3);
}

.cp-badge-muted {
    background-color: rgba(107, 114, 128, 0.15);
    color: var(--text-secondary);
    border: 1px solid var(--border-subtle);
}

/* Metric Stats Widget */
.cp-stat-box {
    background-color: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 1rem 1.15rem;
    display: flex;
    flex-direction: column;
}

.cp-stat-label {
    font-size: 0.8rem;
    color: var(--text-secondary);
    font-weight: 500;
    margin-bottom: 0.25rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.cp-stat-value {
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.2;
}

.cp-stat-hint {
    font-size: 0.75rem;
    color: var(--emerald-primary);
    margin-top: 0.35rem;
}

/* Ticket Physical Card Aesthetic */
.cp-ticket-wrapper {
    background: linear-gradient(145deg, #181D2A 0%, #131722 100%);
    border: 1px solid var(--border-subtle);
    border-radius: 14px;
    overflow: hidden;
    position: relative;
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
    margin-bottom: 1.5rem;
}

.cp-ticket-header {
    background-color: rgba(16, 185, 129, 0.08);
    border-bottom: 1px dashed var(--border-light);
    padding: 1rem 1.25rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.cp-ticket-code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    font-weight: 600;
    color: #34D399;
    letter-spacing: 0.08em;
}

/* Coming Soon Pill */
.cp-coming-soon {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    font-size: 0.7rem;
    color: #9CA3AF;
    background: rgba(255, 255, 255, 0.06);
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    font-weight: 500;
}

/* Custom button overrides */
div.stButton > button:first-child {
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.875rem;
    transition: all 0.2s ease;
    border: 1px solid var(--border-subtle);
}

div.stButton > button[kind="primary"] {
    background-color: var(--emerald-primary);
    color: #064E3B;
    border-color: var(--emerald-primary);
}

div.stButton > button[kind="primary"]:hover {
    background-color: var(--emerald-hover);
    color: #FFFFFF;
    border-color: var(--emerald-hover);
}

/* Clean Form inputs */
div[data-baseweb="input"] {
    background-color: var(--bg-surface) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
}

div[data-baseweb="select"] {
    background-color: var(--bg-surface) !important;
    border-radius: 8px !important;
}

/* Tab headers */
button[data-baseweb="tab"] {
    font-weight: 600;
    color: var(--text-secondary);
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--emerald-primary) !important;
    border-bottom-color: var(--emerald-primary) !important;
}

/* Clean Divider */
hr {
    border-color: var(--border-subtle);
    margin: 1.5rem 0;
}
</style>
"""

def inject_custom_css():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def render_badge(text: str, badge_type: str = "emerald") -> str:
    return f'<span class="cp-badge cp-badge-{badge_type}">{text}</span>'

def render_stat_box(label: str, value: Any, hint: str = ""):
    hint_html = f'<div class="cp-stat-hint">{hint}</div>' if hint else ""
    html = f"""
    <div class="cp-stat-box">
        <div class="cp-stat-label">{label}</div>
        <div class="cp-stat-value">{value}</div>
        {hint_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_coming_soon(feature_name: str = "Feature"):
    html = f"""
    <span class="cp-coming-soon" title="Planned for subsequent release phase">
        ⚡ {feature_name} (Coming soon)
    </span>
    """
    return html

def render_page_header(title: str, subtitle: str = "", tag: str = ""):
    if tag:
        st.markdown(
            f"<div style='font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; color: var(--emerald-primary, #10B981); text-transform: uppercase; margin-bottom: 0.25rem;'>{tag}</div>",
            unsafe_allow_html=True
        )
    st.markdown(f"## {title}")
    if subtitle:
        st.caption(subtitle)
    st.markdown("---")

