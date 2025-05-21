from odoo import models, fields, api  # type: ignore
from odoo.exceptions import ValidationError # type: ignore


class AssignTaskWizard(models.TransientModel):
    _name = "todo.assign.task.wizard"
    _description = "Assign Task Wizard"

    user_ids = fields.Many2one("res.users", string="Users")
    task_ids = fields.Many2many(
        "todo.task",
        string="Tasks",
        required=True,
        domain="[('state', 'not in', ['done', 'close'])]",
    )

    @api.constrains("task_ids")
    def _check_task_states(self):
        for record in self:
            invalid_tasks = record.task_ids.filtered(
                lambda t: t.state in ["done", "close"]
            )
            if invalid_tasks:
                raise ValidationError(
                    f"Cannot assign completed or closed tasks: "
                    f"{', '.join(invalid_tasks.mapped('name'))}"
                )

    # Assign the selected tasks to the selected users
    def action_assign_tasks(self):
        if not self.user_ids or not self.task_ids:
            raise ValidationError("Please select a user and at least one task to assign.")
        self._check_task_states()
        for task in self.task_ids:
            task.write({"assigned_to": self.user_ids.id})
        return {"type": "ir.actions.act_window_close"}
