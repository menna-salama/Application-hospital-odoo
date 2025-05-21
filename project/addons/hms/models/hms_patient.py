from enum import unique
from odoo import models, fields, api # type: ignore
from odoo.exceptions import ValidationError # type: ignore
from datetime import date
import re


class PatientLog(models.Model):
    _name = "hms.patient.log"
    _description = "Patient Log History"

    patient_id = fields.Many2one(
        "hms.patient", string="Patient", required=True, ondelete="cascade"
    )
    date = fields.Datetime(
        string="Date", default=lambda self: fields.Datetime.now(), readonly=True
    )
    description = fields.Text(string="Description", required=True)


class Patient(models.Model):
    _name = "hms.patient"
    _description = "Patient Record"
    _rec_name = "name"

    name = fields.Char(compute="_compute_name", store=True)
    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    birth_date = fields.Date(string="Birth Date")
    history = fields.Html(string="History")
    cr_ratio = fields.Float(string="CR Ratio")
    blood_type = fields.Selection(
        [("a", "A"), ("b", "B"), ("o", "O"), ("ab", "AB")], string="Blood Type"
    )
    pcr = fields.Boolean(string="PCR")
    image = fields.Binary(string="Patient Image")
    address = fields.Text(string="Address")
    age = fields.Integer(string="Age", compute="_compute_age", store=True)
    states = fields.Selection(
        [
            ("undetermined", "Undetermined"),
            ("good", "Good"),
            ("fair", "Fair"),
            ("serious", "Serious"),
        ],
        string="State",
    )
    show_history = fields.Boolean()
    email = fields.Char(string="Email", required=True, unique=True)
    department_id = fields.Many2one(
        "hms.department",
        string="Department",
        required=True,
        domain="[('state', '=', 'open')]",
    )
    department_capacity = fields.Integer(
        related="department_id.capacity", string="Department Capacity", readonly=True
    )
    doctor_ids = fields.Many2many(
        "hms.doctors",
        string="Doctors",

    )
    log_history_ids = fields.One2many(
        "hms.patient.log", "patient_id", string="Log History"
    )
    customer_ids = fields.One2many(
        "res.partner", "related_patient_id", string="Related Customers"
    )
    doctor_selection = fields.Selection(
        [("selected", "Selected"), ("not_selected", "Not Selected")],
        default="not_selected",
    )
    _sql_constrains = [("unique_email", "unique(email)", "Email must be unique")]

    @api.depends("first_name", "last_name")
    def _compute_name(self):
        for rec in self:
            rec.name = (
                f"{rec.first_name} {rec.last_name}"
                if rec.first_name and rec.last_name
                else "New Patient"
            )

    @api.depends("birth_date")
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = date.today()
                record.age = today.year - record.birth_date.year
            else:
                record.age = 0

    @api.constrains("email")
    def _check_valid_email(self):
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        for record in self:
            if record.email and not re.match(email_pattern, record.email):
                raise ValidationError(
                    "Invalid Email Address. Please enter a valid email address"
                )

    @api.constrains("pcr", "cr_ratio")
    def _check_cr_ratio(self):
        for record in self:
            if record.pcr and not record.cr_ratio:
                raise ValidationError("CR Ratio is required when PCR is checked")

    @api.onchange("states")
    def _onchange_state(self):
        if self.states:
            return {
                "warning": {
                    "title": "State Changed",
                    "message": f"State will be changed to {self.states}",
                }
            }

    def write(self, vals):
        res = super(Patient, self).write(vals)
        if "states" in vals:
            self.env["hms.patient.log"].create(
                {
                    "patient_id": self.id,
                    "description": f"State changed to {self.states}",
                }
            )
        return res

    @api.onchange('department_id')
    def _onchange_department_id_readonly_doctors(self):
        for rec in self:
            if rec.department_id:
                rec.doctor_selection = 'selected'
            else:
                rec.doctor_selection = 'not_selected'

    @api.onchange("age")
    def _onchange_show_history(self):
        for record in self:
            if record.age >= 50:
                record.show_history = False
            else:
                record.show_history = True

            if record.age in range(1, 31):
                record.pcr = True
                message = f"PCR has been automatically checked because patient's age ({record.age} years) is less than 30"
                return {"warning": {"title": "Warning", "message": message}}



    def action_open_related_doctor(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("hms.doctors_action")

        if len(self.doctor_ids) == 1:
            # if there is one doctor
            action.update({
                'res_id': self.doctor_ids.id,
                'view_mode': 'form',
                'views': [(self.env.ref("hms.view_hms_doctors_form").id, 'form')],
            })
        else:
            # if there are more doctors
            action.update({
                'domain': [('id', 'in', self.doctor_ids.ids)],
                'view_mode': 'tree,form',
            })

        return action


    def patient_xlsx_report(self):
        if not self:
            raise ValidationError('Please select records to export!')

        return {
            'type': 'ir.actions.act_url',
            'url': f"/api/hms/patient/report?ids={','.join(map(str, self.ids))}",
            'target': 'new',
        }

