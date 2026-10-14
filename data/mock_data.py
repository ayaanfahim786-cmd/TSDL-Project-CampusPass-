"""
CampusPass - Mock Data & Initial State
Contains seed events, student profiles, initial bookings, and waitlist queues.
"""

from datetime import datetime

DEFAULT_STUDENT = {
    "student_id": "STU-2026-104",
    "name": "Aarav Sharma",
    "email": "aarav.sharma@campus.edu",
    "department": "Computer Science & Engineering",
    "batch": "B.Tech 3rd Year (Class of 2027)",
    "roll_no": "22BCSE104"
}

DEFAULT_ORGANIZER = {
    "organizer_id": "ORG-TECH-01",
    "name": "Dr. Meera Iyer",
    "title": "Campus Tech Council Lead & Faculty Advisor",
    "email": "tech.council@campus.edu",
    "department": "Office of Student Affairs & Technology"
}

CATEGORIES = [
    "All",
    "Hackathon",
    "Technical Workshop",
    "Cultural Fest",
    "Robotics Competition",
    "Design Workshop",
    "Entrepreneurship Talk",
    "AI & Seminar"
]

def get_initial_events():
    return [
        {
            "id": "EVT-101",
            "title": "HackCampus 2026: 24h National Hackathon",
            "category": "Hackathon",
            "date": "2026-10-24",
            "time": "09:00 AM - 09:00 AM (Next Day)",
            "venue": "Dr. A.P.J. Abdul Kalam Convention Centre",
            "capacity": 120,
            "booked_count": 114,
            "organizer": "Campus Coding Society",
            "organizer_email": "coding.club@campus.edu",
            "description": "The flagship annual hackathon bringing together over 100+ student innovators to build solutions in Healthcare, AI, and Sustainability. Free meals, mentor guidance, and cash prizes worth ₹1,50,000.",
            "deadline": "2026-10-22",
            "is_published": True,
            "status": "Active",
            "color_accent": "#10B981",
            "tags": ["Coding", "Cash Prizes", "Free Meals", "Mentorship"]
        },
        {
            "id": "EVT-102",
            "title": "Full-Stack AI Workshop: Building with LLM Agents",
            "category": "Technical Workshop",
            "date": "2026-10-18",
            "time": "02:00 PM - 05:30 PM",
            "venue": "Turing Lab 3, Department of CSE",
            "capacity": 45,
            "booked_count": 45,
            "organizer": "AI & Robotics Club",
            "organizer_email": "ai.club@campus.edu",
            "description": "Hands-on masterclass on building autonomous LLM agents, vector search, and local small language models. Participants get API credits and a certificate of completion.",
            "deadline": "2026-10-17",
            "is_published": True,
            "status": "Active",
            "color_accent": "#3B82F6",
            "tags": ["AI", "Hands-on", "Python", "Certificate"]
        },
        {
            "id": "EVT-103",
            "title": "AURA '26: Annual Inter-College Cultural Fest",
            "category": "Cultural Fest",
            "date": "2026-11-05",
            "time": "05:00 PM - 10:30 PM",
            "venue": "Open Air Amphitheatre (OAT)",
            "capacity": 400,
            "booked_count": 285,
            "organizer": "Student Cultural Committee",
            "organizer_email": "cultural@campus.edu",
            "description": "The campus's most anticipated cultural night featuring battle of the bands, classical fusion, contemporary choreography troupes, food stalls, and a celebrity DJ guest performance.",
            "deadline": "2026-11-04",
            "is_published": True,
            "status": "Active",
            "color_accent": "#EC4899",
            "tags": ["Music", "Dance", "Food Stalls", "Celebrity Night"]
        },
        {
            "id": "EVT-104",
            "title": "RoboWars: Combat Robotics Championship",
            "category": "Robotics Competition",
            "date": "2026-10-29",
            "time": "10:00 AM - 04:00 PM",
            "venue": "Mechanical Engineering Workshop Arena",
            "capacity": 80,
            "booked_count": 62,
            "organizer": "Robotics Society",
            "organizer_email": "robotics@campus.edu",
            "description": "Witness custom-engineered 15kg and 30kg combat bots clash inside our reinforced polycarbonate battle arena. High-voltage engineering tournament with live telemetry and referee panels.",
            "deadline": "2026-10-28",
            "is_published": True,
            "status": "Active",
            "color_accent": "#F59E0B",
            "tags": ["Combat Bots", "Hardware", "Live Battles"]
        },
        {
            "id": "EVT-105",
            "title": "Design Systems & UI/UX Sprint",
            "category": "Design Workshop",
            "date": "2026-10-20",
            "time": "11:00 AM - 01:30 PM",
            "venue": "Design Studio Hall A, Architecture Block",
            "capacity": 50,
            "booked_count": 38,
            "organizer": "Campus Design Guild",
            "organizer_email": "design@campus.edu",
            "description": "Learn design token architectures, accessible WCAG contrast grids, and micro-interaction prototyping directly in Figma from visiting product design leads. Free portfolio critique session included.",
            "deadline": "2026-10-19",
            "is_published": True,
            "status": "Active",
            "color_accent": "#8B5CF6",
            "tags": ["Figma", "UI/UX", "Portfolio Review"]
        },
        {
            "id": "EVT-106",
            "title": "Founder's Fireside: From Dorm Project to ₹10Cr Seed",
            "category": "Entrepreneurship Talk",
            "date": "2026-10-31",
            "time": "04:30 PM - 06:30 PM",
            "venue": "Management Auditorium (Main Campus)",
            "capacity": 150,
            "booked_count": 98,
            "organizer": "E-Cell & Incubation Center",
            "organizer_email": "ecell@campus.edu",
            "description": "Alumni unicorn founders share unfiltered insights on finding problem-solution fit in university, cold pitching venture funds, and scaling technical teams without burning out.",
            "deadline": "2026-10-30",
            "is_published": True,
            "status": "Active",
            "color_accent": "#14B8A6",
            "tags": ["Startups", "Venture Capital", "Networking"]
        },
        {
            "id": "EVT-107",
            "title": "Quantum Computing & Cryptography Seminar",
            "category": "AI & Seminar",
            "date": "2026-11-02",
            "time": "03:00 PM - 05:00 PM",
            "venue": "Sir C.V. Raman Physics Seminar Hall",
            "capacity": 70,
            "booked_count": 51,
            "organizer": "Department of Physics & CS",
            "organizer_email": "physics.dept@campus.edu",
            "description": "Distinguished lecture on quantum algorithms, qubit simulators in Qiskit, and post-quantum encryption standards presented by senior researchers from the National Institute of Science.",
            "deadline": "2026-11-01",
            "is_published": True,
            "status": "Active",
            "color_accent": "#06B6D4",
            "tags": ["Quantum", "Cryptography", "Research"]
        },
        {
            "id": "EVT-108",
            "title": "Open Source Day: Git, Linux & First Pull Request",
            "category": "Technical Workshop",
            "date": "2026-10-22",
            "time": "01:30 PM - 04:30 PM",
            "venue": "Seminar Hall 2, IT Block",
            "capacity": 60,
            "booked_count": 60,
            "organizer": "Free & Open Source Guild",
            "organizer_email": "foss@campus.edu",
            "description": "A beginner-friendly sprint guiding undergraduates step-by-step through Git version control, branching strategies, and submitting their very first open source pull request on GitHub.",
            "deadline": "2026-10-21",
            "is_published": True,
            "status": "Active",
            "color_accent": "#6366F1",
            "tags": ["GitHub", "Git", "Beginner Friendly"]
        },
        {
            "id": "EVT-109",
            "title": "Campus Game Jam: 36h Indie Game Challenge",
            "category": "Hackathon",
            "date": "2026-11-12",
            "time": "06:00 PM (Fri) - 06:00 AM (Sun)",
            "venue": "Campus Media Lab & Creative Suite",
            "capacity": 90,
            "booked_count": 42,
            "organizer": "Game Developers Circle",
            "organizer_email": "gamedev@campus.edu",
            "description": "Theme announced at opening ceremony! Build a playable game using Godot, Unity, or Unreal. Category prizes for best art style, soundtrack, and emergent gameplay mechanics.",
            "deadline": "2026-11-10",
            "is_published": True,
            "status": "Active",
            "color_accent": "#F43F5E",
            "tags": ["GameDev", "Unity", "Godot", "Creative"]
        }
    ]

