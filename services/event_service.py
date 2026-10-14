"""
CampusPass - Event Service
Handles event queries, filtering, creation, updating, and status toggles.
"""

import uuid
from typing import List, Dict, Any, Tuple, Optional

def get_all_events(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return events

def get_event_by_id(events: List[Dict[str, Any]], event_id: str) -> Optional[Dict[str, Any]]:
    for event in events:
        if event["id"] == event_id:
            return event
    return None

def filter_events(
    events: List[Dict[str, Any]],
    search_query: str = "",
    category: str = "All",
    availability: str = "All"
) -> List[Dict[str, Any]]:
    filtered = []
    query = search_query.strip().lower()

    for e in events:
        # Check publication status
        if not e.get("is_published", True):
            continue

        # Category filter
        if category != "All" and e.get("category") != category:
            continue

        # Availability filter
        available_seats = max(0, e.get("capacity", 0) - e.get("booked_count", 0))
        if availability == "Open Only" and available_seats <= 0:
            continue
        elif availability == "Full / Waitlist Only" and available_seats > 0:
            continue

        # Search filter
        if query:
            match_title = query in e.get("title", "").lower()
            match_desc = query in e.get("description", "").lower()
            match_venue = query in e.get("venue", "").lower()
            match_org = query in e.get("organizer", "").lower()
            match_tags = any(query in tag.lower() for tag in e.get("tags", []))
            if not (match_title or match_desc or match_venue or match_org or match_tags):
                continue

        filtered.append(e)

    return filtered

def create_event(events: List[Dict[str, Any]], event_data: Dict[str, Any]) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    # Validation
    title = event_data.get("title", "").strip()
    if not title:
        return False, "Event title is required.", None

    capacity = event_data.get("capacity", 0)
    if capacity <= 0:
        return False, "Event capacity must be greater than 0.", None

    # Generate sequential or unique ID
    existing_nums = []
    for e in events:
        if e["id"].startswith("EVT-"):
            try:
                num = int(e["id"].split("-")[1])
                existing_nums.append(num)
            except ValueError:
                pass
    next_num = max(existing_nums, default=100) + 1
    new_id = f"EVT-{next_num}"

    new_event = {
        "id": new_id,
        "title": title,
        "category": event_data.get("category", "Technical Workshop"),
        "date": str(event_data.get("date", "")),
        "time": str(event_data.get("time", "")),
        "venue": event_data.get("venue", "Main Campus Hall"),
        "capacity": int(capacity),
        "booked_count": 0,
        "organizer": event_data.get("organizer", "Campus Student Body"),
        "organizer_email": event_data.get("organizer_email", "organizer@campus.edu"),
        "description": event_data.get("description", ""),
        "deadline": str(event_data.get("deadline", "")),
        "is_published": event_data.get("is_published", True),
        "status": "Active",
        "color_accent": event_data.get("color_accent", "#10B981"),
        "tags": event_data.get("tags", ["Campus Event"])
    }

    events.append(new_event)
    return True, f"Event '{title}' created successfully with ID {new_id}!", new_event

def update_event(events: List[Dict[str, Any]], event_id: str, updated_fields: Dict[str, Any]) -> Tuple[bool, str]:
    event = get_event_by_id(events, event_id)
    if not event:
        return False, f"Event with ID {event_id} not found."

    # Prevent capacity from being reduced below current active bookings
    new_capacity = updated_fields.get("capacity")
    if new_capacity is not None:
        booked_count = event.get("booked_count", 0)
        if new_capacity < booked_count:
            return False, f"Capacity cannot be reduced to {new_capacity}. Currently {booked_count} active bookings exist."

    # Update allowed fields
    for k, v in updated_fields.items():
        event[k] = v

    return True, f"Event '{event['title']}' updated successfully."

def toggle_publish_status(events: List[Dict[str, Any]], event_id: str) -> Tuple[bool, str]:
    event = get_event_by_id(events, event_id)
    if not event:
        return False, "Event not found."

    event["is_published"] = not event.get("is_published", True)
    status_str = "Published" if event["is_published"] else "Unpublished (Draft)"
    return True, f"Event visibility set to: {status_str}"

def cancel_event(events: List[Dict[str, Any]], event_id: str) -> Tuple[bool, str]:
    event = get_event_by_id(events, event_id)
    if not event:
        return False, "Event not found."

    event["status"] = "Cancelled"
    return True, f"Event '{event['title']}' has been cancelled."
