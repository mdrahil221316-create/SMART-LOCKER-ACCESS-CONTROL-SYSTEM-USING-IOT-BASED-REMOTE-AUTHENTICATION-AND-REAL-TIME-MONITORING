"""
Script to generate the comprehensive Word document report for the Smart Locker System
following the evaluation criteria (PC1-PC9) and formatting requirements.
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
import os

def create_report():
    doc = Document()
    
    # Define styles
    styles = doc.styles
    
    # Chapter Title Style (Centered, Bold, Uppercase)
    chapter_style = styles.add_style('Chapter Title', WD_STYLE_TYPE.PARAGRAPH)
    chapter_font = chapter_style.font
    chapter_font.name = 'Times New Roman'
    chapter_font.size = Pt(14)
    chapter_font.bold = True
    chapter_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    chapter_style.paragraph_format.space_after = Pt(24)
    
    # Heading 1 Style (1.1, 1.2)
    h1_style = styles['Heading 1']
    h1_font = h1_style.font
    h1_font.name = 'Times New Roman'
    h1_font.size = Pt(12)
    h1_font.bold = True
    h1_font.color.rgb = RGBColor(0, 0, 0)
    
    # Heading 2 Style (1.1.1, 1.1.2)
    h2_style = styles['Heading 2']
    h2_font = h2_style.font
    h2_font.name = 'Times New Roman'
    h2_font.size = Pt(12)
    h2_font.bold = True
    h2_font.italic = True
    h2_font.color.rgb = RGBColor(0, 0, 0)
    
    # Normal Text Style
    normal_style = styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Times New Roman'
    normal_font.size = Pt(12)
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_after = Pt(12)

    # --- COVER PAGE ---
    doc.add_paragraph('\n\n\n\n')
    title = doc.add_paragraph('INTERNSHIP REPORT\nON\nSMART LOCKER ACCESS CONTROL SYSTEM USING IOT-BASED REMOTE AUTHENTICATION AND REAL-TIME MONITORING', style='Chapter Title')
    title.runs[0].font.size = Pt(16)
    
    doc.add_paragraph('\n\n')
    submitted_by = doc.add_paragraph('Submitted by:\nInternship Project Team', style='Normal')
    submitted_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_page_break()

    # --- TABLE OF CONTENTS ---
    doc.add_paragraph('TABLE OF CONTENTS', style='Chapter Title')
    
    toc_entries = [
        ("1", "EXECUTIVE SUMMARY", "1"),
        ("1.1", "Learning Objectives", "1"),
        ("1.2", "Outcomes Achieved", "2"),
        ("2", "OVERVIEW OF THE ORGANIZATION", "3"),
        ("2.1", "Introduction of the Organization", "3"),
        ("2.2", "Vision, Mission, and Values", "3"),
        ("2.3", "Policy of the Organization in Relation to the Intern Role", "4"),
        ("2.4", "Organizational Structure", "4"),
        ("2.5", "Roles and Responsibilities of the Employees Guiding the Intern", "5"),
        ("3", "PROBLEM ASSESSMENT", "6"),
        ("3.1", "Problem Statement", "6"),
        ("3.2", "Key Parameters (PC1)", "7"),
        ("3.3", "Requirements Evaluation (PC2)", "8"),
        ("4", "SOLUTION DESIGN", "10"),
        ("4.1", "Solution Blueprint (PC3)", "10"),
        ("4.2", "Feasibility Assessment", "12"),
        ("4.3", "Project Implementation Plan (PC4)", "13"),
        ("5", "TECHNOLOGY STACK", "15"),
        ("5.1", "Technology Selection (PC5)", "15"),
        ("5.2", "Architecture Overview", "16"),
        ("6", "SOLUTION DEVELOPMENT", "18"),
        ("6.1", "Implementation Details (PC6)", "18"),
        ("6.2", "IoT Authentication Module", "20"),
        ("6.3", "Security Monitoring and Analytics", "22"),
        ("7", "SOLUTION TESTING AND PERFORMANCE", "24"),
        ("7.1", "Testing Strategy (PC7)", "24"),
        ("7.2", "Bug Fixing and Issue Resolution", "25"),
        ("7.3", "Performance Evaluation (PC8)", "26"),
        ("8", "RESULTS AND VISUALIZATIONS", "28"),
        ("8.1", "Access Pattern and Success Rates", "28"),
        ("8.2", "Security Alerts and Occupancy", "29"),
        ("8.3", "System Security Dashboard", "30"),
        ("9", "LEARNING EVALUATION", "32"),
        ("9.1", "Technical Skill Gain (PC9)", "32"),
        ("9.2", "Conclusion", "33")
    ]
    
    for num, title, page in toc_entries:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        if "." not in num:
            run = p.add_run(f"{num}\t{title}")
            run.bold = True
        else:
            p.add_run(f"\t{num}\t{title}")
    
    doc.add_page_break()

    # Helper function to add a chapter
    def add_chapter(num, title):
        doc.add_paragraph(f'CHAPTER {num}', style='Chapter Title')
        doc.add_paragraph(title, style='Chapter Title')

    # Helper function to add content
    def add_content(text):
        for paragraph in text.split('\n\n'):
            if paragraph.strip():
                doc.add_paragraph(paragraph.strip(), style='Normal')

    # --- CHAPTER 1 ---
    add_chapter("1", "EXECUTIVE SUMMARY")
    
    add_content("""This internship report provides a comprehensive overview of my 8-week Short-Term Internship in developing a Smart Locker Access Control System. The internship was undertaken as part of the academic curriculum. The primary objective of this internship was to gain proficiency in Internet of Things (IoT) security, remote authentication mechanisms, and real-time monitoring to address vulnerabilities in traditional physical storage systems.

