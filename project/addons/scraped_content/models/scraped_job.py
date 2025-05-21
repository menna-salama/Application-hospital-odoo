from odoo import models, fields, api # type: ignore


class ScrapedJob(models.Model):
    _name = 'scraped.job'
    _description = 'Scraped Job'
    _rec_name = 'name'

    name = fields.Char(string='Job Name', required=True)
    company_name = fields.Char(string='Company Name', required=True)
    company_logo_url = fields.Char(string='Company Logo URL')
    location = fields.Char(string='Location')
    source_url = fields.Char(string='Source URL')
    date_posted = fields.Char(string='Date Posted', required=True)
    status = fields.Selection(
        [("new", "New"), ("in_review", "In Review"), ("approved", "Approved"), ("archived", "Archived")],

        string="Status",
    )
    website_published = fields.Boolean(string='Published on Website', default=True)
    website_url = fields.Char(compute='_compute_website_url', string='Website URL')

    def _compute_website_url(self):
        for record in self:
            record.website_url = f"/job/{record.id}"
