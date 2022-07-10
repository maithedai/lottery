from odoo import fields, api, models


class Customer(models.Model):
    _name = 'customer'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', required=True, ondelete='restrict', auto_join=True, index=True,
                                 string='Related Partner', help='Partner-related data of the user')
    name = fields.Char(related='partner_id.name', inherited=True, readonly=False, required=1, string='Họ tên')
    email = fields.Char(related='partner_id.email', inherited=True, readonly=False)
    gender = fields.Selection([('nam', 'Nam'), ('nu', 'Nữ')],
                              string='Giới tính',
                              default='nam')
    phone = fields.Char(string='Số điện thoại', required=1)
    address = fields.Char(string='Địa chỉ', required=1)
    status = fields.Selection([('active', 'Hoạt động'), ('locked', 'Khóa')],
                              string='Trạng thái',
                              default='active')
    note = fields.Char(string='Ghi chú')
    price = fields.Float(string='Đơn giá', required=1)
    planed = fields.Many2one('customer.plan', string='Kế hoạch lãnh', required=1)

    HCM = fields.Integer(string='TP HCM')
    DT = fields.Integer(string='ĐT')
    CM = fields.Integer(string='CM')
    BL = fields.Integer(string='CM')
    BT = fields.Integer(string='BT')
    VT = fields.Integer(string='VT')
    ST = fields.Integer(string='ST')
    CT = fields.Integer(string='ST')
    DN = fields.Integer(string='ĐN')
    TN = fields.Integer(string='TN')
    AG = fields.Integer(string='AG')
    BTH = fields.Integer(string='BTH')
    BD = fields.Integer(string='BD')
    TV = fields.Integer(string='TV')
    VL = fields.Integer(string='VL')
    HCM_2 = fields.Integer(string='TP HCM')
    LA = fields.Integer(string='LA')
    BP = fields.Integer(string='BP')
    HG = fields.Integer(string='HG')
    KG = fields.Integer(string='KG')
    DL = fields.Integer(string='ĐL')
    TG = fields.Integer(string='TG')

    def create_customer(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }


class CustomerPlan(models.Model):
    _name = 'customer.plan'

    name = fields.Char('Tên kế hoạch')
    state = fields.Selection([('active', 'Hoạt động'), ('inactive', 'Ngừng hoạt động')])