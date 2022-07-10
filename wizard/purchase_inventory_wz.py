from odoo import fields, api, models, _
from datetime import datetime


class PurchaseInventoryWZ(models.TransientModel):
    _name = 'purchase.inventory.wz'

    date = fields.Date('Ngày nhập', default=datetime.now())

    def create_purchase(self):
        return {
            'name': _('Nhập kho'),
            'view_mode': 'form',
            'res_model': 'purchase.inventory',
            'type': 'ir.actions.act_window',
            'context': {
                'default_name': f'Nhập kho ngày: {self.date.strftime("%d-%m-%Y")}',
                'default_date': self.date,
                'default_day_of_week': str(self.date.weekday()),
            },
            'view_id': self.env.ref('lottery.purchase_inventory_form_view').id,
            'target': 'current',
        }