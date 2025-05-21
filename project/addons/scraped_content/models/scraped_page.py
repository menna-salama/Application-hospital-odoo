from odoo import models, fields, api # type: ignore


class ScrapedPage(models.Model):
    _name = "scraped.page"
    _description = "Scraped Page"
    _rec_name = "title"

    title = fields.Char(string="Title", required=True)
    content = fields.Char(string="Content")
    source_url = fields.Char(string="Source URL", required=True)
    status = fields.Selection(
        selection=[
            ("vist", "Vist"),
            ("not_visit", "Not Visit"),
        ],
        string="Status",

    )
    website_published = fields.Boolean(string="Published on Website", default=True)
    website_url = fields.Char(compute="_compute_website_url", string="Website URL")

    def _compute_website_url(self):
        for record in self:
            record.website_url = f"/page/{record.id}"
