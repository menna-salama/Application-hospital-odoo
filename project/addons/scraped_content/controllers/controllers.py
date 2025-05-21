from odoo import http # type: ignore
from odoo.http import request # type: ignore


class ScrapedBlogWebsite(http.Controller):

    @http.route("/blog", type="http", auth="public", website=True)
    def blog_list(self, **kw):
        blogs = (
            request.env["scraped.blog"]
            .sudo()
            .search([("website_published", "=", True)])
        )
        return request.render("scraped_content.blog_list_template", {"blogs": blogs})

    @http.route("/blog/<int:blog_id>", type="http", auth="public", website=True)
    def blog_detail(self, blog_id, **kw):
        blog = request.env["scraped.blog"].sudo().browse(blog_id)
        return request.render("scraped_content.blog_detail_template", {"blog": blog})


class ScrapedJobWebsite(http.Controller):

    @http.route("/jobs", type="http", auth="public", website=True)
    def job_list(self, **kw):
        jobs = (
            request.env["scraped.job"].sudo().search([("website_published", "=", True)])
        )
        return request.render("scraped_content.job_list_template", {"jobs": jobs})

    @http.route("/job/<int:job_id>", type="http", auth="public", website=True)
    def job_detail(self, job_id, **kw):
        job = request.env["scraped.job"].sudo().browse(job_id)
        return request.render("scraped_content.job_detail_template", {"job": job})


class ScrapedPageWebsite(http.Controller):

    @http.route("/pages", type="http", auth="public", website=True)
    def page_list(self, **kw):
        pages = (
            request.env["scraped.page"]
            .sudo()
            .search([("website_published", "=", True)])
        )
        return request.render("scraped_content.page_list_template", {"pages": pages})

    @http.route("/page/<int:page_id>", type="http", auth="public", website=True)
    def page_detail(self, page_id, **kw):
        page = request.env["scraped.page"].sudo().browse(page_id)
        return request.render("scraped_content.page_detail_template", {"page": page})
