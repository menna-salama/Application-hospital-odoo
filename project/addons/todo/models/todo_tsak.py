from email.policy import default
from odoo import models, fields, api # type: ignore
from odoo.exceptions import ValidationError # type: ignore
from datetime import datetime # type: ignore


class TimeSheet(models.Model):
    _name = 'todo.timesheet'

    date = fields.Date(string="Date")
    description = fields.Text(string="Description")
    time = fields.Float(string="Time Spent (hours)")
    task_id = fields.Many2one('todo.task', string="Task")


class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'Todo Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Task Name', required=True, translate=True)
    description = fields.Text(string='Description')
    assigned_to = fields.Many2one('res.users', string='Assigned To')
    due_date = fields.Date(string='Due Date', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('close', 'Close'),
    ], string='State', default='draft')
    estimated_time = fields.Float(string='Estimated Time (hours)')
    ref = fields.Char(default='New', readonly=True)
    is_late = fields.Boolean()
    active = fields.Boolean(default=True)
    timesheet_ids = fields.One2many('todo.timesheet', 'task_id', string='Time Sheets')

    @api.constrains('timesheet_ids', 'estimated_time')
    def _check_timesheet(self):
        for record in self:
            total_time = sum(sheet.time for sheet in record.timesheet_ids)
            if total_time > record.estimated_time:
                raise ValidationError("Total time spent on timesheets cannot exceed estimated time.")

    def action_closed(self):
        for rec in self:
            rec.state = 'close'

    def check_is_late(self):
        tasks = self.search([('state', '!=', 'done'), ('state', '!=', 'close')])
        for task in tasks:
            if task.due_date and task.due_date < fields.Date.today():
                task.is_late = True
            else:
                task.is_late = False

    @api.model
    def create(self, vals):
        res = super(TodoTask, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env["ir.sequence"].next_by_code("task_seq")
        return res
