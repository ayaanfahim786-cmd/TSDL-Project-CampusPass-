"""
CampusPass - Organizer Dashboard
Lightweight analytics hub showing metrics, Plotly registration & attendance charts, and recent activity.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from services.attendance_service import get_organizer_kpis
from utils.ui_components import render_page_header, render_stat_box, render_coming_soon

def render_organizer_dashboard_page():
    render_page_header(
        title="Organizer Operations Dashboard",
        subtitle="Real-time campus registration metrics, gate attendance telemetry, and capacity utilization.",
    
    )

    events = st.session_state.get("events", [])
    bookings = st.session_state.get("bookings", [])
    waitlist = st.session_state.get("waitlist", [])

    kpis = get_organizer_kpis(events, bookings)

    # 4 KPI Metrics
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric("Published Events", kpis["published_events"], f"{kpis['total_events']} total")
    with kpi2:
        st.metric("Active Passes", kpis["total_active_bookings"], f"{kpis['total_capacity']} total seats")
    with kpi3:
        st.metric("Gate Check-ins", kpis["total_checkins"], f"{kpis['checkin_rate']}% turnout")
    with kpi4:
        st.metric("Waitlist Queue", len(waitlist))

    st.markdown("---")

    # Charts Row
    chart_col1, chart_col2 = st.columns([1.6, 1.2])

    with chart_col1:
        st.markdown("#### 📊 Registrations by Campus Event")
        # Build DataFrame for Events
        event_chart_data = []
        for e in events:
            if e.get("is_published", True):
                booked = e.get("booked_count", 0)
                cap = e.get("capacity", 0)
                # Count actual checkins for this event
                chk = len([b for b in bookings if b.get("event_id") == e["id"] and b.get("attendance") == "Checked-in" and b.get("status") == "Confirmed"])
                event_chart_data.append({
                    "Event": e.get("title")[:24] + ("..." if len(e.get("title")) > 24 else ""),
                    "Full Title": e.get("title"),
                    "Booked Passes": booked,
                    "Gate Check-ins": chk,
                    "Capacity": cap
                })

        if event_chart_data:
            df_events = pd.DataFrame(event_chart_data)
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                x=df_events["Event"],
                y=df_events["Booked Passes"],
                name="Passes Booked",
                marker_color="#10B981"
            ))
            fig_bar.add_trace(go.Bar(
                x=df_events["Event"],
                y=df_events["Gate Check-ins"],
                name="Checked In",
                marker_color="#3B82F6"
            ))
            fig_bar.update_layout(
                barmode="group",
                paper_bgcolor="#131722",
                plot_bgcolor="#131722",
                font=dict(color="#9CA3AF", family="Plus Jakarta Sans"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=20, r=20, t=30, b=50),
                height=280,
                xaxis=dict(showgrid=False, tickangle=-25),
                yaxis=dict(gridcolor="#262D3D")
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No active events found for chart rendering.")

    with chart_col2:
        st.markdown("#### 🎯 Overall Attendance Distribution")
        active_b = [b for b in bookings if b.get("status") == "Confirmed"]
        checked_in_count = len([b for b in active_b if b.get("attendance") == "Checked-in"])
        pending_count = len(active_b) - checked_in_count

        if active_b:
            fig_donut = go.Figure(data=[go.Pie(
                labels=["Checked In", "Awaiting Arrival"],
                values=[checked_in_count, pending_count],
                hole=0.65,
                marker=dict(colors=["#10B981", "#374151"])
            )])
            fig_donut.update_layout(
                paper_bgcolor="#131722",
                font=dict(color="#9CA3AF", family="Plus Jakarta Sans"),
                legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
                margin=dict(l=10, r=10, t=20, b=20),
                height=280
            )
            st.plotly_chart(fig_donut, use_container_width=True)
        else:
            st.info("No booking records yet.")

    # Table and Recent Activity
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📋 Campus Events Capacity Matrix", "⚡ Recent Activity Feed"])

    with tab1:
        table_rows = []
        for e in events:
            cap = e.get("capacity", 0)
            b_cnt = e.get("booked_count", 0)
            chks = len([b for b in bookings if b.get("event_id") == e["id"] and b.get("attendance") == "Checked-in" and b.get("status") == "Confirmed"])
            rate = f"{(chks / b_cnt * 100):.1f}%" if b_cnt > 0 else "0.0%"
            status = "Published" if e.get("is_published", True) else "Draft"
            if e.get("status") == "Cancelled":
                status = "Cancelled"

            table_rows.append({
                "Event ID": e.get("id"),
                "Event Name": e.get("title"),
                "Date": e.get("date"),
                "Venue": e.get("venue"),
                "Capacity": cap,
                "Booked Seats": b_cnt,
                "Check-ins": chks,
                "Turnout %": rate,
                "Status": status
            })

        df_table = pd.DataFrame(table_rows)
        st.dataframe(
            df_table,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Capacity": st.column_config.NumberColumn(format="%d seats"),
                "Booked Seats": st.column_config.NumberColumn(format="%d passes"),
                "Check-ins": st.column_config.NumberColumn(format="%d verified")
            }
        )

    with tab2:
        st.caption("Latest registrations and gate entries across all campus events:")
        recent_bookings = bookings[:8]
        if not recent_bookings:
            st.info("No recent bookings recorded.")
        else:
            for act in recent_bookings:
                is_chk = act.get("attendance") == "Checked-in"
                badge = "cp-badge-emerald" if is_chk else "cp-badge-blue"
                action_text = f"Checked in at {act.get('checkin_time', '')}" if is_chk else f"Booked pass at {act.get('booking_time')}"

                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.55rem 0.8rem; background: #181D2A; border-bottom: 1px solid #262D3D; border-radius: 6px; margin-bottom: 0.4rem; font-size: 0.82rem;">
                    <div>
                        <span class="cp-badge {badge}" style="font-size: 0.65rem;">{act.get('attendance')}</span>
                        <b style="color: #F3F4F6; margin-left: 0.5rem;">{act.get('student_name')}</b>
                        <span style="color: #9CA3AF;">&bull; {act.get('event_title')}</span>
                    </div>
                    <div style="color: #6B7280; font-family: monospace;">
                        {action_text}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown(render_coming_soon("Automated Hourly CSV Report Mailer"), unsafe_allow_html=True)
