"""
CampusPass - Discover Events Page
Main student exploration page for browsing, searching, viewing details, and booking free tickets.
"""

import streamlit as st
from services.event_service import filter_events, get_event_by_id
from services.booking_service import book_event, join_waitlist
from utils.ui_components import render_page_header
from data.mock_data import CATEGORIES

def render_discover_page():
    render_page_header(
        title="Discover Campus Events",
        subtitle="Browse upcoming college events, workshops, and hackathons with free passes."
    )

    events = st.session_state.get("events", [])
    bookings = st.session_state.get("bookings", [])
    waitlist = st.session_state.get("waitlist", [])
    current_student = st.session_state.get("current_student", {})

    # Simple Search & Filter Controls
    filter_col1, filter_col2, filter_col3 = st.columns([2, 1.2, 1])
    with filter_col1:
        search_query = st.text_input(
            "Search events",
            placeholder="Search by title, keyword, or venue...",
            key="search_events_input",
            label_visibility="collapsed"
        )
    with filter_col2:
        selected_category = st.selectbox(
            "Category",
            options=CATEGORIES,
            index=0,
            key="category_filter_select",
            label_visibility="collapsed"
        )
    with filter_col3:
        availability_filter = st.selectbox(
            "Availability",
            options=["All", "Open Only", "Full / Waitlist Only"],
            index=0,
            key="availability_filter_select",
            label_visibility="collapsed"
        )

    # Filtered Events
    filtered = filter_events(events, search_query, selected_category, availability_filter)

    st.caption(f"Showing **{len(filtered)}** events")

    if not filtered:
        st.info("No campus events matched your search filters.")
        return

    # Render Event Cards in 2 Columns
    col_left, col_right = st.columns(2)
    columns_list = [col_left, col_right]

    for idx, event in enumerate(filtered):
        target_col = columns_list[idx % 2]
        capacity = event.get("capacity", 0)
        booked = event.get("booked_count", 0)
        available = max(0, capacity - booked)
        is_full = available == 0

        # Check booking status for current student
        student_id = current_student.get("student_id")
        already_booked = any(b["event_id"] == event["id"] and b["student_id"] == student_id and b["status"] == "Confirmed" for b in bookings)
        already_waitlisted = any(w["event_id"] == event["id"] and w["student_id"] == student_id for w in waitlist)

        with target_col:
            with st.container(border=True):
                # Header tag
                status_tag = "🟢 Open" if not is_full else "⏳ Waitlist"
                st.caption(f"{event.get('category')} · {status_tag} · Free Pass")

                # Event Title
                st.markdown(f"### {event.get('title')}")

                # Description snippet
                st.write(event.get('description', '')[:120] + "...")

                # Schedule and venue
                st.caption(f"📅 **{event.get('date')}** ({event.get('time')}) · 📍 {event.get('venue')}")

                # Seats count
                if available > 0:
                    st.write(f"Seats available: **{available}** / {capacity}")
                else:
                    st.write(f"Seats available: **0** / {capacity} *(Full)*")

                # Actions
                btn_col1, btn_col2 = st.columns([1, 1.2])

                with btn_col1:
                    with st.popover("Details", use_container_width=True):
                        st.markdown(f"#### {event.get('title')}")
                        st.caption(f"Organized by: **{event.get('organizer')}**")
                        st.markdown("---")
                        st.write(event.get('description'))
                        st.markdown(f"- **Date & Time:** {event.get('date')} ({event.get('time')})")
                        st.markdown(f"- **Venue:** {event.get('venue')}")
                        st.markdown(f"- **Capacity:** {event.get('capacity')} attendees")
                        st.markdown(f"- **Deadline:** {event.get('deadline')}")

                with btn_col2:
                    if already_booked:
                        st.button("✅ Booked", key=f"booked_btn_{event['id']}", disabled=True, use_container_width=True)
                    elif not is_full:
                        if st.button("🎟️ Book Pass", key=f"book_btn_{event['id']}", type="primary", use_container_width=True):
                            success, msg, new_ticket = book_event(events, bookings, waitlist, event["id"], current_student)
                            if success:
                                st.toast(f"Pass booked! ID: {new_ticket['ticket_id']}", icon="🎫")
                                st.rerun()
                            else:
                                st.error(msg)
                    else:
                        if already_waitlisted:
                            wl_entry = next((w for w in waitlist if w["event_id"] == event["id"] and w["student_id"] == student_id), None)
                            pos = wl_entry.get("queue_position", 1) if wl_entry else 1
                            st.button(f"⏳ Waitlisted (#{pos})", key=f"wl_btn_{event['id']}", disabled=True, use_container_width=True)
                        else:
                            if st.button("⏳ Join Waitlist", key=f"join_wl_{event['id']}", use_container_width=True):
                                success, msg, _ = join_waitlist(events, bookings, waitlist, event["id"], current_student)
                                if success:
                                    st.toast(msg, icon="⏳")
                                    st.rerun()
                                else:
                                    st.error(msg)
