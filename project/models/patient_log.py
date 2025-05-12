from odoo import models, fields
from datetime import datetime

class PatientLog(models.Model):
    _name = 'hms.patient.log'
    _description = 'Patient Log'

    patient_id = fields.Many2one('hms.patient')
    created_by = fields.Many2one('res.users', default=lambda self: self.env.user)
    date = fields.Datetime(default=lambda self: fields.Datetime.now())
    description = fields.Text()
