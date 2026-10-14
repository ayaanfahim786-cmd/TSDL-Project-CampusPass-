"""
CampusPass - Attendance Service
Handles manual verification of ticket credentials, check-in timestamps, and attendee reporting.
"""

from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional
from services.event_service import get_event_by_id

def verify_and_checkin(
    bookings: List[Dict[str, Any]],
    events: List[Dict[str, Any]],
    selected_event_id: str,
    code_input: str
) -> Tuple[bool, str, Optional[Dict[str, Any]], str]:
    """
    Verifies a ticket by ID or Credential.
    Returns: (is_success, message, booking_dict, status_code)
    status_code can be: 'SUCCESS', 'ALREADY_CHECKED_IN', 'INVALID', 'WRONG_EVENT', 'CANCELLED'
    """
    clean_code = code_input.strip()
    if not clean_code:
        return False, "Please enter a Ticket ID or Security Credential.", None, "INVALID"

    # Support raw payload or credential (e.g. if extracted from QR: CAMPUSPASS:EVT-101:SEC-...:Name)
    if clean_code.startswith("CAMPUSPASS:"):
        parts = clean_code.split(":")
        if len(parts) >= 3:
            clean_code = parts[2]

    # Find the matching booking
    matched_booking = None
    for b in bookings:
        if (b.get("ticket_id", "").upper() == clean_code.upper() or 
            b.get("ticket_credential", "").upper() == clean_code.upper()):
            matched_booking = b
            break

    if not matched_booking:
        return (
            False,
            f"❌ Ticket Verification Failed: No active booking found matching '{clean_code}'. Please verify the ticket pass code.",
            None,
            "INVALID"
        )

    # Check if booking matches the selected event
    if matched_booking["event_id"] != selected_event_id:
        target_event = get_event_by_id(events, matched_booking["event_id"])
        target_title = target_event["title"] if target_event else matched_booking.get("event_title", "another event")
        return (
            False,
            f"⚠️ Event Mismatch: This ticket is issued for '{target_title}' ({matched_booking['event_id']}), not the selected event.",
            matched_booking,
            "WRONG_EVENT"
        )

    # Check booking status
    if matched_booking["status"] == "Cancelled":
        return (
            False,
            f"🚫 Ticket Cancelled: Booking ({matched_booking['ticket_id']}) was cancelled by the attendee and is void.",
            matched_booking,
            "CANCELLED"
        )

    # Check duplicate check-in
    if matched_booking.get("attendance") == "Checked-in":
        checked_time = matched_booking.get("checkin_time", "Earlier")
        return (
            False,
            f"⚠️ Already Checked-in: {matched_booking['student_name']} was already checked in at {checked_time}.",
            matched_booking,
            "ALREADY_CHECKED_IN"
        )

    # Record successful check-in
    now_str = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    matched_booking["attendance"] = "Checked-in"
    matched_booking["checkin_time"] = now_str

    return (
        True,
        f"✅ Check-in Verified: Welcome {matched_booking['student_name']} ({matched_booking['student_id']})!",
        matched_booking,
        "SUCCESS"
    )

def get_event_attendees(bookings: List[Dict[str, Any]], event_id: str) -> List[Dict[str, Any]]:
    return [b for b in bookings if b.get("event_id") == event_id]

def get_organizer_kpis(events: List[Dict[str, Any]], bookings: List[Dict[str, Any]]) -> Dict[str, Any]:
    total_events = len(events)
    published_events = len([e for e in events if e.get("is_published", True)])
    total_capacity = sum(e.get("capacity", 0) for e in events)
    
    active_bookings = [b for b in bookings if b.get("status") == "Confirmed"]
    total_active_bookings = len(active_bookings)
    
    checkins = [b for b in active_bookings if b.get("attendance") == "Checked-in"]
    total_checkins = len(checkins)

    checkin_rate = (total_checkins / total_active_bookings * 100) if total_active_bookings > 0 else 0.0

    return {
        "total_events": total_events,
        "published_events": published_events,
        "total_capacity": total_capacity,
        "total_active_bookings": total_active_bookings,
        "total_checkins": total_checkins,
        "checkin_rate": round(checkin_rate, 1)
    }
