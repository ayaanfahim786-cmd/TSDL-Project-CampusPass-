"""
CampusPass - Attendance Check-in Page
Organizer gate entry desk for verifying student ticket credentials, check-in validation, and live attendance logs.
"""

import streamlit as st
import pandas as pd
from services.attendance_service import verify_and_checkin, get_event_attendees
from services.event_service import get_event_by_id
from utils.ui_components import render_page_header, render_badge, render_coming_soon

def render_checkin_page():
    render_page_header(
        title="Gate Attendance & Ticket Scanner",
        subtitle="Validate student passes, check in attendees in real time, and monitor entrance queue volume.",
        tag="CAMPUSPASS · GATE ENTRY CONSOLE"
    )

    events = st.session_state.get("events", [])
    bookings = st.session_state.get("bookings", [])

    if not events:
        st.warning("No events available in the system.")
        return

    # Event Selector Dropdown
    event_choices = {e["id"]: f"{e['title']} ({e['id']}) - {e.get('venue')}" for e in events}
    selected_event_id = st.selectbox(
        "🎯 Select Current Gate / Event Session",
        options=list(event_choices.keys()),
        format_func=lambda x: event_choices[x],
        key="checkin_event_selector"
    )

    target_event = get_event_by_id(events, selected_event_id)
    attendees = get_event_attendees(bookings, selected_event_id)
    confirmed_attendees = [a for a in attendees if a.get("status") == "Confirmed"]
    checked_in_count = len([a for a in confirmed_attendees if a.get("attendance") == "Checked-in"])
    total_booked = len(confirmed_attendees)

    # Gate Stats
    s1, s2, s3 = st.columns(3)
    with s1:
        st.metric("Total Passholders", f"{total_booked}")
    with s2:
        st.metric("Checked-in at Gate", f"{checked_in_count}", f"{(checked_in_count/total_booked*100):.0f}% turnout" if total_booked > 0 else "0%")
    with s3:
        st.metric("Pending Arrival", f"{max(0, total_booked - checked_in_count)}")

    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)

    # Verification Section
    left_col, right_col = st.columns([1.6, 1.2])

    with left_col:
        st.markdown("#### 🎫 Manual Pass Credential Verification")
        st.caption("Enter the student's Ticket ID (e.g. `CP-2026-A101`) or the Security Credential (e.g. `SEC-CP101-7F4A2B`):")

        # Input form
        with st.form("manual_checkin_form", clear_on_submit=False):
            code_input = st.text_input(
                "Pass ID or Security Credential",
                placeholder="e.g. CP-2026-A101 or SEC-CP101-7F4A2B",
                key="code_entry_field"
            )
            verify_btn = st.form_submit_button("🔍 Verify & Admit Attendee", type="primary", use_container_width=True)

            if verify_btn:
                success, msg, matched_booking, status_code = verify_and_checkin(
                    bookings, events, selected_event_id, code_input
                )

                if status_code == "SUCCESS":
                    st.success(msg)
                    st.balloons()
                    st.toast(f"✅ Admitted: {matched_booking['student_name']}", icon="🎉")
                    st.rerun()
                elif status_code == "ALREADY_CHECKED_IN":
                    st.warning(msg)
                    if matched_booking:
                        st.caption(f"Original check-in time: **{matched_booking.get('checkin_time')}**")
                elif status_code == "WRONG_EVENT":
                    st.error(msg)
                elif status_code == "CANCELLED":
                    st.error(msg)
                else:
                    st.error(msg)

        # Quick Demo Helper with Sample Codes for this Event
        if confirmed_attendees:
            with st.expander("💡 Quick Test Helper (Sample Pass IDs for this Event)", expanded=False):
                st.caption("Click to copy any of the following valid passes for demonstration:")
                for demo_b in confirmed_attendees[:5]:
                    status_emoji = "✅" if demo_b.get("attendance") == "Checked-in" else "⏳"
                    st.markdown(f"- **{demo_b.get('student_name')}**: ID ` {demo_b.get('ticket_id')} ` &bull; Credential ` {demo_b.get('ticket_credential')} ` ({status_emoji} {demo_b.get('attendance')})")

    with right_col:
        st.markdown("#### 📷 Optical QR Scanner")
        with st.container(border=True):
            st.caption("Hardware Webcam Scanner")
            st.info("⚡ Webcam scanning is in development. Use the manual pass verification on the left.")

    # Live Gate Log Table
    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
    st.markdown("#### 📋 Live Gate Roster for Current Session")

    if confirmed_attendees:
        log_rows = []
        for a in confirmed_attendees:
            is_in = a.get("attendance") == "Checked-in"
            log_rows.append({
                "Ticket ID": a.get("ticket_id"),
                "Student": a.get("student_name"),
                "Email": a.get("student_email"),
                "Gate Status": "✅ Checked In" if is_in else "⏳ Awaiting Entry",
                "Timestamp": a.get("checkin_time") or "—",
                "Pass Key": a.get("ticket_credential")
            })

        df_log = pd.DataFrame(log_rows)
        st.dataframe(df_log, use_container_width=True, hide_index=True)
    else:
        st.info("No active passholders registered for this event yet.")
