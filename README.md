# CampusPass — Campus Event Ticketing & Attendance System

CampusPass is an all-in-one web application for university event ticketing and gate attendance. It allows students to discover campus events, reserve digital passes with unique QR codes, and join waitlists. At the same time, it provides event organizers with tools to manage listings, track live attendance, verify tickets at the gate, and view registration analytics.

---

## ⚡ How to Run the Project

### 1. Prerequisites
- Python 3.10 or higher installed.

### 2. Install Dependencies
Open your terminal in the project directory and run:
```bash
pip install -r requirements.txt
```

### 3. Start the Application
```bash
streamlit run app.py
```
The app will automatically open in your default browser at `http://localhost:8501`.

---

## 📂 Codebase Structure & How It Works

The codebase follows a **modular architecture** with a strict separation of concerns across layers:

```
CampusPass/
├── app.py                      # Main entry point: routing, sidebar & role switcher
├── requirements.txt            # Project dependencies
├── README.md                   # Project guide and documentation
├── .streamlit/
│   └── config.toml             # Dark theme visual styling settings
├── data/
│   └── mock_data.py            # Pre-seeded events, student profiles & initial bookings
├── services/                   # Business logic layer (independent of UI)
│   ├── event_service.py        # Event search, category filtering & CRUD actions
│   ├── booking_service.py      # Ticket creation, cancellation & waitlist queueing
│   └── attendance_service.py   # Gate check-in verification, duplicate checks & KPIs
├── pages_views/                # Presentation/UI layer (Streamlit views)
│   ├── discover.py             # Event browsing, searching, and pass booking
│   ├── tickets.py              # Student ticket wallet & QR pass display
│   ├── organizer_dashboard.py  # Visual charts & registration metrics
│   ├── manage_events.py        # Event creation, capacity editing & attendee roster
│   └── checkin.py              # Gate entry scanner and manual pass validator
└── utils/                      # Helper utilities
    ├── qr_utils.py             # QR code generation and PNG byte conversion
    └── ui_components.py        # Custom CSS, badges, KPI cards & page headers
```

### Flow of Data:
1. **Entry Point (`app.py`)**: Initializes global session state with seed data from `data/mock_data.py`, provides the sidebar role switcher (Student / Organizer), and dispatches the active view.
2. **Services (`services/`)**: Contains pure Python functions implementing business rules (no Streamlit UI code).
3. **Pages/Views (`pages_views/`)**: Handles user inputs and displays results using Streamlit elements.
4. **Utils (`utils/`)**: Provides shared UI styling components and QR code image processing.

---

## 🧠 Concepts & Technologies Used

### 1. Software Architecture & Design Patterns
- **Separation of Concerns (SoC)**: Business logic (`services/`), data storage (`data/`), and presentation (`pages_views/`) are decoupled for easy testing and maintenance.
- **Role-Based Views**: Instant persona switching between **Student** and **Organizer** to simulate end-to-end workflows without login complexity.
- **In-Memory State Store**: Uses Streamlit's `st.session_state` as a reactive, lightweight database that retains all actions across page switches.

### 2. Ticketing & Gate Logic
- **Unique Credential Generation**: Creates human-readable ticket numbers (`CP-2026-XXXX`) and cryptographically random security codes (`SEC-CPXXX-XXXXXX`).
- **QR Code Encoding**: Dynamically creates real scannable QR images using `qrcode` and `Pillow` (PIL) for on-screen display and PNG download.
- **Idempotent Check-in & Duplicate Prevention**: Verifies ticket legitimacy at the gate, rejects tickets from different events, and blocks double check-ins while logging entry timestamps.
- **Capacity & FIFO Waitlist Queue**: Prevents overbooking. When capacity reaches 100%, students are placed in a First-In, First-Out (FIFO) queue with live position numbers.
- **Seat Release on Cancellation**: Canceling a pass frees up a seat and updates event capacity in real time.

### 3. Data Science & Visual Analytics
- **Data Wrangling with Pandas**: Formats event logs, calculates summary tables, and powers one-click CSV attendee roster exports.
- **Interactive Visualizations (Plotly)**:
  - Bar charts for registrations across events.
  - Donut charts for total gate attendance turnout rate.

### 4. Modern UI/UX Engineering
- **Custom Design System**: Dark theme (`#0B0E14`) built with custom CSS tokens, modern typography (*Plus Jakarta Sans* and *JetBrains Mono*), and emerald accenting.
- **Streamlit Reactive Components**: Layout columns, tabs, metric stat cards, conditional badges, and interactive popups (`st.dialog`).

---

## 🎯 Key User Journeys to Test

### A. Student Pass Booking
1. Set the sidebar role to **Student**.
2. Go to **Discover Events** and search or filter by category.
3. Click **Book Free Pass** on an open event to reserve your seat.
4. Open **My Tickets** to view your pass and generated QR code.

### B. Waitlist Overflow Flow
1. In **Discover Events**, find a full event (e.g., *Full-Stack AI Workshop*).
2. Click **Join Waitlist** to get an assigned queue number (`#1`, `#2`, etc.).

### C. Gate Check-in & Admission
1. Switch the sidebar role to **Organizer**.
2. Go to **Attendance Check-in**, choose an event, and enter a Ticket ID (e.g. `CP-2026-P203`).
3. Click **Verify & Admit Attendee** to confirm admission, or test duplicate entry prevention.

### D. Organizer Analytics & Export
1. Go to **Organizer Dashboard** to view live KPI cards and Plotly charts.
2. Go to **Manage Events** → **Attendee Roster** to view or download the attendee list as a CSV.
