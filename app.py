"""
CampusPass - Campus Event Ticketing & Attendance MVP
Main Streamlit Application Entrypoint
"""

import os
import streamlit as st
from data.mock_data import (
    DEFAULT_STUDENT,
    DEFAULT_ORGANIZER,
    get_initial_events,
    get_initial_bookings,
    get_initial_waitlist
)
from utils.ui_components import inject_custom_css, render_badge, render_coming_soon
from pages_views.discover import render_discover_page
from pages_views.tickets import render_tickets_page
from pages_views.organizer_dashboard import render_organizer_dashboard_page
from pages_views.manage_events import render_manage_events_page
from pages_views.checkin import render_checkin_page

# ----------------- STREAMLIT CONFIG -----------------
st.set_page_config(
    page_title="CampusPass — Campus Event Ticketing",
    page_icon="🎟️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- SESSION STATE SETUP -----------------
def init_session_state():
    if "events" not in st.session_state:
        st.session_state["events"] = get_initial_events()
    if "bookings" not in st.session_state:
        st.session_state["bookings"] = get_initial_bookings()
    if "waitlist" not in st.session_state:
        st.session_state["waitlist"] = get_initial_waitlist()
    if "current_student" not in st.session_state:
        st.session_state["current_student"] = DEFAULT_STUDENT
    if "current_organizer" not in st.session_state:
        st.session_state["current_organizer"] = DEFAULT_ORGANIZER
    if "user_role" not in st.session_state:
        st.session_state["user_role"] = "Student"
    if "active_nav" not in st.session_state:
        st.session_state["active_nav"] = "Discover Events"

init_session_state()

# Inject Global Custom CSS
inject_custom_css()

# ----------------- SIDEBAR NAVIGATION -----------------
with st.sidebar:
    # Logo / Wordmark (Text)
    st.markdown("""
    <div style="font-size: 1.6rem; font-weight: 800; color: #F9FAFB; letter-spacing: -0.02em;">
        Campus<span style="color: #10B981;">Pass</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size: 0.72rem; color: #9CA3AF; margin-bottom: 1.25rem;">
        Ticketing & Attendance System &bull; <b style="color: #10B981;">v0.7 MVP</b>
    </div>
    """, unsafe_allow_html=True)

    # Demo Role Switcher
    st.write("**Active Persona**")
    selected_role = st.radio(
        "Current Active Persona",
        options=["Student", "Organizer"],
        index=0 if st.session_state["user_role"] == "Student" else 1,
        horizontal=True,
        label_visibility="collapsed"
    )

    if selected_role != st.session_state["user_role"]:
        st.session_state["user_role"] = selected_role
        if selected_role == "Student" and st.session_state["active_nav"] in ["Organizer Dashboard", "Manage Events", "Attendance Check-in"]:
            st.session_state["active_nav"] = "Discover Events"
        elif selected_role == "Organizer" and st.session_state["active_nav"] in ["Discover Events", "My Tickets"]:
            st.session_state["active_nav"] = "Organizer Dashboard"
        st.rerun()

    # Active User Profile
    if st.session_state["user_role"] == "Student":
        u = st.session_state["current_student"]
        st.caption(f"👤 **{u['name']}** · {u['roll_no']}")
    else:
        o = st.session_state["current_organizer"]
        st.caption(f"🏛️ **{o['name']}** · Tech Council")

    st.markdown("---")

    # Navigation Menu Items
    nav_options = [
        "Discover Events",
        "My Tickets",
        "Organizer Dashboard",
        "Manage Events",
        "Attendance Check-in"
    ]

    nav_icons = {
        "Discover Events": "🔍",
        "My Tickets": "🎟️",
        "Organizer Dashboard": "📊",
        "Manage Events": "✏️",
        "Attendance Check-in": "🎫"
    }

    # Ensure current selection is valid
    if st.session_state["active_nav"] not in nav_options:
        st.session_state["active_nav"] = "Discover Events"

    current_idx = nav_options.index(st.session_state["active_nav"])

    nav_selection = st.radio(
        "Application Navigation",
        options=nav_options,
        index=current_idx,
        format_func=lambda x: f"{nav_icons.get(x, '•')}  {x}",
        label_visibility="collapsed"
    )

    if nav_selection != st.session_state["active_nav"]:
        st.session_state["active_nav"] = nav_selection
        st.rerun()

    st.markdown("<hr style='margin: 1.5rem 0 1rem 0;'>", unsafe_allow_html=True)

    # Session Reset Action
    with st.expander("🛠️ Demo State Controls"):
        st.caption("Resets all in-memory mock events, tickets, and attendance back to seed state.")
        if st.button("🔄 Reset to Default Data", use_container_width=True):
            st.session_state["events"] = get_initial_events()
            st.session_state["bookings"] = get_initial_bookings()
            st.session_state["waitlist"] = get_initial_waitlist()
            st.session_state["active_nav"] = "Discover Events"
            st.toast("Mock data restored to initial state!", icon="🔄")
            st.rerun()
# ----------------- MAIN VIEW DISPATCHER -----------------
current_view = st.session_state["active_nav"]

if current_view == "Discover Events":
    render_discover_page()
elif current_view == "My Tickets":
    render_tickets_page()
elif current_view == "Organizer Dashboard":
    render_organizer_dashboard_page()
elif current_view == "Manage Events":
    render_manage_events_page()
elif current_view == "Attendance Check-in":
    render_checkin_page()
else:
    st.error(f"Unknown page route: {current_view}")
