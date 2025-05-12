{
    'name': 'Hospital Management System',
    'version': '1.0',
    'depends': ['base','web'],
    'data': [
        'views/patient_views.xml',
        'views/department_views.xml',
        'views/doctor_views.xml',
        'views/patient_log_views.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',

}
