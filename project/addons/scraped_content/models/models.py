# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class scraped_content(models.Model):
#     _name = 'scraped_content.scraped_content'
#     _description = 'scraped_content.scraped_content'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

