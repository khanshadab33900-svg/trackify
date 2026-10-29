import os
import base64
import subprocess

def get_base64_img(file_path):
    if not os.path.exists(file_path):
        return ""
    ext = os.path.splitext(file_path)[1].lower().replace(".", "")
    if ext == "jpg":
        ext = "jpeg"
    with open(file_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/{ext};base64,{data}"

logo_cover = get_base64_img(r"docs\report_assets\page_1_img_1_Image21.jpg")
logo_cert = get_base64_img(r"docs\report_assets\page_2_img_1_Image24.png")
plag_badge = get_base64_img(r"docs\report_assets\page_7_img_1_Image37.jpg")

ss_login = get_base64_img(r"docs\screenshots\01_login_page.png")
ss_register = get_base64_img(r"docs\screenshots\02_register_page.png")
ss_dashboard = get_base64_img(r"docs\screenshots\03_analytics_dashboard.png")
ss_projects = get_base64_img(r"docs\screenshots\04_projects_management.png")
ss_tickets = get_base64_img(r"docs\screenshots\05_bug_tickets_directory.png")
ss_detail = get_base64_img(r"docs\screenshots\06_ticket_detail_and_discussion.png")
ss_form = get_base64_img(r"docs\screenshots\07_report_bug_form.png")

# Vector SVGs
svg_architecture = """
<svg width="100%" height="220" viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" style="font-family:'Times New Roman',serif;">
  <defs>
    <linearGradient id="gradTop" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#e0e7ff" />
      <stop offset="100%" stop-color="#ede9fe" />
    </linearGradient>
    <linearGradient id="gradMid" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#eff6ff" />
      <stop offset="100%" stop-color="#dbeafe" />
    </linearGradient>
    <linearGradient id="gradBot" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#f8fafc" />
      <stop offset="100%" stop-color="#e2e8f0" />
    </linearGradient>
    <marker id="arr" markerWidth="8" markerHeight="8" refX="5" refY="4" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 z" fill="#334155" />
    </marker>
  </defs>

  <!-- Presentation Layer -->
  <rect x="50" y="10" width="580" height="48" rx="6" fill="url(#gradTop)" stroke="#6366f1" stroke-width="1.5"/>
  <text x="340" y="30" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e1b4b">Users / Web Browser Interface (Presentation Layer)</text>
  <text x="340" y="47" text-anchor="middle" font-size="11" fill="#4338ca">Administrator Portal  •  Developer Lead Workspace  •  QA / Tester Reporting View</text>

  <!-- Line 1 to 2 -->
  <line x1="340" y1="58" x2="340" y2="82" stroke="#334155" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="355" y="73" font-size="10" fill="#475569">HTTP(S) Requests / JSON &amp; HTML Responses</text>

  <!-- Application Logic Layer -->
  <rect x="50" y="84" width="580" height="52" rx="6" fill="url(#gradMid)" stroke="#2563eb" stroke-width="1.5"/>
  <text x="340" y="105" text-anchor="middle" font-size="13" font-weight="bold" fill="#172554">Trackify Application Engine (Business &amp; Application Logic Layer)</text>
  <text x="340" y="123" text-anchor="middle" font-size="11" fill="#1e40af">Django 5.x / FastAPI  •  Role-Based Access Control  •  Defect Lifecycle State Machine  •  ORM Engine</text>

  <!-- Line 2 to 3 -->
  <line x1="340" y1="136" x2="340" y2="160" stroke="#334155" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="355" y="151" font-size="10" fill="#475569">SQL Queries, Migrations &amp; Relational Schema Mapping</text>

  <!-- Data Layer -->
  <rect x="50" y="162" width="580" height="48" rx="6" fill="url(#gradBot)" stroke="#64748b" stroke-width="1.5"/>
  <text x="340" y="182" text-anchor="middle" font-size="13" font-weight="bold" fill="#0f172a">Relational Database Layer (SQLite db.sqlite3 / trackify.db)</text>
  <text x="340" y="199" text-anchor="middle" font-size="11" fill="#334155">Users &amp; Roles  •  Software Projects  •  Bug Tickets &amp; Priorities  •  Technical Discussions  •  Audit Logs</text>
</svg>
"""

svg_dfd0 = """
<svg width="100%" height="210" viewBox="0 0 680 210" xmlns="http://www.w3.org/2000/svg" style="font-family:'Times New Roman',serif;">
  <defs>
    <marker id="arr2" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
      <path d="M 0 0 L 7 3.5 L 0 7 z" fill="#1e293b" />
    </marker>
  </defs>

  <!-- Central System Bubble -->
  <circle cx="340" cy="105" r="58" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
  <text x="340" y="98" text-anchor="middle" font-size="12" font-weight="bold" fill="#0369a1">0.0</text>
  <text x="340" y="112" text-anchor="middle" font-size="11" font-weight="bold" fill="#0369a1">Trackify Issue</text>
  <text x="340" y="125" text-anchor="middle" font-size="11" font-weight="bold" fill="#0369a1">Tracker System</text>

  <!-- Entity: QA Tester -->
  <rect x="20" y="80" width="120" height="50" rx="4" fill="#f8fafc" stroke="#334155" stroke-width="1.5"/>
  <text x="80" y="102" text-anchor="middle" font-size="11" font-weight="bold">QA Engineer</text>
  <text x="80" y="118" text-anchor="middle" font-size="10" fill="#64748b">/ Tester</text>

  <!-- Arrows QA -> System -->
  <line x1="140" y1="95" x2="278" y2="95" stroke="#1e293b" stroke-width="1.3" marker-end="url(#arr2)"/>
  <text x="210" y="88" text-anchor="middle" font-size="9" fill="#334155">Report Bug, Screenshots</text>
  
  <line x1="280" y1="115" x2="144" y2="115" stroke="#1e293b" stroke-width="1.3" marker-end="url(#arr2)"/>
  <text x="210" y="130" text-anchor="middle" font-size="9" fill="#334155">Ticket Status, History</text>

  <!-- Entity: Developer -->
  <rect x="280" y="5" width="120" height="42" rx="4" fill="#f8fafc" stroke="#334155" stroke-width="1.5"/>
  <text x="340" y="24" text-anchor="middle" font-size="11" font-weight="bold">Developer Lead</text>
  <text x="340" y="38" text-anchor="middle" font-size="9" fill="#64748b">Assigned Engineer</text>

  <!-- Arrows Developer <-> System -->
  <line x1="330" y1="47" x2="330" y2="47" stroke="#1e293b"/>
  <line x1="330" y1="47" x2="330" y2="88" stroke="#1e293b" stroke-width="1.3" marker-end="url(#arr2)"/>
  <text x="270" y="65" font-size="9" fill="#334155">Status Patch (In Progress / Resolved)</text>

  <!-- Entity: Administrator -->
  <rect x="540" y="80" width="120" height="50" rx="4" fill="#f8fafc" stroke="#334155" stroke-width="1.5"/>
  <text x="600" y="102" text-anchor="middle" font-size="11" font-weight="bold">Administrator</text>
  <text x="600" y="118" text-anchor="middle" font-size="10" fill="#64748b">System Manager</text>

  <!-- Arrows Admin <-> System -->
  <line x1="540" y1="95" x2="402" y2="95" stroke="#1e293b" stroke-width="1.3" marker-end="url(#arr2)"/>
  <text x="470" y="88" text-anchor="middle" font-size="9" fill="#334155">Projects, Assign Devs</text>

  <line x1="400" y1="115" x2="536" y2="115" stroke="#1e293b" stroke-width="1.3" marker-end="url(#arr2)"/>
  <text x="470" y="130" text-anchor="middle" font-size="9" fill="#334155">Analytics, Defect Logs</text>
</svg>
"""

svg_usecase = """
<svg width="100%" height="280" viewBox="0 0 680 280" xmlns="http://www.w3.org/2000/svg" style="font-family:'Times New Roman',serif;">
  <rect x="150" y="10" width="380" height="260" rx="8" fill="#fdfdfe" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="340" y="28" text-anchor="middle" font-size="12" font-weight="bold" fill="#334155">Trackify System Boundary</text>

  <!-- QA Tester Actor -->
  <circle cx="60" cy="50" r="12" fill="#e0e7ff" stroke="#4f46e5" stroke-width="1.5"/>
  <line x1="60" y1="62" x2="60" y2="92" stroke="#4f46e5" stroke-width="1.5"/>
  <line x1="40" y1="74" x2="80" y2="74" stroke="#4f46e5" stroke-width="1.5"/>
  <line x1="60" y1="92" x2="45" y2="115" stroke="#4f46e5" stroke-width="1.5"/>
  <line x1="60" y1="92" x2="75" y2="115" stroke="#4f46e5" stroke-width="1.5"/>
  <text x="60" y="130" text-anchor="middle" font-size="11" font-weight="bold">QA Tester</text>

  <!-- Developer Actor -->
  <circle cx="60" cy="180" r="12" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
  <line x1="60" y1="192" x2="60" y2="222" stroke="#16a34a" stroke-width="1.5"/>
  <line x1="40" y1="204" x2="80" y2="204" stroke="#16a34a" stroke-width="1.5"/>
  <line x1="60" y1="222" x2="45" y2="245" stroke="#16a34a" stroke-width="1.5"/>
  <line x1="60" y1="222" x2="75" y2="245" stroke="#16a34a" stroke-width="1.5"/>
  <text x="60" y="260" text-anchor="middle" font-size="11" font-weight="bold">Developer Lead</text>

  <!-- Admin Actor -->
  <circle cx="620" cy="110" r="12" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
  <line x1="620" y1="122" x2="620" y2="152" stroke="#d97706" stroke-width="1.5"/>
  <line x1="600" y1="134" x2="640" y2="134" stroke="#d97706" stroke-width="1.5"/>
  <line x1="620" y1="152" x2="605" y2="175" stroke="#d97706" stroke-width="1.5"/>
  <line x1="620" y1="152" x2="635" y2="175" stroke="#d97706" stroke-width="1.5"/>
  <text x="620" y="190" text-anchor="middle" font-size="11" font-weight="bold">Administrator</text>

  <!-- Use Cases (Ovals) -->
  <!-- UC1 -->
  <ellipse cx="250" cy="55" rx="70" ry="16" fill="#f1f5f9" stroke="#64748b"/>
  <text x="250" y="58" text-anchor="middle" font-size="10">Register / 1-Click Login</text>
  <line x1="85" y1="55" x2="180" y2="55" stroke="#94a3b8"/>

  <!-- UC2 -->
  <ellipse cx="250" cy="100" rx="70" ry="16" fill="#f1f5f9" stroke="#64748b"/>
  <text x="250" y="103" text-anchor="middle" font-size="10">Report Defect / Bug</text>
  <line x1="85" y1="75" x2="182" y2="98" stroke="#94a3b8"/>

  <!-- UC3 -->
  <ellipse cx="250" cy="145" rx="70" ry="16" fill="#f1f5f9" stroke="#64748b"/>
  <text x="250" y="148" text-anchor="middle" font-size="10">Filter &amp; View Directory</text>
  <line x1="85" y1="90" x2="183" y2="140" stroke="#94a3b8"/>
  <line x1="85" y1="200" x2="183" y2="150" stroke="#94a3b8"/>

  <!-- UC4 -->
  <ellipse cx="250" cy="190" rx="70" ry="16" fill="#f1f5f9" stroke="#64748b"/>
  <text x="250" y="193" text-anchor="middle" font-size="10">Update Bug Status</text>
  <line x1="85" y1="210" x2="182" y2="193" stroke="#94a3b8"/>

  <!-- UC5 -->
  <ellipse cx="250" cy="235" rx="70" ry="16" fill="#f1f5f9" stroke="#64748b"/>
  <text x="250" y="238" text-anchor="middle" font-size="10">Post Technical Comments</text>
  <line x1="85" y1="225" x2="185" y2="235" stroke="#94a3b8"/>

  <!-- UC6 Admin -->
  <ellipse cx="430" cy="80" rx="70" ry="16" fill="#f1f5f9" stroke="#64748b"/>
  <text x="430" y="83" text-anchor="middle" font-size="10">Create Software Project</text>
  <line x1="595" y1="125" x2="498" y2="87" stroke="#94a3b8"/>

  <!-- UC7 Admin -->
  <ellipse cx="430" cy="130" rx="70" ry="16" fill="#f1f5f9" stroke="#64748b"/>
  <text x="430" y="133" text-anchor="middle" font-size="10">Assign Developer to Bug</text>
  <line x1="595" y1="135" x2="502" y2="132" stroke="#94a3b8"/>

  <!-- UC8 Admin -->
  <ellipse cx="430" cy="180" rx="70" ry="16" fill="#f1f5f9" stroke="#64748b"/>
  <text x="430" y="183" text-anchor="middle" font-size="10">View Analytics &amp; KPIs</text>
  <line x1="595" y1="145" x2="498" y2="175" stroke="#94a3b8"/>

  <!-- UC9 Admin -->
  <ellipse cx="430" cy="225" rx="70" ry="16" fill="#f1f5f9" stroke="#64748b"/>
  <text x="430" y="228" text-anchor="middle" font-size="10">Manage RBAC Roles</text>
  <line x1="595" y1="160" x2="495" y2="220" stroke="#94a3b8"/>
</svg>
"""

svg_er = """
<svg width="100%" height="270" viewBox="0 0 680 270" xmlns="http://www.w3.org/2000/svg" style="font-family:'Times New Roman',serif;">
  <defs>
    <marker id="crow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M 0 1 L 8 5 L 0 9 M 0 5 L 8 5" fill="none" stroke="#334155" stroke-width="1.3"/>
    </marker>
  </defs>

  <!-- Table 1: User -->
  <rect x="20" y="15" width="180" height="110" rx="4" fill="#ffffff" stroke="#2563eb" stroke-width="1.5"/>
  <rect x="20" y="15" width="180" height="24" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
  <text x="110" y="31" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e40af">tracker_user</text>
  <text x="30" y="52" font-size="10" font-weight="bold">PK  id (INTEGER)</text>
  <text x="30" y="68" font-size="10">    username (VARCHAR)</text>
  <text x="30" y="84" font-size="10">    password (VARCHAR)</text>
  <text x="30" y="100" font-size="10">    role (admin/dev/tester)</text>
  <text x="30" y="116" font-size="10">    email (VARCHAR)</text>

  <!-- Table 2: Project -->
  <rect x="20" y="150" width="180" height="100" rx="4" fill="#ffffff" stroke="#059669" stroke-width="1.5"/>
  <rect x="20" y="150" width="180" height="24" fill="#d1fae5" stroke="#059669" stroke-width="1.5"/>
  <text x="110" y="166" text-anchor="middle" font-size="11" font-weight="bold" fill="#065f46">tracker_project</text>
  <text x="30" y="188" font-size="10" font-weight="bold">PK  id (INTEGER)</text>
  <text x="30" y="204" font-size="10">    name (VARCHAR)</text>
  <text x="30" y="220" font-size="10">    description (TEXT)</text>
  <text x="30" y="236" font-size="10">    status (active/archived)</text>

  <!-- Table 3: Ticket -->
  <rect x="260" y="45" width="190" height="180" rx="4" fill="#ffffff" stroke="#dc2626" stroke-width="1.5"/>
  <rect x="260" y="45" width="190" height="24" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
  <text x="355" y="61" text-anchor="middle" font-size="11" font-weight="bold" fill="#991b1b">tracker_ticket</text>
  <text x="270" y="82" font-size="10" font-weight="bold">PK  id (INTEGER)</text>
  <text x="270" y="98" font-size="10">    title (VARCHAR)</text>
  <text x="270" y="114" font-size="10">    description (TEXT)</text>
  <text x="270" y="130" font-size="10">    priority (low/med/high)</text>
  <text x="270" y="146" font-size="10">    status (open/prog/res)</text>
  <text x="270" y="162" font-size="10" fill="#047857">FK  project_id (INT)</text>
  <text x="270" y="178" font-size="10" fill="#1d4ed8">FK  creator_id (INT)</text>
  <text x="270" y="194" font-size="10" fill="#1d4ed8">FK  assigned_dev_id (INT)</text>
  <text x="270" y="210" font-size="10">    created_at (DATETIME)</text>

  <!-- Table 4: Comment -->
  <rect x="500" y="85" width="170" height="110" rx="4" fill="#ffffff" stroke="#7c3aed" stroke-width="1.5"/>
  <rect x="500" y="85" width="170" height="24" fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5"/>
  <text x="585" y="101" text-anchor="middle" font-size="11" font-weight="bold" fill="#5b21b6">tracker_comment</text>
  <text x="510" y="122" font-size="10" font-weight="bold">PK  id (INTEGER)</text>
  <text x="510" y="138" font-size="10" fill="#b91c1c">FK  ticket_id (INT)</text>
  <text x="510" y="154" font-size="10" fill="#1d4ed8">FK  user_id (INT)</text>
  <text x="510" y="170" font-size="10">    content (TEXT)</text>
  <text x="510" y="186" font-size="10">    created_at (DATETIME)</text>

  <!-- Relationships -->
  <!-- User -> Ticket (1:N) -->
  <line x1="200" y1="80" x2="258" y2="80" stroke="#334155" stroke-width="1.3" marker-end="url(#crow)"/>
  <text x="225" y="73" font-size="9" fill="#475569">1 : N</text>

  <!-- Project -> Ticket (1:N) -->
  <line x1="200" y1="180" x2="258" y2="160" stroke="#334155" stroke-width="1.3" marker-end="url(#crow)"/>
  <text x="225" y="165" font-size="9" fill="#475569">1 : N</text>

  <!-- Ticket -> Comment (1:N) -->
  <line x1="450" y1="135" x2="498" y2="135" stroke="#334155" stroke-width="1.3" marker-end="url(#crow)"/>
  <text x="470" y="128" font-size="9" fill="#475569">1 : N</text>
</svg>
"""

print("SVGs prepared successfully.")
