"""
CampusPass - My Tickets Page
Displays student's booked passes, scannable QR ticket badges, download options, and cancellation.
"""

import streamlit as st
from services.booking_service import get_student_bookings, cancel_booking, get_student_waitlist_entries, leave_waitlist
from services.event_service import get_event_by_id
from utils.qr_utils import get_qr_image_bytes
from utils.ui_components import render_page_header

def render_tickets_page():
    render_page_header(
        title="My Campus Passes",
        subtitle="View your passes, show QR credentials at event gates, or cancel reservations."
    )

    events = st.session_state.get("events", [])
    bookings = st.session_state.get("bookings", [])
    waitlist = st.session_state.get("waitlist", [])
    current_student = st.session_state.get("current_student", {})
    student_id = current_student.get("student_id")

    my_bookings = get_student_bookings(bookings, student_id)
    my_waitlist = get_student_waitlist_entries(waitlist, student_id)

    tab_active, tab_waitlist, tab_history = st.tabs([
        f"🎟️ Active Passes ({len([b for b in my_bookings if b.get('status') == 'Confirmed'])})",
        f"⏳ Waitlist ({len(my_waitlist)})",
        f"📜 Cancelled ({len([b for b in my_bookings if b.get('status') == 'Cancelled'])})"
    ])

    with tab_active:
        active_tickets = [b for b in my_bookings if b.get("status") == "Confirmed"]
        if not active_tickets:
            st.info("You don't have any active passes yet. Go to **Discover Events** to book a pass.")
        else:
            for b in active_tickets:
                event = get_event_by_id(events, b.get("event_id"))
                event_date = event.get("date", "") if event else ""
                event_time = event.get("time", "") if event else ""
                event_venue = event.get("venue", "") if event else ""
                is_checked_in = b.get("attendance") == "Checked-in"

                with st.container(border=True):
                    c_info, c_qr = st.columns([2.2, 1])

                    with c_info:
                        status_str = "✅ Checked-in" if is_checked_in else "🟢 Valid Pass"
                        st.caption(f"{event.get('category', 'Event') if event else 'Event'} · {status_str} · Pass ID: `{b.get('ticket_id')}`")
                        st.markdown(f"### {b.get('event_title')}")
                        st.markdown(f"📅 **{event_date}** ({event_time})  \n📍 **Venue:** {event_venue}")
                        st.caption(f"Attendee: **{b.get('student_name')}** ({b.get('student_email')})")
                        st.caption(f"Security Credential: `{b.get('ticket_credential')}`")

                    with c_qr:
                        qr_payload = b.get("qr_payload", b.get("ticket_credential", "CAMPUSPASS"))
                        qr_bytes = get_qr_image_bytes(qr_payload)
                        st.image(qr_bytes, width=150)

                        st.download_button(
                            label="📥 Download QR",
                            data=qr_bytes,
                            file_name=f"Pass_{b['ticket_id']}.png",
                            mime="image/png",
                            key=f"dl_qr_{b['ticket_id']}",
                            use_container_width=True
                        )

                        if not is_checked_in:
                            with st.popover("Cancel Pass", use_container_width=True):
                                st.write("Cancel this reservation and release the seat?")
                                if st.button("Confirm", key=f"confirm_cancel_{b['ticket_id']}", type="primary"):
                                    ok, msg, promo = cancel_booking(events, bookings, waitlist, b["ticket_id"], student_id)
                                    if ok:
                                        st.toast(msg, icon="🗑️")
                                        st.rerun()
                                    else:
                                        st.error(msg)

    with tab_waitlist:
        if not my_waitlist:
            st.info("You are not currently in any event waitlists.")
        else:
            for w in my_waitlist:
                event = get_event_by_id(events, w.get("event_id"))
                event_title = event.get("title") if event else "Campus Event"
                pos = w.get("queue_position", 1)

                with st.container(border=True):
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.caption(f"Waitlist · Queue Position **#{pos}**")
                        st.markdown(f"#### {event_title}")
                        st.caption(f"Joined on: {w.get('joined_time')}")
                    with c2:
                        if st.button("Leave Queue", key=f"leave_wl_{w['waitlist_id']}", use_container_width=True):
                            ok, msg = leave_waitlist(waitlist, w["event_id"], student_id)
                            if ok:
                                st.toast(msg)
                                st.rerun()
                            else:
                                st.error(msg)

    with tab_history:
        past_tickets = [b for b in my_bookings if b.get("status") == "Cancelled"]
        if not past_tickets:
            st.caption("No cancelled bookings.")
        else:
            for b in past_tickets:
                with st.container(border=True):
                    st.caption(f"Cancelled Pass · ID: `{b.get('ticket_id')}`")
                    st.markdown(f"**{b.get('event_title')}**")
                    st.caption(f"Booked on: {b.get('booking_time')}")
