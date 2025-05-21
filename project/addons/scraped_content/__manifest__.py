# -*- coding: utf-8 -*-
{
    "name": "Scraped Content",
    "summary": "Scraped Content and Integration with Odoo",
    "description": """
    This module allows you to scrape content from various sources and integrate it with Odoo.
    It provides a user-friendly interface for managing scraped content and offers features
    for data extraction, transformation, and loading (ETL) processes.
    """,
    "author": "My Company",
    "website": "https://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "website"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/views.xml",
        "views/templates.xml",
        "views/scraped_job_view.xml",
        "views/scraped_blog_view.xml",
        "views/scraped_page_view.xml",
        "views/blog_templates.xml",
        "views/job_templates.xml",
        "views/page_templates.xml",
    ],
    "application": True,
    "installable": True,
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
}  # type: ignore
