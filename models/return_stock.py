from odoo import fields, api, models
from datetime import datetime


class ReturnStock(models.Model):
    _name = 'return.stock'

    name = fields.Char('Tên trả ế')
    date = fields.Date(string='Ngày', default=datetime.now())
    lines = fields.One2many('return.stock.line', 'return_stock_id')
    tele_ids = fields.One2many('return.stock.tele', 'return_stock_id')

    @api.model
    def default_get(self, fields_list):
        res = super(ReturnStock, self).default_get(fields_list)
        stock_ids = self.env['data.tele'].search([])
        data = []
        for p in stock_ids:
            data.append((0, 0, {'data_tele_id': p.id}))
        res.update({'tele_ids': data})
        customer_ids = self.env['customer'].search([('status', '=', 'active')])
        val_lines = []
        for customer in customer_ids:
            vals = {
                'customer_id': customer.id,
                'HCM': customer.HCM,
                'DT': customer.DT,
                'CM': customer.CM,
                'BL': customer.BL,
                'BT': customer.BT,
                'VT': customer.VT,
                'ST': customer.ST,
                'CT': customer.CT,
                'DN': customer.DN,
                'AG': customer.AG,
                'BD': customer.BD,
                'TV': customer.TV,
                'VL': customer.VL,
                'HCM_2': customer.HCM_2,
                'LA': customer.LA,
                'BP': customer.BP,
                'HG': customer.HG,
                'KG': customer.KG,
                'DL': customer.DL,
                'TG': customer.TG,
            }
            val_lines.append((0, 0, vals))
        res.update({'lines': val_lines})
        return res

    day_of_week = fields.Selection([
        ('0', 'Thứ 2'),
        ('1', 'Thứ 3'),
        ('2', 'Thứ 4'),
        ('3', 'Thứ 5'),
        ('4', 'Thứ 6'),
        ('5', 'Thứ 7'),
        ('6', 'Chủ nhật')
    ])