Secure storage of valuable items is essential in homes, offices, educational institutions, banks, and commercial facilities. Traditional locker systems rely on physical keys or password-based locks, which are vulnerable to key loss, unauthorized access, and limited monitoring capabilities. This project successfully addresses these limitations by providing an intelligent system that enables secure locker access using IoT-based remote authentication (RFID, Biometric, Mobile App) and real-time monitoring.""")
    
    doc.add_heading('1.1 Learning Objectives', level=1)
    add_content("""During my internship, I learned and practiced the following:
• To design and implement a secure locker management simulation using Python that models authentication workflows, access logging, and threat detection.
• To integrate simulated IoT authentication devices (RFID readers, Biometric scanners, Mobile App tokens) with varying success rates and confidence scoring.
• To develop security algorithms capable of detecting brute force attacks, unauthorized access attempts, and physical tampering.
• To create interactive data visualizations using Matplotlib and Seaborn to display access patterns, security alerts, and system health.
• To understand the software development lifecycle from security requirements gathering to testing and performance evaluation.""")

    doc.add_heading('1.2 Outcomes Achieved', level=1)
    add_content("""Key outcomes from my internship include:
• A fully operational simulation of a Smart Locker Access Control System capable of managing multiple lockers and users simultaneously.
• An advanced security monitoring module that generates instant alerts for network failures, low batteries, and forced entry attempts.
• Successful implementation of multi-modal authentication logic (RFID, Fingerprint, Mobile App, PIN) with realistic error rates and response times.
• Professional dashboards and visualizations that help security administrators monitor access logs and investigate suspicious activities.
• Comprehensive documentation of the system architecture, technology stack, and testing procedures.""")

    doc.add_page_break()

    # --- CHAPTER 2 ---
    add_chapter("2", "OVERVIEW OF THE ORGANIZATION")
    
    doc.add_heading('2.1 Introduction of the Organization', level=1)
    add_content("""The organization where this internship was conducted focuses on bridging the academia-industry divide, enhancing student employability, promoting innovation, and fostering an entrepreneurial ecosystem. By leveraging emerging technologies such as IoT, cybersecurity, and AI, the organization aims to augment and upgrade the knowledge ecosystem, enabling beneficiaries to become contributors themselves. The organization offers both online and instructor-led programs, benefiting thousands of learners annually.""")
    
    doc.add_heading('2.2 Vision, Mission, and Values', level=1)
    add_content("""• Vision: To combine cutting-edge technology with impactful social ventures to drive technological prosperity and secure digital infrastructure.
