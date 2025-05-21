{
    "name": "To Do App",
    "summary": """

    """,
    "description": """

    """,
    "author": "My Company",
    "website": "http://www.yourcompany.com",
    "category": "",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "mail",
    ],
    # always loaded
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "views/views.xml",
        "views/todo_task_view.xml",
        "reports/todo_task_report.xml",
        "data/sequence.xml",
        "wizards/assign_task_to_wizard_view.xml",
    ],
    "application": True,
    "installable": True,
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
    "license": "LGPL-3",
}  # type: ignore
