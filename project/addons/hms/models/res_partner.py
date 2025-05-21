from odoo import models, fields, api  # type: ignore
from odoo.exceptions import ValidationError # type: ignore


class ResPartner(models.Model):
    _inherit = "res.partner"

    related_patient_id = fields.Many2one(
        "hms.patient",
        string="Related Patient",
    )

    @api.constrains("vat", "is_company")
    def _check_vat_for_crm_customers(self):
        for record in self:
            if record.is_company and not record.vat:
                raise ValidationError(" VAT is required for companies")

    @api.constrains("related_patient_id", "email")
    def _check_patient_email(self):
        for record in self:
            if record.related_patient_id and record.email:
                other_partners = self.search(
                    [
                        ("id", "!=", record.id),
                        ("email", "=", record.email),
                        ("related_patient_id", "!=", False),
                    ]
                )
                if other_partners:
                    raise ValidationError(
                        "This email is already used by another customer with a linked patient!"
                    )

 
    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise ValidationError(
                    "You cannot delete a customer that is linked to a patient!"
                )
        return super(ResPartner, self).unlink()