• Mission: To support individuals dedicated to helping others by empowering and equipping them with modern technical skills, thereby creating an extensive educational network dedicated to societal betterment and security.
• Values: The organization emphasizes technological skills for Industry 4.0, meta-human competencies for the future, and inclusive access for everyone to be future-ready.""")
    
    doc.add_heading('2.3 Policy of the Organization in Relation to the Intern Role', level=1)
    add_content("""The organization encourages internships as a means to foster learning and contribute to the mission. Interns are expected to adhere to the following policies:
• Confidentiality: Interns must maintain the strict confidentiality of all organizational data, especially concerning security protocols and authentication logic.
• Professionalism: Interns are expected to demonstrate professionalism, punctuality, and respect for all team members.
• Learning and Contribution: Interns are encouraged to actively participate in projects, share ideas, and contribute to the organization's goals.""")

    doc.add_heading('2.4 Organizational Structure', level=1)
    add_content("""The organization operates under a hierarchical structure with the following key roles:
• Board of Directors: Provides strategic direction and oversight.
• Executive Director: Oversees day-to-day operations and implementation of programs.
• Program Managers: Lead specific initiatives and technology projects.
• Technical Mentors: Guide interns in software development and project execution.
• Interns: Work under the guidance of mentors and contribute to ongoing projects.""")

    doc.add_heading('2.5 Roles and Responsibilities of the Employees Guiding the Intern', level=1)
    add_content("""Interns are typically placed under the guidance of technical mentors or project managers. The roles and responsibilities of these guiding employees include:
1. Project Managers: Design and implement projects, coordinate with stakeholders, and define project scopes.
2. Technical Mentors: Supervise interns, review code, provide technical assistance, and conduct performance evaluations.
3. Security Analysts: Provide domain knowledge regarding encryption, authentication protocols, and threat modeling.""")

    doc.add_page_break()

    # --- CHAPTER 3 ---
    add_chapter("3", "PROBLEM ASSESSMENT")
    
    doc.add_heading('3.1 Problem Statement', level=1)
    add_content("""Secure storage of valuable items is essential in homes, offices, educational institutions, banks, and commercial facilities. Traditional locker systems rely on physical keys or password-based locks, which are vulnerable to key loss, unauthorized access, and limited monitoring capabilities. Users require intelligent systems that provide secure remote authentication, continuous access monitoring, and instant notifications to enhance locker security.

The proposed solution is a Smart Locker Access Control System that enables secure locker access using IoT-based remote authentication and real-time monitoring. The system provides a centralized platform where locker status and user authentication are managed through a secure and user-friendly interface.""")
    
    doc.add_heading('3.2 Key Parameters (PC1)', level=1)
    add_content("""In accordance with the evaluation criteria (PC1), the key parameters of the problem have been identified as follows:

Issue to be Solved: The reliance on physical keys (which can be lost or duplicated) and static PINs (which can be shared or guessed), combined with a total lack of audit trails for when and by whom a locker was accessed.

Target Community: The target community includes bank administrators, gym/spa facility managers, university campus security, warehouse operators, and residential complex managers.

User Needs and Preferences:
• Administrators need centralized control to grant or revoke access instantly without changing physical locks.
• Users prefer frictionless access using their mobile phones or biometrics rather than carrying physical keys.
• Security teams require real-time alerts for forced entry, tampering, or repeated failed access attempts (brute force).
• Auditors require immutable logs detailing every successful and failed access attempt.

Security Impact: By digitizing access control and implementing multi-modal authentication, the system drastically reduces the attack surface associated with physical locks, directly enhancing asset protection.""")

    doc.add_heading('3.3 Requirements Evaluation (PC2)', level=1)
    add_content("""In accordance with the evaluation criteria (PC2), the requirements have been evaluated and mapped to the problem statement:

Functional Requirements:
1. Multi-modal Authentication: The system must support RFID, Biometric (Fingerprint), Mobile App, and PIN authentication.
2. Real-time Monitoring: The system must track locker status (Locked, Unlocked, Open, Tampered) and occupancy.
3. Threat Detection: The system must detect and alert on brute force attempts (e.g., 5 failed attempts in 5 minutes) and physical tampering.
4. Audit Logging: The system must record every access attempt, including user ID, timestamp, method, and success/failure status.

Non-Functional Requirements:
1. Scalability: The architecture must support managing hundreds of lockers and thousands of users.
2. Reliability: The system must handle network disconnections gracefully, generating alerts while maintaining physical security.
3. Accuracy: Biometric and RFID simulations must reflect realistic false acceptance/rejection rates.
4. Security: User data and authentication templates must be securely hashed.

Mapping to Problem Statement:
The functional requirements directly address the "vulnerable to key loss, unauthorized access, and limited monitoring" by providing secure remote authentication and continuous access monitoring as outlined in the problem statement.""")

    doc.add_page_break()

    # --- CHAPTER 4 ---
    add_chapter("4", "SOLUTION DESIGN")
    
    doc.add_heading('4.1 Solution Blueprint (PC3)', level=1)
    add_content("""In accordance with the evaluation criteria (PC3), a comprehensive solution blueprint has been designed for the Smart Locker Access Control System.

The solution utilizes a three-layer architecture:
1. Perception/Edge Layer (IoT Devices): This layer consists of the physical smart lockers equipped with electronic deadbolts, RFID readers, biometric scanners, tamper switches, and battery monitors.
2. Network Layer: This layer handles the secure transmission of authentication requests from the edge devices to the central server, and access granted/denied commands back to the lockers.
3. Application Layer: This layer contains the core business logic, user database, security monitoring engine, and analytics dashboards.

Core Modules Designed:
• LockerManagementSystem Module: The central hub that orchestrates users, lockers, and access requests.
• SmartLocker Module: Simulates individual lockers, tracking status, battery, and processing authentication requests.
• Authentication Module: Simulates the specific behaviors, success rates, and confidence scoring of RFID, Biometric, and Mobile authenticators.
• SecurityMonitor Module: Analyzes access logs in real-time to detect brute force attacks and unauthorized access.""")

    doc.add_heading('4.2 Feasibility Assessment', level=1)
    add_content("""Technical Feasibility: The solution is technically feasible. The use of Python for simulation and security logic is an industry standard. Cryptographic hashing (SHA-256) used for biometric templates and the object-oriented design for different authentication methods represent best practices.

Economic Feasibility: The software solution is highly cost-effective. In a real-world deployment, retrofitting existing lockers with IoT electronic locks is significantly cheaper than replacing entire locker banks. The reduction in administrative overhead (managing lost keys, rekeying locks) provides a rapid return on investment.

Operational Feasibility: The system is designed to drastically improve operational efficiency. By centralizing access management, administrators can onboard/offboard users instantly via software, eliminating the physical key management lifecycle.""")

    doc.add_heading('4.3 Project Implementation Plan (PC4)', level=1)
    add_content("""In accordance with the evaluation criteria (PC4), the project implementation plan was developed encompassing milestones, deadlines, and resource allocation over the 8-week internship period.

Phase 1: Requirements Gathering and Security Design (Weeks 1-2)
• Milestone 1: Finalize problem statement, authentication methods, and threat models.
• Milestone 2: Design system architecture, class diagrams, and database schemas.
• Resources: Technical mentor, security analyst, design documentation.

Phase 2: Core System and Authentication Development (Weeks 3-4)
• Milestone 3: Develop the SmartLocker and User classes.
• Milestone 4: Implement the RFID, Biometric, and Mobile authentication modules with realistic error rates.
• Resources: Python development environment, hashlib library.

Phase 3: Security Monitoring and Threat Detection (Weeks 5-6)
• Milestone 5: Develop the SecurityMonitor to detect brute force attacks and physical tampering.
• Milestone 6: Implement comprehensive access logging and alert generation.
• Resources: Python development environment, testing frameworks.

Phase 4: Analytics, Visualization, and Documentation (Weeks 7-8)
• Milestone 7: Develop the LockerAnalytics module using Matplotlib/Seaborn to visualize access patterns.
• Milestone 8: Generate all visualization charts and compile the final internship report.
• Resources: Data visualization libraries, word processing software.""")

    doc.add_page_break()

    # --- CHAPTER 5 ---
    add_chapter("5", "TECHNOLOGY STACK")
    
    doc.add_heading('5.1 Technology Selection (PC5)', level=1)
    add_content("""In accordance with the evaluation criteria (PC5), a robust technology stack was determined to build the proposed solution.

Programming Language: Python 3.12
Python was selected as the primary programming language due to its extensive support for object-oriented programming, data analytics, and built-in cryptographic libraries. Its readability makes it ideal for developing complex authentication logic.

Data Visualization Libraries:
• Matplotlib: Chosen for its powerful 2D plotting capabilities, allowing for the creation of detailed bar charts, pie charts, and histograms for security data.
• Seaborn: Selected to enhance Matplotlib visuals with attractive default styles and color palettes, specifically used for statistical data visualization.

Security and Data Manipulation:
• Hashlib: Utilized for secure hashing (SHA-256) of simulated biometric templates, ensuring sensitive user data is not stored in plaintext.
• NumPy: Utilized for efficient numerical operations and array manipulations.
• JSON: Used for data serialization and exporting audit logs, facilitating potential integration with SIEM (Security Information and Event Management) systems.

Development Tools:
• Standard Python logging module for tracking system operations and security events.
• Dataclasses for structured data representation (AccessLog, SecurityAlert, AuthenticationAttempt).""")

    doc.add_heading('5.2 Architecture Overview', level=1)
    add_content("""The software architecture follows a modular, object-oriented design with a strong focus on separation of concerns:

1. Data Models (Dataclasses): Define the strict structure of User, AccessLog, SecurityAlert, and AuthenticationAttempt to ensure data integrity.
2. Authentication Engine: The `RFIDAuthenticator`, `BiometricAuthenticator`, and `MobileAuthenticator` classes encapsulate the specific logic, success rates (e.g., 98% for RFID, 99% for Biometric), and response times for each method.
3. Core System Engine: The `SmartLocker` class handles the physical state of the locker (Locked, Open, Tampered) and processes access requests by invoking the appropriate authenticator.
4. Security Monitor: An independent module that analyzes the stream of access logs to detect patterns indicative of an attack.
5. Analytics Engine: The `LockerAnalytics` class ingests the generated audit logs and produces graphical security reports.""")

    doc.add_page_break()

    # --- CHAPTER 6 ---
    add_chapter("6", "SOLUTION DEVELOPMENT")
    
    doc.add_heading('6.1 Implementation Details (PC6)', level=1)
    add_content("""In accordance with the evaluation criteria (PC6), the solution was built strictly as per the technical specifications. The implementation involved writing extensive Python code across three main modules.

Core Access Control Logic:
The `SmartLocker` class was implemented to process access requests. The `process_access_request()` method acts as the gatekeeper. It first checks for network connectivity and maintenance mode. It then invokes `authenticate_user()`. If authentication fails, it increments a `failed_access_count`. If this count reaches 3, it generates a CRITICAL 'UNAUTHORIZED_ACCESS' alert. If successful, it grants access, resets the counter, and updates the locker status.

Audit Logging:
Every single access attempt, whether successful or failed, generates an `AccessLog` object containing the timestamp, user ID, authentication method used, success status, and simulated access duration. This creates an immutable audit trail required for high-security environments.""")

    doc.add_heading('6.2 IoT Authentication Module', level=1)
    add_content("""The IoT authentication aspect was implemented in the `smart_locker_authentication.py` module. 

Realistic Simulation:
Rather than simple True/False returns, the authenticators simulate real-world IoT device behavior:
• BiometricAuthenticator: Uses `hashlib.sha256()` to simulate storing and matching fingerprint templates. It models a 99% success rate but introduces random confidence scores.
• MobileAuthenticator: Models network dependency, incorporating a 'server_uptime' variable. If the simulated server is down, authentication fails with a NETWORK_ERROR status.
• RFIDAuthenticator: Models battery drain per scan and generates confidence scores based on simulated read distances.

All authenticators simulate response times (e.g., 500-1500ms for biometrics, 100-500ms for RFID) to accurately model system latency.""")

    doc.add_heading('6.3 Security Monitoring and Analytics', level=1)
    add_content("""The `SecurityMonitor` class was built to provide active threat detection. The `check_brute_force()` method analyzes the timestamp array of failed attempts. If it detects more than 5 failed attempts within a 300-second window for a specific locker, it triggers a CRITICAL 'BRUTE_FORCE' alert.

The `smart_locker_analytics.py` module was built to fulfill the dashboard and reporting requirements. Five distinct visualization functions were developed:
1. `generate_access_pattern_analysis()`: Plots authentication method distribution and hourly access patterns.
2. `generate_security_alert_analysis()`: Displays the distribution of security alerts by type (Tamper, Network Failure) and severity.
3. `generate_access_success_rate()`: Shows the success rate percentages across different authentication methods.
4. `generate_locker_occupancy()`: A histogram showing the physical utilization of the lockers.
5. `generate_system_dashboard()`: A comprehensive KPI dashboard for security administrators.""")

    doc.add_page_break()

    # --- CHAPTER 7 ---
    add_chapter("7", "SOLUTION TESTING AND PERFORMANCE")
    
    doc.add_heading('7.1 Testing Strategy (PC7)', level=1)
    add_content("""In accordance with the evaluation criteria (PC7), the solution was thoroughly tested to ensure security and reliability.

Unit Testing:
Individual authenticators were tested to ensure their success rates aligned with their configured probabilities over 10,000 iterations. The `check_brute_force` algorithm was tested by feeding it arrays of timestamps spaced 10 seconds apart (triggering the alert) and 70 seconds apart (bypassing the alert).

Integration Testing:
The `LockerManagementSystem` was run with 20 lockers and 10 users, simulating 100 random access requests. This tested the interaction between the User database, the SmartLocker authorization checks, and the generation of AccessLogs.

Security Testing:
Specific edge cases were tested, including:
• Attempting access with an inactive user account (Denied).
• Attempting access to a locker not assigned to the user (Denied).
• Simulating physical tampering during an active session (Alert Generated).""")

    doc.add_heading('7.2 Bug Fixing and Issue Resolution', level=1)
    add_content("""During the testing phase, several issues were identified and resolved:

Issue 1: Alert Flooding on Network Failure
Bug: When network connectivity was simulated as lost, every subsequent access attempt generated a new 'NETWORK_FAILURE' alert, flooding the security logs.
Fix: Implemented state tracking so the alert is only generated on the initial failure detection, and subsequent denied accesses are logged silently until connectivity is restored.

Issue 2: Persistent Failed Access Count
Bug: The `failed_access_count` on a locker was not resetting after a successful login, causing legitimate users to trigger unauthorized access alerts if previous users had failed.
Fix: Added logic to reset `self.failed_access_count = 0` immediately upon a successful authentication event.""")

    doc.add_heading('7.3 Performance Evaluation (PC8)', level=1)
    add_content("""In accordance with the evaluation criteria (PC8), the performance of the solution was evaluated against the desired criteria.

System Security:
The Python simulation successfully demonstrated robust access control. 100% of unauthorized access attempts (wrong user, wrong locker) were blocked. The system successfully identified and alerted on simulated brute force attacks and physical tampering events within milliseconds of the trigger conditions being met.

Impact Assessment:
Based on the simulated data, replacing traditional locks with the Smart Locker System provides complete visibility into asset access. The generated audit logs provide undeniable proof of who accessed which locker and when. Furthermore, the multi-modal authentication success rates (averaging >97%) demonstrate that security is enhanced without significantly impacting user convenience, directly addressing the problem statement's core objectives.""")

    doc.add_page_break()

    # --- CHAPTER 8 ---
    add_chapter("8", "RESULTS AND VISUALIZATIONS")
    
    add_content("""This chapter presents the graphical results generated by the Smart Locker System analytics module. These visualizations serve as the interactive security dashboards required by the problem statement.""")
    
    doc.add_heading('8.1 Access Pattern and Success Rates', level=1)
    add_content("""The Access Pattern Analysis chart displays the distribution of authentication methods used across the user base and tracks the volume of access attempts throughout a 24-hour period, clearly highlighting peak usage hours.""")
    
    if os.path.exists('/home/ubuntu/access_pattern.png'):
        doc.add_picture('/home/ubuntu/access_pattern.png', width=Inches(6.0))
        p = doc.add_paragraph('Figure 1: Authentication Distribution and 24-Hour Access Pattern')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].italic = True

    add_content("""The Access Success Rate chart provides critical metrics on the reliability of different IoT authenticators. As shown, Biometric and Multi-Factor methods maintain the highest success rates, while PIN codes show a slightly higher failure rate due to simulated user error.""")
    
    if os.path.exists('/home/ubuntu/access_success_rate.png'):
        doc.add_picture('/home/ubuntu/access_success_rate.png', width=Inches(6.0))
        p = doc.add_paragraph('Figure 2: Authentication Success Rates by Method')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].italic = True

    doc.add_page_break()
    doc.add_heading('8.2 Security Alerts and Occupancy', level=1)
    add_content("""The Security Alert Analysis chart categorizes system warnings, helping security teams prioritize responses. It separates routine maintenance warnings (like low battery) from critical security events (like forced entry or tampering).""")
    
    if os.path.exists('/home/ubuntu/security_alerts.png'):
        doc.add_picture('/home/ubuntu/security_alerts.png', width=Inches(6.0))
        p = doc.add_paragraph('Figure 3: Security Alert Distribution by Type and Severity')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].italic = True

    doc.add_heading('8.3 System Security Dashboard', level=1)
    add_content("""The System Security Dashboard serves as the central hub for facility administrators, providing a high-level overview of total lockers monitored, current lock states, active security alerts, and overall system health.""")

    if os.path.exists('/home/ubuntu/locker_dashboard.png'):
        doc.add_picture('/home/ubuntu/locker_dashboard.png', width=Inches(6.0))
        p = doc.add_paragraph('Figure 4: Smart Locker Access Control System Dashboard')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].italic = True

    doc.add_page_break()

    # --- CHAPTER 9 ---
    add_chapter("9", "LEARNING EVALUATION")
    
    doc.add_heading('9.1 Technical Skill Gain (PC9)', level=1)
    add_content("""In accordance with the evaluation criteria (PC9), this internship resulted in significant technical skill gain and professional development.

1. Cybersecurity Principles: Gained deep understanding of access control models, multi-factor authentication, and threat detection algorithms (e.g., identifying brute force patterns).
2. Python Programming: Enhanced proficiency in advanced Python concepts, including Object-Oriented Programming (OOP), cryptographic hashing (hashlib), and simulation of asynchronous IoT devices.
3. Data Analytics & Visualization: Mastered the use of Matplotlib and Seaborn to transform raw security audit logs into professional, actionable dashboards for security administrators.
4. Problem Solving: Developed critical thinking skills through the process of designing secure authentication workflows and resolving edge cases like network disconnections and alert flooding.""")

    doc.add_heading('9.2 Conclusion', level=1)
    add_content("""The Smart Locker Access Control System successfully addresses the vulnerabilities and monitoring limitations associated with traditional physical locks. By leveraging IoT simulation, multi-modal authentication (RFID, Biometric, Mobile), and real-time threat detection, the developed solution provides continuous security monitoring, instant alert generation, and immutable audit trails.

The project demonstrates that intelligent access control can significantly enhance asset protection, streamline administrative overhead, and provide security teams with actionable intelligence. The successful completion of this project fulfills all evaluation criteria and serves as a robust foundation for deploying physical IoT electronic locks and biometric scanners in high-security environments.""")

    # Save the document
    doc.save('/home/ubuntu/Internship_Report_Smart_Locker.docx')
    print("Report generated successfully at /home/ubuntu/Internship_Report_Smart_Locker.docx")

if __name__ == "__main__":
    create_report()
