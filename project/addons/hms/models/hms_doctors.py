from odoo import models, fields, api  # type: ignore


class Doctor(models.Model):
    _name = "hms.doctors"
    _description = "Doctor Record"
    _rec_name = "name"

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    image = fields.Binary(string="Doctor Image")
    patient_ids = fields.Many2many("hms.patient", string="Patients")
    name = fields.Char(string="Name", compute="_compute_name", store=True)

    @api.depends("first_name", "last_name")
    def _compute_name(self):
        for rec in self:
            rec.name = (
                f"Dr. {rec.first_name} {rec.last_name}"
                if rec.first_name and rec.last_name
                else "New Doctor"
            )
