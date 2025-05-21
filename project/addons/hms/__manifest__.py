{
    "name": "Hospital Management System",
    "summary": """
        Complete Hospital Management System for managing patients,
        doctors, appointments and medical records.
    """,
    "description": """
        Hospital Management System (HMS) Features:
        ========================================
        * Patient Registration and Management
        * Patient Medical History
        * Blood Type Tracking
        * PCR Test Results
        * Medical Reports and Documents
        * Patient Image Management
        * Address and Contact Information

        This module helps hospitals and clinics to:
        -----------------------------------------
        1. Efficiently manage patient records
        2. Track medical history
        3. Monitor patient test results
        4. Store and organize patient documents
        5. Maintain comprehensive patient profiles
    """,
    "author": "My Company",
    "website": "http://www.yourcompany.com",
    "category": "Healthcare",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "crm",
    ],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "security/res_groups.xml",
        "views/views.xml",
        "views/templates.xml",
        "views/hms_patient_view.xml",
        "views/hms_doctors_view.xml",
        "views/hms_department_view.xml",
        "views/res_partner_view.xml",
        "reports/hms_patient_report.xml",
        "wizards/patient_transfer_wizard_view.xml",
    ],
    'assets': {
        'web.report_assets_common': ['hms/static/src/css/fonts.css'],
    },
    "application": True,
    "installable": True,
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
    "license": "LGPL-3",
}  # type: ignore
