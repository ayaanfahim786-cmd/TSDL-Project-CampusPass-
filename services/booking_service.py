"""
CampusPass - Booking Service
Handles ticket generation, booking creation, cancellation, and waitlist operations.
"""

import uuid
import secrets
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional
from services.event_service import get_event_by_id

def generate_ticket_id() -> str:
    # Format: CP-2026-X8Y9
    chars = secrets.token_hex(2).upper()
    rand_num = secrets.randbelow(900) + 100
    return f"CP-2026-{chars}{rand_num}"

def generate_ticket_credential(event_id: str) -> str:
    # Format: SEC-CP101-7A4B9F
    short_id = event_id.replace("EVT-", "CP")
    token = secrets.token_hex(3).upper()
    return f"SEC-{short_id}-{token}"

def get_student_bookings(bookings: List[Dict[str, Any]], student_id: str) -> List[Dict[str, Any]]:
    return [b for b in bookings if b.get("student_id") == student_id]

def get_student_waitlist_entries(waitlist: List[Dict[str, Any]], student_id: str) -> List[Dict[str, Any]]:
    return [w for w in waitlist if w.get("student_id") == student_id]

def book_event(
    events: List[Dict[str, Any]],
    bookings: List[Dict[str, Any]],
    waitlist: List[Dict[str, Any]],
    event_id: str,
    student: Dict[str, Any]
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    event = get_event_by_id(events, event_id)
    if not event:
        return False, "Event not found.", None

    if event.get("status") == "Cancelled":
        return False, "This event has been cancelled by the organizers.", None

    if not event.get("is_published", True):
        return False, "This event is currently unlisted or in draft status.", None

    student_id = student["student_id"]

    # Prevent duplicate active bookings for the same student and event
    for b in bookings:
        if b["event_id"] == event_id and b["student_id"] == student_id and b["status"] == "Confirmed":
            return False, f"You already have an active ticket ({b['ticket_id']}) for this event.", None

    # Check capacity limit
    current_booked = event.get("booked_count", 0)
    capacity = event.get("capacity", 0)
    if current_booked >= capacity:
        return False, "This event is fully booked. You can join the waitlist instead.", None

    # Generate credentials
    ticket_id = generate_ticket_id()
    credential = generate_ticket_credential(event_id)
    now_str = datetime.now().strftime("%Y-%m-%d %I:%M %p")

    new_booking = {
        "ticket_id": ticket_id,
        "event_id": event_id,
        "event_title": event["title"],
        "student_id": student_id,
        "student_name": student["name"],
        "student_email": student["email"],
        "booking_time": now_str,
        "status": "Confirmed",
        "attendance": "Not Checked-in",
        "checkin_time": None,
        "ticket_credential": credential,
        "qr_payload": f"CAMPUSPASS:{event_id}:{credential}:{student['name']}"
    }

    # Update booked count
    event["booked_count"] = current_booked + 1
    bookings.insert(0, new_booking)

    # If student was on waitlist for this event, remove them
    for i, w in enumerate(list(waitlist)):
        if w["event_id"] == event_id and w["student_id"] == student_id:
            waitlist.remove(w)
            # Reindex queue positions
            _reindex_waitlist(waitlist, event_id)

    return True, f"Ticket booked successfully! Pass ID: {ticket_id}", new_booking

def cancel_booking(
    events: List[Dict[str, Any]],
    bookings: List[Dict[str, Any]],
    waitlist: List[Dict[str, Any]],
    ticket_id: str,
    student_id: str
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    # Find the booking
    booking = None
    for b in bookings:
        if b["ticket_id"] == ticket_id:
            booking = b
            break

    if not booking:
        return False, "Ticket not found.", None

    if booking["student_id"] != student_id:
        return False, "Unauthorized: You can only cancel your own bookings.", None

    if booking["status"] == "Cancelled":
        return False, "This booking is already cancelled.", None

    event_id = booking["event_id"]
    event = get_event_by_id(events, event_id)

    # Mark booking as cancelled
    booking["status"] = "Cancelled"

    # Release seat
    if event and event.get("booked_count", 0) > 0:
        event["booked_count"] = event["booked_count"] - 1

    # Check if waitlist has pending students
    promoted_info = None
    event_waitlist = [w for w in waitlist if w["event_id"] == event_id]
    if event_waitlist:
        next_in_queue = event_waitlist[0]
        promoted_info = {
            "student_name": next_in_queue["student_name"],
            "student_email": next_in_queue["student_email"],
            "queue_position": 1,
            "event_title": event["title"] if event else "the event"
        }

    return True, f"Booking {ticket_id} cancelled. 1 seat has been released.", promoted_info

def join_waitlist(
    events: List[Dict[str, Any]],
    bookings: List[Dict[str, Any]],
    waitlist: List[Dict[str, Any]],
    event_id: str,
    student: Dict[str, Any]
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    event = get_event_by_id(events, event_id)
    if not event:
        return False, "Event not found.", None

    student_id = student["student_id"]

    # Check if already booked
    for b in bookings:
        if b["event_id"] == event_id and b["student_id"] == student_id and b["status"] == "Confirmed":
            return False, "You already have a confirmed seat for this event.", None

    # Check if already in waitlist
    for w in waitlist:
        if w["event_id"] == event_id and w["student_id"] == student_id:
            return False, f"You are already in the waitlist at position #{w.get('queue_position', 1)}.", None

    current_queue = [w for w in waitlist if w["event_id"] == event_id]
    new_position = len(current_queue) + 1
    now_str = datetime.now().strftime("%Y-%m-%d %I:%M %p")

    wl_entry = {
        "waitlist_id": f"WL-{event_id.replace('EVT-', '')}-{secrets.token_hex(2).upper()}",
        "event_id": event_id,
        "student_id": student_id,
        "student_name": student["name"],
        "student_email": student["email"],
        "joined_time": now_str,
        "queue_position": new_position
    }

    waitlist.append(wl_entry)
    return True, f"Joined waitlist! Your queue position is #{new_position}.", wl_entry

def leave_waitlist(
    waitlist: List[Dict[str, Any]],
    event_id: str,
    student_id: str
) -> Tuple[bool, str]:
    target = None
    for w in waitlist:
        if w["event_id"] == event_id and w["student_id"] == student_id:
            target = w
            break

    if not target:
        return False, "You are not in the waitlist for this event."

    waitlist.remove(target)
    _reindex_waitlist(waitlist, event_id)
    return True, "Successfully removed from waitlist."

def _reindex_waitlist(waitlist: List[Dict[str, Any]], event_id: str):
    pos = 1
    for w in waitlist:
        if w["event_id"] == event_id:
            w["queue_position"] = pos
            pos += 1
