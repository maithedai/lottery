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

    HCM = fields.Integer(string='TP HCM', default=0)
    HCM_PC = fields.Float(string='TP HCM', readonly=1, compute="_compute_percent_back")

    DT = fields.Integer(string='ĐT', sum="Tổng số")
    DT_PC = fields.Float(string='ĐT', readonly=1, compute="_compute_percent_back")

    CM = fields.Integer(string='CM')
    CM_PC = fields.Float(string='CM', readonly=1, compute="_compute_percent_back")

    BL = fields.Integer(string='CM')
    BL_PC = fields.Float(string='BL', readonly=1, compute="_compute_percent_back")

    BT = fields.Integer(string='BT')
    BT_PC = fields.Float(string='BT', readonly=1, compute="_compute_percent_back")

    VT = fields.Integer(string='VT')
    VT_PC = fields.Float(string='VT', readonly=1, compute="_compute_percent_back")

    ST = fields.Integer(string='ST')
    ST_PC = fields.Float(string='ST', readonly=1, compute="_compute_percent_back")

    CT = fields.Integer(string='ST')
    CT_PC = fields.Float(string='CT', readonly=1, compute="_compute_percent_back")

    DN = fields.Integer(string='ĐN')
    DN_PC = fields.Float(string='ĐN', readonly=1, compute="_compute_percent_back")

    TN = fields.Integer(string='TN')
    TN_PC = fields.Float(string='TN', readonly=1, compute="_compute_percent_back")

    AG = fields.Integer(string='AG')
    AG_PC = fields.Float(string='AG', readonly=1, compute="_compute_percent_back")

    BTH = fields.Integer(string='BTH')
    BTH_PC = fields.Float(string='BTH', readonly=1, compute="_compute_percent_back")

    BD = fields.Integer(string='BD')
    BD_PC = fields.Float(string='BD', readonly=1, compute="_compute_percent_back")

    TV = fields.Integer(string='TV')
    TV_PC = fields.Float(string='TV', readonly=1, compute="_compute_percent_back")

    VL = fields.Integer(string='VL')
    VL_PC = fields.Float(string='VL', readonly=1, compute="_compute_percent_back")

    HCM_2 = fields.Integer(string='TP HCM')
    HCM_2_PC = fields.Float(string='TP HCM', readonly=1, compute="_compute_percent_back")

    LA = fields.Integer(string='LA')
    LA_PC = fields.Float(string='LA', readonly=1, compute="_compute_percent_back")

    BP = fields.Integer(string='BP')
    BP_PC = fields.Float(string='BP', readonly=1, compute="_compute_percent_back")

    HG = fields.Integer(string='HG')
    HG_PC = fields.Float(string='HG', readonly=1, compute="_compute_percent_back")

    KG = fields.Integer(string='KG')
    KG_PC = fields.Float(string='KG', readonly=1, compute="_compute_percent_back")

    DL = fields.Integer(string='ĐL')
    DL_PC = fields.Float(string='ĐL', readonly=1, compute="_compute_percent_back")

    TG = fields.Integer(string='TG')
    TG_PC = fields.Float(string='TG', readonly=1, compute="_compute_percent_back")

    percent = fields.Float("%", compute="_compute_percent")
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
            plan = self.env['planed.line'].search([('date', '=', r.date), ('customer_id', '=', r.customer_id.id)])
            total = sum(plan.mapped('total'))
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

    @api.depends('HCM', 'DT', 'CM', 'BL', 'BT', 'VT', 'ST', 'CT', 'DN', 'TN', 'AG',
                 'BTH', 'BD', 'TV', 'VL', 'HCM_2', 'LA', 'BP', 'HG', 'KG', 'DL', 'TG')
    def _compute_percent_back(self):
        for r in self:
            r.HCM_PC = r.HCM / r.customer_id.HCM if r.customer_id.HCM > 0 else 0
            r.DT_PC = r.DT / r.customer_id.DT if r.customer_id.DT > 0 else 0
            r.CM_PC = r.CM / r.customer_id.CM if r.customer_id.CM > 0 else 0
            r.BL_PC = r.BL / r.customer_id.BL if r.customer_id.BL > 0 else 0
            r.BT_PC = r.BT / r.customer_id.BT if r.customer_id.BT > 0 else 0
            r.VT_PC = r.VT / r.customer_id.VT if r.customer_id.VT > 0 else 0
            r.ST_PC = r.ST / r.customer_id.ST if r.customer_id.ST > 0 else 0
            r.CT_PC = r.CT / r.customer_id.CT if r.customer_id.CT > 0 else 0
            r.DN_PC = r.DN / r.customer_id.DN if r.customer_id.DN > 0 else 0
            r.TN_PC = r.TN / r.customer_id.TN if r.customer_id.TN > 0 else 0
            r.AG_PC = r.AG / r.customer_id.AG if r.customer_id.AG > 0 else 0
            r.BTH_PC = r.BTH / r.customer_id.BTH if r.customer_id.BTH > 0 else 0
            r.BD_PC = r.BD / r.customer_id.BD if r.customer_id.BD > 0 else 0
            r.TV_PC = r.TV / r.customer_id.TV if r.customer_id.TV > 0 else 0
            r.VL_PC = r.VL / r.customer_id.VL if r.customer_id.VL > 0 else 0
            r.HCM_2_PC = r.HCM_2 / r.customer_id.HCM_2 if r.customer_id.HCM_2 > 0 else 0
            r.LA_PC = r.LA / r.customer_id.LA if r.customer_id.LA > 0 else 0
            r.BP_PC = r.BP / r.customer_id.BP if r.customer_id.BP > 0 else 0
            r.HG_PC = r.HG / r.customer_id.HG if r.customer_id.HG > 0 else 0
            r.KG_PC = r.KG / r.customer_id.KG if r.customer_id.KG > 0 else 0
            r.DL_PC = r.DL / r.customer_id.DL if r.customer_id.DL > 0 else 0
            r.TG_PC = r.TG / r.customer_id.TG if r.customer_id.TG > 0 else 0

    @api.depends('HCM_PC', 'DT_PC', 'CM_PC', 'BL_PC', 'BT_PC', 'VT_PC', 'ST_PC', 'CT_PC', 'DN_PC', 'TN_PC', 'AG_PC',
                 'BTH_PC', 'BD_PC', 'TV_PC', 'VL_PC', 'HCM_2_PC', 'LA_PC', 'BP_PC', 'HG_PC', 'KG_PC', 'DL_PC', 'TG_PC')
    def _compute_percent(self):
        for r in self:
            if r.return_stock_id.day_of_week == 0:
                r.percent = (r.HCM_PC + r.DT_PC + r.CM_PC) / 3
            elif r.return_stock_id.day_of_week == 1:
                r.percent = (r.BL_PC + r.BT_PC + r.VT_PC) / 3
            elif r.return_stock_id.day_of_week == 2:
                r.percent = (r.ST_PC + r.CT_PC + r.DN_PC) / 3
            elif r.return_stock_id.day_of_week == 3:
                r.percent = (r.TN_PC + r.AG_PC + r.BTH_PC) / 3
            elif r.return_stock_id.day_of_week == 4:
                r.percent = (r.BD_PC + r.TV_PC + r.VL_PC) / 3
            elif r.return_stock_id.day_of_week == 5:
                r.percent = (r.HCM_2_PC + r.LA_PC + r.BP_PC + r.HG_PC) / 3
            else:
                r.percent = (r.KG_PC + r.DL_PC + r.TG_PC) / 3


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