def get_initial_bookings():
    return [
        # Demo student Aarav Sharma's bookings
        {
            "ticket_id": "CP-2026-A101",
            "event_id": "EVT-101",
            "event_title": "HackCampus 2026: 24h National Hackathon",
            "student_id": "STU-2026-104",
            "student_name": "Aarav Sharma",
            "student_email": "aarav.sharma@campus.edu",
            "booking_time": "2026-10-14 10:30 AM",
            "status": "Confirmed",
            "attendance": "Checked-in",
            "checkin_time": "2026-10-24 09:12 AM",
            "ticket_credential": "SEC-CP101-7F4A2B",
            "qr_payload": "CAMPUSPASS:EVT-101:SEC-CP101-7F4A2B:Aarav Sharma"
        },
        {
            "ticket_id": "CP-2026-A105",
            "event_id": "EVT-105",
            "event_title": "Design Systems & UI/UX Sprint",
            "student_id": "STU-2026-104",
            "student_name": "Aarav Sharma",
            "student_email": "aarav.sharma@campus.edu",
            "booking_time": "2026-10-15 02:15 PM",
            "status": "Confirmed",
            "attendance": "Not Checked-in",
            "checkin_time": None,
            "ticket_credential": "SEC-CP105-9D2E8C",
            "qr_payload": "CAMPUSPASS:EVT-105:SEC-CP105-9D2E8C:Aarav Sharma"
        },
        {
            "ticket_id": "CP-2026-A106",
            "event_id": "EVT-106",
            "event_title": "Founder's Fireside: From Dorm Project to ₹10Cr Seed",
            "student_id": "STU-2026-104",
            "student_name": "Aarav Sharma",
            "student_email": "aarav.sharma@campus.edu",
            "booking_time": "2026-10-15 04:00 PM",
            "status": "Confirmed",
            "attendance": "Not Checked-in",
            "checkin_time": None,
            "ticket_credential": "SEC-CP106-3B1F7A",
            "qr_payload": "CAMPUSPASS:EVT-106:SEC-CP106-3B1F7A:Aarav Sharma"
        },
        # Other peer students for EVT-101
        {
            "ticket_id": "CP-2026-R201",
            "event_id": "EVT-101",
            "event_title": "HackCampus 2026: 24h National Hackathon",
            "student_id": "STU-2026-108",
            "student_name": "Rohan Gupta",
            "student_email": "rohan.gupta@campus.edu",
            "booking_time": "2026-10-14 11:00 AM",
            "status": "Confirmed",
            "attendance": "Checked-in",
            "checkin_time": "2026-10-24 09:18 AM",
            "ticket_credential": "SEC-CP101-8C3D1E",
            "qr_payload": "CAMPUSPASS:EVT-101:SEC-CP101-8C3D1E:Rohan Gupta"
        },
        {
            "ticket_id": "CP-2026-A202",
            "event_id": "EVT-101",
            "event_title": "HackCampus 2026: 24h National Hackathon",
            "student_id": "STU-2026-112",
            "student_name": "Ananya Sen",
            "student_email": "ananya.sen@campus.edu",
            "booking_time": "2026-10-14 11:35 AM",
            "status": "Confirmed",
            "attendance": "Checked-in",
            "checkin_time": "2026-10-24 09:22 AM",
            "ticket_credential": "SEC-CP101-4E7B2A",
            "qr_payload": "CAMPUSPASS:EVT-101:SEC-CP101-4E7B2A:Ananya Sen"
        },
        {
            "ticket_id": "CP-2026-P203",
            "event_id": "EVT-101",
            "event_title": "HackCampus 2026: 24h National Hackathon",
            "student_id": "STU-2026-125",
            "student_name": "Priya Nair",
            "student_email": "priya.nair@campus.edu",
            "booking_time": "2026-10-14 12:10 PM",
            "status": "Confirmed",
            "attendance": "Not Checked-in",
            "checkin_time": None,
            "ticket_credential": "SEC-CP101-1A9C8D",
            "qr_payload": "CAMPUSPASS:EVT-101:SEC-CP101-1A9C8D:Priya Nair"
        },
        # EVT-102 attendees
        {
            "ticket_id": "CP-2026-V301",
            "event_id": "EVT-102",
            "event_title": "Full-Stack AI Workshop: Building with LLM Agents",
            "student_id": "STU-2026-130",
            "student_name": "Vikram Patel",
            "student_email": "vikram.patel@campus.edu",
            "booking_time": "2026-10-14 01:20 PM",
            "status": "Confirmed",
            "attendance": "Checked-in",
            "checkin_time": "2026-10-18 01:50 PM",
            "ticket_credential": "SEC-CP102-5D6A7B",
            "qr_payload": "CAMPUSPASS:EVT-102:SEC-CP102-5D6A7B:Vikram Patel"
        },
        {
            "ticket_id": "CP-2026-N302",
            "event_id": "EVT-102",
            "event_title": "Full-Stack AI Workshop: Building with LLM Agents",
            "student_id": "STU-2026-141",
            "student_name": "Neha Joshi",
            "student_email": "neha.joshi@campus.edu",
            "booking_time": "2026-10-14 02:00 PM",
            "status": "Confirmed",
            "attendance": "Checked-in",
            "checkin_time": "2026-10-18 01:55 PM",
            "ticket_credential": "SEC-CP102-2B8C4F",
            "qr_payload": "CAMPUSPASS:EVT-102:SEC-CP102-2B8C4F:Neha Joshi"
        },
        # EVT-103 attendees
        {
            "ticket_id": "CP-2026-D401",
            "event_id": "EVT-103",
            "event_title": "AURA '26: Annual Inter-College Cultural Fest",
            "student_id": "STU-2026-155",
            "student_name": "Devendra Singh",
            "student_email": "devendra.singh@campus.edu",
            "booking_time": "2026-10-15 09:30 AM",
            "status": "Confirmed",
            "attendance": "Not Checked-in",
            "checkin_time": None,
            "ticket_credential": "SEC-CP103-6F3E1A",
            "qr_payload": "CAMPUSPASS:EVT-103:SEC-CP103-6F3E1A:Devendra Singh"
        },
        # EVT-104 attendees
        {
            "ticket_id": "CP-2026-T501",
            "event_id": "EVT-104",
            "event_title": "RoboWars: Combat Robotics Championship",
            "student_id": "STU-2026-160",
            "student_name": "Tanya Verma",
            "student_email": "tanya.verma@campus.edu",
            "booking_time": "2026-10-15 11:45 AM",
            "status": "Confirmed",
            "attendance": "Checked-in",
            "checkin_time": "2026-10-29 09:48 AM",
            "ticket_credential": "SEC-CP104-7A2B9C",
            "qr_payload": "CAMPUSPASS:EVT-104:SEC-CP104-7A2B9C:Tanya Verma"
        },
        # EVT-108 attendees
        {
            "ticket_id": "CP-2026-A601",
            "event_id": "EVT-108",
            "event_title": "Open Source Day: Git, Linux & First Pull Request",
            "student_id": "STU-2026-172",
            "student_name": "Aditi Rao",
            "student_email": "aditi.rao@campus.edu",
            "booking_time": "2026-10-15 03:20 PM",
            "status": "Confirmed",
            "attendance": "Not Checked-in",
            "checkin_time": None,
            "ticket_credential": "SEC-CP108-8C5D3E",
            "qr_payload": "CAMPUSPASS:EVT-108:SEC-CP108-8C5D3E:Aditi Rao"
        }
    ]

def get_initial_waitlist():
    return [
        {
            "waitlist_id": "WL-102-001",
            "event_id": "EVT-102",
            "student_id": "STU-2026-180",
            "student_name": "Kabir Mehta",
            "student_email": "kabir.mehta@campus.edu",
            "joined_time": "2026-10-15 05:00 PM",
            "queue_position": 1
        },
        {
            "waitlist_id": "WL-102-002",
            "event_id": "EVT-102",
            "student_id": "STU-2026-185",
            "student_name": "Sanya Kapoor",
            "student_email": "sanya.kapoor@campus.edu",
            "joined_time": "2026-10-15 06:15 PM",
            "queue_position": 2
        }
    ]
