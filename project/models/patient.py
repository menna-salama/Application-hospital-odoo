from odoo import models, fields, api
from odoo.exceptions import ValidationError
import  re
class HmsPatient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient Record'

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    email = fields.Char(string="Email")
    birth_date = fields.Date(string="Birth Date")
    history = fields.Html(string="History")
    cr_ratio = fields.Float(string="CR Ratio")
    blood_type = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('ab', 'AB'),
        ('o', 'O')
    ], string="Blood Type")
    pcr = fields.Boolean(string="PCR Done")
    image = fields.Binary(string="Image")
    address = fields.Text(string="Address")
    age = fields.Integer(string="Age")
    department_id = fields.Many2one('hms.department', string="Department")
    doctor_ids = fields.Many2many('hms.doctor', string="Doctors")
    log_ids = fields.One2many('hms.patient.log', 'patient_id', string="Log History")

    @api.constrains('department_id')
    def _check_department_opened(self):
        for rec in self:
            if rec.department_id and not rec.department_id.is_opened:
                raise ValidationError("You cannot choose a closed department.")

    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio_required(self):
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                raise ValidationError("CR Ratio is required when PCR is checked.")

    @api.onchange('birth_date')
    def _onchange_birth_date(self):
        if self.birth_date:
            today = fields.Date.today()
            self.age = today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )

    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 50:
            self.history = False


    @api.depends('birth_date')
    def _compute_age(self):
        today = fields.Date.today()
        for rec in self:
            if rec.birth_date:
                rec.age = today.year - rec.birth_date.year - (
                    (today.month, today.day) < (rec.birth_date.month, rec.birth_date.day)
                )
            else:
                rec.age = 0



    @api.constrains('email')
    def _check_email_valid_unique(self):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        for rec in self:
            if rec.email and not re.match(pattern, rec.email):
                raise ValidationError("Invalid email format.")
            existing = self.search([('email', '=', rec.email), ('id', '!=', rec.id)], limit=1)
            if existing:
                raise ValidationError("Email must be unique.")
