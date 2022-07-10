from odoo import fields, api, models, _
from datetime import datetime


class CreatePlan(models.TransientModel):
    _name = 'create.plan'

    date = fields.Date('Kế hoạch ngày', default=datetime.now())

    def create_plan(self):
        return {
            'name': _('Kế hoạch lãnh vé'),
            'view_mode': 'form',
            'res_model': 'planed',
            'type': 'ir.actions.act_window',
            'context': {
                'default_name': f'Kế hoạch lãnh vé ngày {self.date.strftime("%d-%m-%Y")}',
                'default_date': self.date,
                'default_day_of_week': str(self.date.weekday()),
            },
            'view_id': self.env.ref('lottery.form_planed').id,
            'target': 'current',
        }