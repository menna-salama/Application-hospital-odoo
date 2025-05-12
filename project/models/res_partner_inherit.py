from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string="Related Patient")

    @api.constrains('email')
    def _check_patient_email_conflict(self):
        for rec in self:
            if rec.email:
                patient = self.env['hms.patient'].search([('email', '=', rec.email)], limit=1)
                if patient:
                    raise ValidationError("This email is already used for a patient.")

    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise ValidationError("You cannot delete a customer linked to a patient.")
        return super().unlink()
