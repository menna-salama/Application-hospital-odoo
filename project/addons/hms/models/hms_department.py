from odoo import models, fields, api  # type: ignore


class Department(models.Model):
    _name = "hms.department"
    _description = "Department Record"

    name = fields.Char(string="Name", required=True)
    capacity = fields.Integer(string="Capacity")
    state = fields.Selection(
        [("open", "Open"), ("closed", "Closed")],
        string="Status",
        default="open",
        required=True,
    )
    patient_ids = fields.One2many("hms.patient", "department_id", string="Patients")

    def open_transfer_wizard(self):
        self.ensure_one()
        patients = self.env['hms.patient'].search([('department_id', '=', self.id)])
        return {
            "type": "ir.actions.act_window",
            "res_model": "hms.patient.transfer.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_patient_ids": [(6, 0, patients.ids)]},
        }
