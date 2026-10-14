"""
CampusPass - Manage Events Page
Allows organizers to create events, edit details/capacity, publish/unpublish, cancel, and export attendee rosters.
"""

from datetime import date, datetime, timedelta
import streamlit as st
import pandas as pd
from services.event_service import create_event, update_event, toggle_publish_status, cancel_event, get_event_by_id
from services.attendance_service import get_event_attendees
from utils.ui_components import render_page_header, render_badge, render_coming_soon
from data.mock_data import CATEGORIES

def render_manage_events_page():
    render_page_header(
        title="Event Operations & Roster Management",
        subtitle="Create campus listings, modify schedules, set seat quotas, and export attendee records.",
        tag="CAMPUSPASS · ORGANIZER TOOLS"
    )

    events = st.session_state.get("events", [])
    bookings = st.session_state.get("bookings", [])
    current_organizer = st.session_state.get("current_organizer", {})

    tab_create, tab_edit, tab_roster = st.tabs([
        "➕ Create New Event",
        "✏️ Edit & Manage Existing Listings",
        "👥 Attendee Roster & CSV Export"
    ])

    # ---------------- TAB 1: CREATE EVENT ----------------
    with tab_create:
        st.markdown("#### Create a New Campus Event Listing")
        st.caption("Fill in the event logistics below. Free student passes will be made available upon creation.")

        with st.form("create_event_form", clear_on_submit=True):
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                title = st.text_input("Event Title *", placeholder="e.g. Next-Gen Web3 & Blockchain Summit")
                category = st.selectbox("Category *", [c for c in CATEGORIES if c != "All"], index=0)
                venue = st.text_input("Campus Venue *", placeholder="e.g. Dr. A.P.J. Abdul Kalam Convention Centre")
                capacity = st.number_input("Seat Capacity *", min_value=1, max_value=2000, value=60, step=5)

            with f_col2:
                default_date = date.today() + timedelta(days=14)
                event_date = st.date_input("Event Date *", value=default_date)
                event_time = st.text_input("Time / Duration *", value="02:00 PM - 05:00 PM", placeholder="e.g. 10:00 AM - 01:00 PM")
                deadline = st.date_input("Registration Deadline *", value=default_date - timedelta(days=1))
                organizer_club = st.text_input("Host Club / Society *", value=current_organizer.get("name", "Campus Tech Council"))

            description = st.text_area(
                "Event Description & Agenda *",
                placeholder="Provide a compelling description of what students will learn, keynote speakers, prerequisite tools, and rewards.",
                height=120
            )

            color_accent = st.selectbox(
                "Card Accent Color",
                options=["#10B981 (Emerald)", "#3B82F6 (Blue)", "#8B5CF6 (Purple)", "#EC4899 (Pink)", "#F59E0B (Amber)", "#14B8A6 (Teal)"],
                index=0
            ).split(" ")[0]

            is_published = st.checkbox("Publish immediately to Discover Events", value=True)

            submitted = st.form_submit_button("🚀 Publish Event Listing", type="primary", use_container_width=True)

            if submitted:
                if not title.strip() or not description.strip() or not venue.strip():
                    st.error("Please fill in all required fields (Title, Venue, Description).")
                else:
                    new_data = {
                        "title": title.strip(),
                        "category": category,
                        "date": str(event_date),
                        "time": event_time.strip(),
                        "venue": venue.strip(),
                        "capacity": int(capacity),
                        "description": description.strip(),
                        "deadline": str(deadline),
                        "organizer": organizer_club.strip(),
                        "organizer_email": current_organizer.get("email", "council@campus.edu"),
                        "is_published": is_published,
                        "color_accent": color_accent,
                        "tags": [category, "Free Pass"]
                    }
                    success, msg, _ = create_event(events, new_data)
                    if success:
                        st.toast(msg, icon="🎉")
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

    # ---------------- TAB 2: EDIT & MANAGE ----------------
    with tab_edit:
        st.markdown("#### Modify Existing Event Parameters")
        if not events:
            st.warning("No events available to edit.")
        else:
            event_options = {e["id"]: f"{e['title']} ({e['id']}) - {e.get('booked_count', 0)}/{e.get('capacity', 0)} Booked" for e in events}
            selected_id = st.selectbox("Select Event to Modify", options=list(event_options.keys()), format_func=lambda x: event_options[x])

            cur_event = get_event_by_id(events, selected_id)
            if cur_event:
                st.markdown(f"**Current Status:** {'🟢 Published' if cur_event.get('is_published') else '⚪ Draft/Unlisted'} &bull; **Lifecycle:** {cur_event.get('status')}")

                # Quick Actions: Publish Toggle and Cancel
                act_col1, act_col2, _ = st.columns([1, 1, 1.5])
                with act_col1:
                    pub_label = "👁️ Unpublish Listing" if cur_event.get("is_published") else "🌐 Publish Listing"
                    if st.button(pub_label, key=f"toggle_pub_{cur_event['id']}", use_container_width=True):
                        ok, m = toggle_publish_status(events, cur_event["id"])
                        if ok:
                            st.toast(m)
                            st.rerun()
                with act_col2:
                    if cur_event.get("status") != "Cancelled":
                        if st.button("🚫 Cancel Event", key=f"cancel_evt_{cur_event['id']}", use_container_width=True):
                            ok, m = cancel_event(events, cur_event["id"])
                            if ok:
                                st.toast(m, icon="⚠️")
                                st.rerun()

                st.markdown("---")
                with st.form(f"edit_event_form_{cur_event['id']}"):
                    e_col1, e_col2 = st.columns(2)
                    with e_col1:
                        new_title = st.text_input("Title", value=cur_event.get("title"))
                        cat_list = [c for c in CATEGORIES if c != "All"]
                        cat_idx = cat_list.index(cur_event.get("category")) if cur_event.get("category") in cat_list else 0
                        new_category = st.selectbox("Category", cat_list, index=cat_idx)
                        new_venue = st.text_input("Venue", value=cur_event.get("venue"))

                    with e_col2:
                        cur_booked = cur_event.get("booked_count", 0)
                        new_capacity = st.number_input(
                            f"Capacity (Minimum {cur_booked} due to active passes)",
                            min_value=max(1, cur_booked),
                            max_value=3000,
                            value=max(cur_event.get("capacity", 50), cur_booked),
                            step=5,
                            help=f"Cannot reduce capacity below currently booked seats ({cur_booked})."
                        )
                        new_date = st.text_input("Date (YYYY-MM-DD)", value=cur_event.get("date"))
                        new_time = st.text_input("Time", value=cur_event.get("time"))

                    new_desc = st.text_area("Description", value=cur_event.get("description"), height=100)
                    new_deadline = st.text_input("Registration Deadline", value=cur_event.get("deadline"))

                    save_btn = st.form_submit_button("💾 Save Changes", type="primary")

                    if save_btn:
                        updated_fields = {
                            "title": new_title.strip(),
                            "category": new_category,
                            "venue": new_venue.strip(),
                            "capacity": int(new_capacity),
                            "date": new_date.strip(),
                            "time": new_time.strip(),
                            "description": new_desc.strip(),
                            "deadline": new_deadline.strip()
                        }
                        ok, msg = update_event(events, cur_event["id"], updated_fields)
                        if ok:
                            st.toast(msg, icon="✅")
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)

    # ---------------- TAB 3: ATTENDEE ROSTER & CSV ----------------
    with tab_roster:
        st.markdown("#### Attendee Roster & Gate List")
        if not events:
            st.info("No events to display.")
        else:
            evt_selector = st.selectbox(
                "Choose Event to View Roster & Export",
                options=[e["id"] for e in events],
                format_func=lambda x: f"{next((e['title'] for e in events if e['id'] == x), x)} ({x})",
                key="roster_event_selector"
            )

            matched_event = get_event_by_id(events, evt_selector)
            attendees = get_event_attendees(bookings, evt_selector)

            if matched_event:
                confirmed_att = [a for a in attendees if a.get("status") == "Confirmed"]
                checked_in_att = [a for a in confirmed_att if a.get("attendance") == "Checked-in"]

                r_col1, r_col2, r_col3 = st.columns([1, 1, 1.5])
                with r_col1:
                    st.metric("Total Booked", f"{len(confirmed_att)} / {matched_event.get('capacity')}")
                with r_col2:
                    st.metric("Checked-in at Gate", f"{len(checked_in_att)}")
                with r_col3:
                    turnout = (len(checked_in_att) / len(confirmed_att) * 100) if confirmed_att else 0
                    st.metric("Check-in Rate", f"{turnout:.1f}%")

                if confirmed_att:
                    roster_data = []
                    for a in confirmed_att:
                        roster_data.append({
                            "Ticket ID": a.get("ticket_id"),
                            "Student Name": a.get("student_name"),
                            "Email": a.get("student_email"),
                            "Booking Status": a.get("status"),
                            "Attendance": a.get("attendance"),
                            "Check-in Time": a.get("checkin_time") or "Pending",
                            "Security Credential": a.get("ticket_credential")
                        })

                    df_roster = pd.DataFrame(roster_data)
                    st.dataframe(df_roster, use_container_width=True, hide_index=True)

                    # CSV Export button
                    csv_bytes = df_roster.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label=f"📥 Export {matched_event['title'][:20]} Attendee CSV",
                        data=csv_bytes,
                        file_name=f"CampusPass_{matched_event['id']}_attendees.csv",
                        mime="text/csv",
                        type="primary"
                    )
                else:
                    st.info(f"No confirmed registrations yet for '{matched_event['title']}'.")
