import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
import datetime


def get_dashboard_file(role):
    mapping = {
        "Admin": "pages/5_Admin.py",
        "Operations Manager": "pages/1_Operations_Manager.py",
        "Executive Director": "pages/2_Executive_Director.py",
        "Analyst": "pages/3_Analyst.py",
        "Technician": "pages/4_Technician.py"
    }
    return mapping.get(role, "pages/Home.py")

def show_navbar():
    role = st.session_state.get("current_role", "")

    pages = [{"label": "Dashboard", "target": get_dashboard_file(role)}]

    if role != "Analyst":
        pages.append({"label": "Tasks", "target": "pages/8_Tasks.py"})
    if role != "Technician":
        pages.append({"label": "Reports", "target": "pages/7_Reports.py"})

    pages.append({"label": "Alerts", "target": "pages/6_Alerts.py"})
    pages.append({"label": "Profile", "target": "pages/9_Profile.py"})
    pages.append({"label": "Logout", "target": "logout"})

    st.markdown('<div class="navbar">', unsafe_allow_html=True)

    cols = st.columns(len(pages))
    for i, p in enumerate(pages):
        with cols[i]:
            if st.button(p["label"], use_container_width=True):
                if p["target"] == "logout":
                    st.session_state.show_logout_modal = True
                else:
                    st.switch_page(p["target"])

    if st.session_state.get("show_logout_modal", False):
        st.markdown("""
            <div class="logout-modal">
                <h4>Are you sure you want to logout?</h4>
            """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Yes, logout"):
                st.session_state.clear()
                st.switch_page("Home.py")
        with col2:
            if st.button("Cancel"):
                st.session_state.show_logout_modal = False

        st.markdown("</div>", unsafe_allow_html=True)



def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def generate_work_order_pdf():
    """Generate a PDF work order for the current task"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=12,
        spaceBefore=12
    )
    normal_style = styles['Normal']
    
    # Title
    story.append(Paragraph("WORK ORDER", title_style))
    story.append(Spacer(1, 20))
    
    # Task Information
    story.append(Paragraph("Task Information", heading_style))
    
    task_data = [
        ["Task ID:", "WT-2025-001"],
        ["Task Title:", "Wind Turbine Inspection"],
        ["Priority:", "High (4/5)"],
        ["Status:", st.session_state.get('task_status', 'Pending')],
        ["Due Date:", "2025-06-20 14:30"],
        ["Created:", "2025-06-15 09:00"],
        ["Assigned To:", "John Smith"],
        ["Location:", "Wind Farm A, Turbine 23"],
        ["Estimated Duration:", "2 hours"]
    ]
    
    task_table = Table(task_data, colWidths=[2*inch, 4*inch])
    task_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.grey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(task_table)
    story.append(Spacer(1, 20))
    
    # Required Tools
    story.append(Paragraph("Required Tools", heading_style))
    tools_data = [
        ["Tool", "Quantity", "Location"],
        ["Multimeter", "1", "Toolbox A"],
        ["Safety harness", "1", "Safety equipment room"],
        ["High-temperature grease", "500ml", "Warehouse B"],
        ["Bearing puller", "1", "Toolbox A"]
    ]
    
    tools_table = Table(tools_data, colWidths=[2*inch, 1.5*inch, 2.5*inch])
    tools_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(tools_table)
    story.append(Spacer(1, 20))
    
    # Work Instructions
    story.append(Paragraph("Work Instructions", heading_style))
    instructions = [
        "1. Perform safety check and wear appropriate PPE",
        "2. Inspect bearing temperature and vibration levels",
        "3. Check for phase imbalance in electrical system",
        "4. Apply lubrication if temperature exceeds 75°C",
        "5. Monitor parameters for 30 minutes after lubrication",
        "6. Document all readings and actions taken",
        "7. Update task status upon completion"
    ]
    
    for instruction in instructions:
        story.append(Paragraph(instruction, normal_style))
    
    story.append(Spacer(1, 20))
    
    # Notes Section
    story.append(Paragraph("Notes", heading_style))
    story.append(Paragraph("Check phase imbalance – similar to 2025-04 incident", normal_style))
    story.append(Paragraph("Reference attachment: sensor_readings_023.csv", normal_style))
    
    story.append(Spacer(1, 20))
    
    # Footer
    story.append(Paragraph(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    story.append(Paragraph("Rayfield Systems - Work Order Management System", normal_style))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer


load_css()
show_navbar()


st.set_page_config(
    page_title="📋 Task Manager",
    layout="wide"
)

# Auth check
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("Please login to view this page")
    st.stop()

# Page Title
st.title("🗓️ Task Calendar")

# Calendar Header
st.markdown("#### June 2025 | June 16 – 22")
st.divider()

# Initialize task status in session state if not exists
if 'task_status' not in st.session_state:
    st.session_state.task_status = "Pending"

# Top-level Buttons
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Print Work Order", use_container_width=True):
        try:
            pdf_buffer = generate_work_order_pdf()
            st.download_button(
                label="📄 Download Work Order PDF",
                data=pdf_buffer.getvalue(),
                file_name=f"work_order_WT-2025-001_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
            st.success("Work order PDF generated successfully!")
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")
with col2:
    st.file_uploader("Upload New", type=["pdf", "csv"], label_visibility="collapsed")
with col3:
    if st.button("Notify Technician", use_container_width=True):
        st.success("Technician notification sent!")
with col4:
    if st.button("Cancel Task", use_container_width=True):
        st.session_state.task_status = "Cancelled"
        st.warning("Task cancelled successfully! Status updated to 'Cancelled'")

st.markdown("---")

# Task Card
st.subheader("Wind Turbine Inspection")
st.markdown(f"""
<div class="metric-card">
    <p><strong>Status:</strong> <span style="color: {'red' if st.session_state.task_status == 'Cancelled' else 'orange' if st.session_state.task_status == 'In Progress' else 'green'}">{st.session_state.task_status}</span></p>
    <p><strong>Priority:</strong> High (4/5)</p>
    <p><strong>Due:</strong> 2025-06-20 14:30</p>
    <p><strong>Notes:</strong> Check phase imbalance – similar to 2025-04 incident</p>
    <p><strong>Attachments:</strong></p>
    <ul>
        <li>sensor_readings_023.csv</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Task Actions
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Start Task", use_container_width=True, disabled=st.session_state.task_status == "Cancelled"):
        st.session_state.task_status = "In Progress"
        st.success("Task started! Status updated to 'In Progress'")
with col2:
    if st.button("Add Notes", use_container_width=True):
        st.session_state.show_notes_form = True
with col3:
    if st.button("View Details", use_container_width=True):
        st.session_state.show_task_details = True

# Notes form
if st.session_state.get("show_notes_form", False):
    st.markdown("### Add Notes")
    notes = st.text_area("Enter your notes:", height=100)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save Notes"):
            st.success("Notes saved successfully!")
            st.session_state.show_notes_form = False
    with col2:
        if st.button("Cancel"):
            st.session_state.show_notes_form = False

# Task details
if st.session_state.get("show_task_details", False):
    st.markdown("### Task Details")
    st.markdown("""
    **Task ID:** WT-2025-001  
    **Created:** 2025-06-15 09:00  
    **Assigned To:** John Smith  
    **Location:** Wind Farm A, Turbine 23  
    **Estimated Duration:** 2 hours  
    **Required Tools:** Multimeter, Safety harness  
    **Previous Issues:** Phase imbalance detected on 2025-04-15
    """)
    
    # Notes History Section
    st.markdown("### Notes History")
    st.markdown("""
    **2025-06-16 14:30 - John Smith:**  
    Initial inspection completed. Bearing temperature reading 89°C, which is 14°C above normal. Vibration levels at 7.2mm/s. Recommend immediate lubrication and monitoring.
    
    **2025-06-16 15:45 - Sarah Johnson:**  
    Applied high-temperature grease to bearing housing. Temperature dropped to 82°C within 30 minutes. Vibration reduced to 5.8mm/s. Will continue monitoring.
    
    **2025-06-17 09:15 - John Smith:**  
    Follow-up inspection shows stable conditions. Temperature at 78°C, vibration at 5.2mm/s. Bearing appears to be responding well to lubrication. Scheduled for re-inspection in 48 hours.
    
    **2025-06-17 16:20 - Mike Wilson:**  
    Completed final inspection. All parameters within normal range. Temperature: 75°C, Vibration: 4.8mm/s. Task completed successfully. No further action required.
    """)
    
    if st.button("Close Details"):
        st.session_state.show_task_details = False

