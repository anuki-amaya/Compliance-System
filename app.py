import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date
import plotly.express as px

st.set_page_config(
    page_title="Compliance Management System",
    page_icon="📊",
    layout="wide"
)
st.markdown("""
<style>

/* MAIN APP BACKGROUND */
.stApp {
    background-color: #1f2937;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background-color: #111827;
}

/* ALL HEADINGS */
h1, h2, h3 {
    color: white !important;
}

/* GENERAL TEXT */
p, div, span, label {
    color: white !important;
}

/* SIDEBAR TEXT */
[data-testid="stSidebar"] * {
    color: white !important;
}

/* METRICS */
[data-testid="stMetricLabel"] {
    color: #d1d5db !important;
}

[data-testid="stMetricValue"] {
    color: white !important;
}
.stButton > button {
    background-color: #192b52;
    color: white;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    border: none;
}

.stButton > button:hover {
    background-color: #374f82;
    color: white;
}
/* 🌟 Input fields (text box, dropdown, date picker) */
input, textarea {
    background-color: #3e4c5e !important;
    border-radius: 8px !important;
    border: 1px solid #E5E7EB !important;
}

/* 🌟 Select boxes */
div[data-baseweb="select"] > div {
    background-color: #3e4c5e !important;
    border-radius: 8px !important;
}

/* 🌟 Form container look */
section[data-testid="stForm"] {
    background-color: #3e4c5e;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #E5E7EB;
}

/* 🔥 Kill the internal input cursor completely */
div[data-baseweb="select"] input {
    opacity: 0 !important;
    position: absolute !important;
    pointer-events: none !important;
    caret-color: transparent !important;
}

/* 🔥 Force select display to behave like a button */
div[data-baseweb="select"] > div {
    cursor: pointer !important;
}

/* 🔥 Remove focus outline that triggers text mode feel */
div[data-baseweb="select"]:focus,
div[data-baseweb="select"] *:focus {
    outline: none !important;
    box-shadow: none !important;
}

/* 🔥 Extra: hide blinking caret container */
div[data-baseweb="select"] div[role="combobox"] {
    caret-color: transparent !important;
}
/* =========================
   FORCE DROPDOWN COLORS
   ========================= */

/* BaseWeb popover root */
div[data-baseweb="popover"] {
    background-color: #3e4c5e !important;
    border: 1px solid #2f3b4a !important;
    border-radius: 10px !important;
}

/* dropdown menu container */
ul, div[role="listbox"] {
    background-color: #3e4c5e !important;
}

/* dropdown options */
li, div[role="option"] {
    background-color: #3e4c5e !important;
    color: white !important;
}

/* hover option */
li:hover, div[role="option"]:hover {
    background-color: #2f3b4a !important;
    color: white !important;
}

/* selected option */
div[aria-selected="true"] {
    background-color: #1f2a36 !important;
    color: white !important;
}

/* =========================
   FORCE DATE PICKER
   ========================= */

/* calendar popup (IMPORTANT: BaseWeb uses this more reliably than role=dialog) */
div[data-baseweb="calendar"] {
    background-color: #3e4c5e !important;
    border-radius: 12px !important;
}

/* calendar all text */
div[data-baseweb="calendar"] * {
    color: white !important;
}

/* calendar days */
td, button[role="gridcell"] {
    color: #3e4c5e !important;
    background-color: transparent !important;
}

/* hover day */
td:hover, button[role="gridcell"]:hover {
    background-color: #2f3b4a !important;
}

/* selected day */
button[aria-selected="true"] {
    background-color: #1f2a36 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)
# SIDEBAR

st.sidebar.markdown("""
# 🛡️ Compliance System



---
""")

page = st.sidebar.radio(
    "📂 Navigation",
    [
        "📊 Dashboard",
        "📋 Internal Audits",
        "⚠️ Incidents",
        "🎓 Training",
        "📅 Activities"
    ]
)

# Dashboard
if page == "📊 Dashboard":

    st.title("📊 Compliance Management Dashboard")

    st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(
            135deg,
            #1e3a8a,
            #2563eb
        );
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: none;
        margin-bottom: 10px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }

    .metric-title {
        color: #9ca3af;
        font-size: 14px;
    }

    .metric-value {
        color: white;
        font-size: 32px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    conn = sqlite3.connect("compliance.db")
    cursor = conn.cursor()

    # Audit Counts
    cursor.execute("SELECT COUNT(*) FROM audit_findings")
    total_findings = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM audit_findings
    WHERE status != 'Closed'
    """)
    open_findings = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM audit_findings
    WHERE status = 'Closed'
    """)
    closed_findings = cursor.fetchone()[0]

    # Incidents
    cursor.execute("""
    SELECT COUNT(*)
    FROM incidents
    WHERE status != 'Closed'
    """)
    open_incidents = cursor.fetchone()[0]

    # Activities
    cursor.execute("""
    SELECT COUNT(*)
    FROM compliance_activities
    WHERE status != 'Completed'
    """)
    open_activities = cursor.fetchone()[0]

    # Training
    cursor.execute("""
    SELECT COUNT(*)
    FROM employee_training
    """)
    total_training = cursor.fetchone()[0]

    conn.close()

    # Health Score
    if total_findings > 0:
        health_score = round(
            (closed_findings / total_findings) * 100
        )
    else:
        health_score = 100

    # Audit Data
    conn = sqlite3.connect("compliance.db")

    audit_df = pd.read_sql_query(
        "SELECT * FROM audit_findings",
        conn
    )

    incident_df = pd.read_sql_query(
        "SELECT * FROM incidents",
        conn
    )

    conn.close()

    today = date.today()

    overdue_count = 0

    for _, row in audit_df.iterrows():

        due_date = datetime.strptime(
            row["due_date"],
            "%Y-%m-%d"
        ).date()

        if (
            due_date < today
            and row["status"] != "Closed"
        ):
            overdue_count += 1

    incident_overdue = 0

    for _, row in incident_df.iterrows():

        due_date = datetime.strptime(
            row["due_date"],
            "%Y-%m-%d"
        ).date()

        if (
            due_date < today
            and row["status"] != "Closed"
        ):
            incident_overdue += 1

    # KPI CARDS

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-title">
        Compliance Health
        </div>
        <div class="metric-value">
        {health_score}%
        </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-title">
        Open Findings
        </div>
        <div class="metric-value">
        {open_findings}
        </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-title">
        Open Incidents
        </div>
        <div class="metric-value">
        {open_incidents}
        </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-title">
        Open Activities
        </div>
        <div class="metric-value">
        {open_activities}
        </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # CHART LAYOUT

    left, middle, right = st.columns([1,1,1])

    # AUDIT DONUT
    with left:

        st.subheader("📋 Internal Audits")

        conn = sqlite3.connect("compliance.db")

        audit_chart = pd.read_sql_query("""
        SELECT status, COUNT(*) as count
        FROM audit_findings
        GROUP BY status
        """, conn)

        conn.close()

        fig1 = px.pie(
            audit_chart,
            names="status",
            values="count",
            hole=0.65,
            color_discrete_sequence=[
                "#22c55e",
                "#f59e0b",
                "#ef4444"
            ]
        )

        fig1.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            legend_font_color="white"
        )

        fig1.update_traces(
            textfont_color="white"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    # INCIDENT DONUT
    with middle:

        st.subheader("⚠️ Incident Management")

        conn = sqlite3.connect("compliance.db")

        incident_chart = pd.read_sql_query("""
        SELECT status, COUNT(*) as count
        FROM incidents
        GROUP BY status
        """, conn)

        conn.close()

        fig2 = px.pie(
            incident_chart,
            names="status",
            values="count",
            hole=0.65,
            color_discrete_sequence=[
                "#3b82f6",
                "#f59e0b",
                "#ef4444"
            ]
        )

        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            legend_font_color="white"
        )

        fig2.update_traces(
            textfont_color="white"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    # ALERT CENTER
    with right:

        st.subheader("🚨 Alert Center")

        if overdue_count > 0:
            st.error(
                f"{overdue_count} Overdue Audits"
            )

        if incident_overdue > 0:
            st.error(
                f"{incident_overdue} Overdue Incidents"
            )

        if open_activities > 0:
            st.warning(
                f"{open_activities} Open Activities"
            )

        st.info(
            f"{total_training} Training Records"
        )

    st.divider()

    # LIVE COMPLIANCE STATUS TRACKING

    st.subheader("🎯 Compliance Status Tracking")

    conn = sqlite3.connect("compliance.db")
    cursor = conn.cursor()

    # AUDITS
    cursor.execute("""
    SELECT COUNT(*)
    FROM audit_findings
    """)
    total_audits = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM audit_findings
    WHERE status = 'Closed'
    """)
    closed_audits = cursor.fetchone()[0]

    audit_score = (
        round((closed_audits / total_audits) * 100)
        if total_audits > 0 else 100
    )

    # INCIDENTS
    cursor.execute("""
    SELECT COUNT(*)
    FROM incidents
    """)
    total_incidents = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM incidents
    WHERE status = 'Closed'
    """)
    closed_incidents = cursor.fetchone()[0]

    incident_score = (
        round((closed_incidents / total_incidents) * 100)
        if total_incidents > 0 else 100
    )

    # ACTIVITIES
    cursor.execute("""
    SELECT COUNT(*)
    FROM compliance_activities
    """)
    total_activities = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM compliance_activities
    WHERE status = 'Completed'
    """)
    completed_activities = cursor.fetchone()[0]

    activity_score = (
        round((completed_activities / total_activities) * 100)
        if total_activities > 0 else 100
    )

    # TRAINING
    cursor.execute("""
    SELECT COUNT(*)
    FROM employee_training
    """)
    total_training_records = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM employee_training
    WHERE status = 'Valid'
    """)
    completed_training = cursor.fetchone()[0]

    training_score = (
        round((completed_training / total_training_records) * 100)
        if total_training_records > 0 else 100
    )

    conn.close()

    # DISPLAY PROGRESS BARS

    st.write("📋 Internal Audits")
    st.progress(audit_score / 100)
    st.caption(f"{audit_score}% Complete")

    st.write("⚠️ Incident Management")
    st.progress(incident_score / 100)
    st.caption(f"{incident_score}% Complete")

    st.write("📅 Compliance Activities")
    st.progress(activity_score / 100)
    st.caption(f"{activity_score}% Complete")

    st.write("🎓 Employee Training")
    st.progress(training_score / 100)
    st.caption(f"{training_score}% Complete")

    st.divider()
    # OVERVIEW CHART

    st.subheader("📊 Compliance Overview")

    overview_df = pd.DataFrame({
        "Module": [
            "Audits",
            "Incidents",
            "Training",
            "Activities"
        ],
        "Count": [
            total_findings,
            open_incidents,
            total_training,
            open_activities
        ]
    })

    fig3 = px.bar(
        overview_df,
        x="Module",
        y="Count",
        text="Count",
        color="Module"
    )

    fig3.update_traces(
        textposition="outside"
    )

    fig3.update_layout(
        height=450,
        showlegend=False,
        title=None,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="",
        yaxis_title="Records",
        font=dict(size=14)
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )
# Audits
elif page == "📋 Internal Audits":
    st.title("📋 Internal Audit Findings")

    finding = st.text_input("Finding")

    department = st.selectbox(
        "Department",
        ["QA", "Operations", "HR", "IT", "Finance"]
    )

    severity = st.selectbox(
        "Severity",
        ["Low", "Medium", "High", "Critical"]
    )

    due_date = st.date_input("Due Date")

    status = st.selectbox(
        "Status",
        ["Open", "In Progress", "Closed"]
    )

    if st.button("Save Finding"):

        conn = sqlite3.connect("compliance.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO audit_findings
            (finding, department, severity, due_date, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            finding,
            department,
            severity,
            str(due_date),
            status
        ))

        conn.commit()
        conn.close()

        st.success("Finding Saved Successfully!")

    st.subheader("Saved Findings")

    conn = sqlite3.connect("compliance.db")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM audit_findings")

    findings = cursor.fetchall()

    conn.close()

    df = pd.DataFrame(
        findings,
        columns=[
            "ID",
            "Finding",
            "Department",
            "Severity",
            "Due Date",
            "Status"
        ]
    )

    st.dataframe(df, use_container_width=True)

    today = date.today()

    overdue = []
    due_soon = []

    for _, row in df.iterrows():

        due_date = datetime.strptime(
            row["Due Date"],
            "%Y-%m-%d"
        ).date()

        days_left = (due_date - today).days

        if row["Status"] != "Closed":

            if days_left < 0:
                overdue.append(row["Finding"])

            elif days_left <= 7:
                due_soon.append(row["Finding"])

    st.subheader("🔔 Alerts")

    if overdue:

        st.error(
            f"{len(overdue)} overdue findings detected"
        )

        for item in overdue:
            st.write(f"🔴 {item}")

    if due_soon:

        st.warning(
            f"{len(due_soon)} findings due within 7 days"
        )

        for item in due_soon:
            st.write(f"🟠 {item}")
# Incidents
elif page == "⚠️ Incidents":

    st.title("⚠️ Incident Management")

    incident = st.text_input("Incident")

    department = st.selectbox(
        "Department",
        ["IT", "QA", "HR", "Operations", "Finance"],
        key="incident_department"
    )

    severity = st.selectbox(
        "Severity",
        ["Low", "Medium", "High", "Critical"],
        key="incident_severity"
    )

    due_date = st.date_input(
        "Due Date",
        key="incident_due_date"
    )

    status = st.selectbox(
        "Status",
        ["Open", "In Progress", "Closed"],
        key="incident_status"
    )

    if st.button("Save Incident"):

        conn = sqlite3.connect("compliance.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO incidents
        (incident, department, severity, due_date, status)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            incident,
            department,
            severity,
            str(due_date),
            status
        ))

        conn.commit()
        conn.close()

        st.success("Incident Saved Successfully!")
    st.subheader("Saved Incidents")

    conn = sqlite3.connect("compliance.db")

    incidents = pd.read_sql_query(
        "SELECT * FROM incidents",
        conn
    )

    conn.close()

    st.dataframe(
        incidents,
        use_container_width=True
    )
    today = date.today()

    overdue_incidents = []
    due_soon_incidents = []

    for _, row in incidents.iterrows():

        due_date = datetime.strptime(
            row["due_date"],
            "%Y-%m-%d"
        ).date()

        days_left = (due_date - today).days

        if row["status"] != "Closed":

            if days_left < 0:
                overdue_incidents.append(
                    row["incident"]
                )

            elif days_left <= 7:
                due_soon_incidents.append(
                    row["incident"]
                )
    st.subheader("🔔 Incident Alerts")

    if overdue_incidents:

        st.error(
            f"{len(overdue_incidents)} overdue incidents"
        )

        for item in overdue_incidents:
            st.write(f"🔴 {item}")

    if due_soon_incidents:

        st.warning(
            f"{len(due_soon_incidents)} incidents due within 7 days"
        )

        for item in due_soon_incidents:
            st.write(f"🟠 {item}")

# Employee Training
elif page == "🎓 Training":

    st.title("🎓 Employee Training")

    employee_id = st.text_input(
        "Employee ID"
    )

    employee_name = st.text_input(
        "Employee Name"
    )

    department = st.selectbox(
        "Department",
        [
            "QA",
            "Operations",
            "HR",
            "IT",
            "Finance"
        ],
        key="training_department"
    )

    training_name = st.text_input(
        "Training Name"
    )

    expiry_date = st.date_input(
        "Expiry Date"
    )

    status = st.selectbox(
        "Status",
        [
            "Valid",
            "Expiring Soon",
            "Expired"
        ],
        key="training_status"
    )

    if st.button("Save Training"):

        conn = sqlite3.connect(
            "compliance.db"
        )

        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO employee_training
        (
            employee_id,
            employee_name,
            department,
            training_name,
            expiry_date,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            employee_id,
            employee_name,
            department,
            training_name,
            str(expiry_date),
            status
        ))

        conn.commit()
        conn.close()

        st.success(
            "Training Saved Successfully!"
        )
    st.subheader(
        "Saved Training Records"
    )

    conn = sqlite3.connect(
        "compliance.db"
    )

    training_df = pd.read_sql_query(
        """
        SELECT *
        FROM employee_training
        """,
        conn
    )

    conn.close()

    st.dataframe(
        training_df,
        use_container_width=True
    )
    today = date.today()

    expired_training = []

    expiring_soon = []

    for _, row in training_df.iterrows():

        expiry = datetime.strptime(
            row["expiry_date"],
            "%Y-%m-%d"
        ).date()

        days_left = (
            expiry - today
        ).days

        if days_left < 0:

            expired_training.append(
                f"{row['employee_id']} - {row['training_name']}"
            )

        elif days_left <= 30:

            expiring_soon.append(
                f"{row['employee_id']} - {row['training_name']}"
            )
    st.subheader(
        "🎓 Training Alerts"
    )

    if expired_training:

        st.error(
            f"{len(expired_training)} expired trainings"
        )

        for item in expired_training:

            st.write(
                f"🔴 {item}"
            )

    if expiring_soon:

        st.warning(
            f"{len(expiring_soon)} trainings expiring within 30 days"
        )

        for item in expiring_soon:

            st.write(
                f"🟠 {item}"
            )

# Compliance Activities
elif page == "📅 Activities":

    st.title("📅 Compliance Activities")

    activity_name = st.text_input(
        "Activity Name"
    )

    owner = st.text_input(
        "Owner Employee ID"
    )

    department = st.selectbox(
        "Department",
        [
            "QA",
            "Operations",
            "HR",
            "IT",
            "Finance"
        ],
        key="activity_department"
    )

    due_date = st.date_input(
        "Due Date",
        key="activity_due_date"
    )

    status = st.selectbox(
        "Status",
        [
            "Planned",
            "In Progress",
            "Completed"
        ],
        key="activity_status"
    )

    if st.button("Save Activity"):

        conn = sqlite3.connect(
            "compliance.db"
        )

        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO compliance_activities
        (
            activity_name,
            owner,
            department,
            due_date,
            status
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            activity_name,
            owner,
            department,
            str(due_date),
            status
        ))
        conn.commit()
        conn.close()

        st.success(
            "Activity Saved Successfully!"
        )
    st.subheader(
        "Saved Activities"
    )

    conn = sqlite3.connect(
        "compliance.db"
    )

    activities_df = pd.read_sql_query(
        """
        SELECT *
        FROM compliance_activities
        """,
        conn
    )

    conn.close()

    st.dataframe(
        activities_df,
        use_container_width=True
    )
    today = date.today()

    overdue_activities = []

    due_soon_activities = []

    for _, row in activities_df.iterrows():

        due = datetime.strptime(
            row["due_date"],
            "%Y-%m-%d"
        ).date()

        days_left = (
            due - today
        ).days

        if row["status"] != "Completed":

            if days_left < 0:

                overdue_activities.append(
                    row["activity_name"]
                )

            elif days_left <= 7:

                due_soon_activities.append(
                    row["activity_name"]
                )
    st.subheader(
        "📅 Activity Alerts"
    )

    if overdue_activities:

        st.error(
            f"{len(overdue_activities)} overdue activities"
        )

        for item in overdue_activities:

            st.write(
                f"🔴 {item}"
            )

    if due_soon_activities:

        st.warning(
            f"{len(due_soon_activities)} activities due within 7 days"
        )

        for item in due_soon_activities:

            st.write(
                f"🟠 {item}"
            )

