from odoo import fields, api, models, _
from datetime import datetime


class CreateReturnStock(models.TransientModel):
    _name = 'create.return.stock'

    date = fields.Date('Trả ế ngày', default=datetime.now())

    def create_return_stock(self):
        return {
            'name': _('Trả ế'),
            'view_mode': 'form',
            'res_model': 'return.stock',
            'type': 'ir.actions.act_window',
            'context': {
                'default_name': f'Trả ế ngày {self.date.strftime("%d-%m-%Y")}',
                'default_date': self.date,
                'default_day_of_week': str(self.date.weekday()),
            },
            'view_id': self.env.ref('lottery.form_return_stock').id,
            'target': 'current',
        }