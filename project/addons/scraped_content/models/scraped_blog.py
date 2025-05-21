from odoo import models, fields, api # type: ignore


class ScrapedBlog(models.Model):
    _name = "scraped.blog"
    _description = "Scraped Blog"
    _rec_name = "title"

    title = fields.Char(string="Title", required=True)
    summary = fields.Char(string="Summary")
    content = fields.Char(string="Content")
    source_url = fields.Char(string="Source URL")
    published_date = fields.Char(string="Date Published")
    status = fields.Selection(
        selection=[
            ("read", "Read"),
            ("note_read", "Note Read"),
        ],
        string="Status",
        default="read",
    )
    website_published = fields.Boolean(string="Published on Website", default=True)
    website_url = fields.Char(compute="_compute_website_url", string="Website URL")

    def _compute_website_url(self):
        for record in self:
            record.website_url = f"/blog/{record.id}"