class ReturnStockLine(models.Model):
    _name = "return.stock.line"

    return_stock_id = fields.Many2one('return.stock')
    customer_id = fields.Many2one('customer', string='Khách hàng', readonly=1)

    HCM = fields.Integer(string='TP HCM')
    HCM_PC = fields.Integer(string='TP HCM', readonly=1)

    DT = fields.Integer(string='ĐT', sum="Tổng số")
    DT_PC = fields.Integer(string='ĐT', readonly=1)

    CM = fields.Integer(string='CM')
    CM_PC = fields.Integer(string='CM', readonly=1)

    BL = fields.Integer(string='CM')
    BL_PC = fields.Integer(string='BL', readonly=1)

    BT = fields.Integer(string='BT')
    BT_PC = fields.Integer(string='BT', readonly=1)

    VT = fields.Integer(string='VT')
    VT_PC = fields.Integer(string='VT', readonly=1)

    ST = fields.Integer(string='ST')
    ST_PC = fields.Integer(string='ST', readonly=1)

    CT = fields.Integer(string='ST')
    CT_PC = fields.Integer(string='CT', readonly=1)

    DN = fields.Integer(string='ĐN')
    DN_PC = fields.Integer(string='ĐN', readonly=1)

    TN = fields.Integer(string='TN')
    TN_PC = fields.Integer(string='TN', readonly=1)

    AG = fields.Integer(string='AG')
    AG_PC = fields.Integer(string='AG', readonly=1)

    BTH = fields.Integer(string='BTH')
    BTH_PC = fields.Integer(string='BTH', readonly=1)

    BD = fields.Integer(string='BD')
    BD_PC = fields.Integer(string='BD', readonly=1)

    TV = fields.Integer(string='TV')
    TV_PC = fields.Integer(string='TV', readonly=1)

    VL = fields.Integer(string='VL')
    VL_PC = fields.Integer(string='VL', readonly=1)

    HCM_2 = fields.Integer(string='TP HCM')
    HCM_2_PC = fields.Integer(string='TP HCM', readonly=1)

    LA = fields.Integer(string='LA')
    LA_PC = fields.Integer(string='LA', readonly=1)

    BP = fields.Integer(string='BP')
    BP_PC = fields.Integer(string='BP', readonly=1)

    HG = fields.Integer(string='HG')
    HG_PC = fields.Integer(string='HG', readonly=1)

    KG = fields.Integer(string='KG')
    KG_PC = fields.Integer(string='KG', readonly=1)

    DL = fields.Integer(string='ĐL')
    DL_PC = fields.Integer(string='ĐL', readonly=1)

    TG = fields.Integer(string='TG')
    TG_PC = fields.Integer(string='TG', readonly=1)

    percent = fields.Float("%")
    sum_return = fields.Integer("Tổng trả", compute="_compute_sum_return")
    consume = fields.Integer("Tiêu thụ", compute="_compute_consume")
    ticket_receive = fields.Integer("Lượng vé lãnh", compute='_compute_ticket_receive')
    du_thieu = fields.Integer('Dư thiếu')
    revenues = fields.Float('Tiền thu', compute="_compute_revenues")
    day_of_week = fields.Selection([
        ('0', 'Thứ 2'),
        ('1', 'Thứ 3'),
        ('2', 'Thứ 4'),
        ('3', 'Thứ 5'),
        ('4', 'Thứ 6'),
        ('5', 'Thứ 7'),
        ('6', 'Chủ nhật')
    ])

    date = fields.Date(string='Ngày', default=datetime.now())

    @api.depends('HCM', 'DT', 'CM', 'BL', 'BT', 'VT', 'ST', 'CT', 'DN', 'TN', 'AG',
                 'BTH', 'BD', 'TV', 'VL', 'HCM_2', 'LA', 'BP', 'HG', 'KG', 'DL', 'TG')
    def _compute_sum_return(self):
        for r in self:
            if r.return_stock_id.day_of_week == 0:
                r.sum_return = (r.HCM + r.DT + r.CM) * 1000
            elif r.return_stock_id.day_of_week == 1:
                r.sum_return = (r.BL + r.BT + r.VT) * 1000
            elif r.return_stock_id.day_of_week == 2:
                r.sum_return = (r.ST + r.CT + r.DN) * 1000
            elif r.return_stock_id.day_of_week == 3:
                r.sum_return = (r.TN + r.AG + r.BTH) * 1000
            elif r.return_stock_id.day_of_week == 4:
                r.sum_return = (r.BD + r.TV + r.VL) * 1000
            elif r.return_stock_id.day_of_week == 5:
                r.sum_return = (r.HCM_2 + r.LA + r.BP + r.HG) * 1000
            else:
                r.sum_return = (r.KG + r.DL + r.TG) * 1000

    @api.depends('HCM', 'DT', 'CM', 'BL', 'BT', 'VT', 'ST', 'CT', 'DN', 'TN', 'AG',
                 'BTH', 'BD', 'TV', 'VL', 'HCM_2', 'LA', 'BP', 'HG', 'KG', 'DL', 'TG')
    def _compute_consume(self):
        for r in self:
            plans = self.env['planed'].search([('date', '=', r.date)])
            total = 0
            for plan in plans:
                for item in plan.lines:
                    if item.customer_id == r.customer_id:
                        total += item.total
            r.consume = total - r.sum_return

    @api.depends('return_stock_id', 'return_stock_id.day_of_week')
    def _compute_ticket_receive(self):
        for r in self:
            if r.return_stock_id.day_of_week == 0:
                r.ticket_receive = (r.customer_id.HCM + r.customer_id.DT + r.customer_id.CM) * 1000
            elif r.return_stock_id.day_of_week == 1:
                r.ticket_receive = (r.customer_id.BL + r.customer_id.BT + r.customer_id.VT) * 1000
            elif r.return_stock_id.day_of_week == 2:
                r.ticket_receive = (r.customer_id.ST + r.customer_id.CT + r.customer_id.DN) * 1000
            elif r.return_stock_id.day_of_week == 3:
                r.ticket_receive = (r.customer_id.TN + r.customer_id.AG + r.customer_id.BTH) * 1000
            elif r.return_stock_id.day_of_week == 4:
                r.ticket_receive = (r.customer_id.BD + r.customer_id.TV + r.customer_id.VL) * 1000
            elif r.return_stock_id.day_of_week == 5:
                r.ticket_receive = (r.customer_id.HCM_2 + r.customer_id.LA + r.customer_id.BP + r.customer_id.HG) * 1000
            else:
                r.ticket_receive = (r.customer_id.KG + r.customer_id.DL + r.customer_id.TG) * 1000

    @api.depends('ticket_receive', 'sum_return')
    def _compute_revenues(self):
        for r in self:
            r.revenues = r.ticket_receive - r.sum_return * r.customer_id.price


class DataTele(models.Model):
    _name = "data.tele"

    name = fields.Char('Đài')


class ReturnStockTele(models.Model):
    _name = "return.stock.tele"

    return_stock_id = fields.Many2one('return.stock')
    data_tele_id = fields.Many2one('data.tele', "Đài", readonly=1)

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