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
    code = fields.Char('Code')


class ReturnStockTele(models.Model):
    _name = "return.stock.tele"

    return_stock_id = fields.Many2one('return.stock')
    data_tele_id = fields.Many2one('data.tele', "Đài", readonly=1)

    HCM = fields.Char(string='TP HCM', compute="_compute_tele_value")
    DT = fields.Char(string='ĐT', compute="_compute_tele_value")
    CM = fields.Char(string='CM', compute="_compute_tele_value")
    BL = fields.Char(string='CM', compute="_compute_tele_value")
    BT = fields.Char(string='BT', compute="_compute_tele_value")
    VT = fields.Char(string='VT', compute="_compute_tele_value")
    ST = fields.Char(string='ST', compute="_compute_tele_value")
    CT = fields.Char(string='ST', compute="_compute_tele_value")
    DN = fields.Char(string='ĐN', compute="_compute_tele_value")
    TN = fields.Char(string='TN', compute="_compute_tele_value")
    AG = fields.Char(string='AG', compute="_compute_tele_value")
    BTH = fields.Char(string='BTH', compute="_compute_tele_value")
    BD = fields.Char(string='BD', compute="_compute_tele_value")
    TV = fields.Char(string='TV', compute="_compute_tele_value")
    VL = fields.Char(string='VL', compute="_compute_tele_value")
    HCM_2 = fields.Char(string='TP HCM', compute="_compute_tele_value")
    LA = fields.Char(string='LA', compute="_compute_tele_value")
    BP = fields.Char(string='BP', compute="_compute_tele_value")
    HG = fields.Char(string='HG', compute="_compute_tele_value")
    KG = fields.Char(string='KG', compute="_compute_tele_value")
    DL = fields.Char(string='ĐL', compute="_compute_tele_value")
    TG = fields.Char(string='TG', compute="_compute_tele_value")

    @api.depends('return_stock_id', 'return_stock_id.lines')
    def _compute_tele_value(self):
        for r in self:
            if r.data_tele_id.code == 'slte':
                r.HCM = str(sum(r.return_stock_id.lines.mapped('HCM')))
                r.DT = str(sum(r.return_stock_id.lines.mapped('DT')))
                r.CM = str(sum(r.return_stock_id.lines.mapped('CM')))
                r.BL = str(sum(r.return_stock_id.lines.mapped('BL')))
                r.BT = str(sum(r.return_stock_id.lines.mapped('BT')))
                r.VT = str(sum(r.return_stock_id.lines.mapped('VT')))
                r.ST = str(sum(r.return_stock_id.lines.mapped('ST')))
                r.CT = str(sum(r.return_stock_id.lines.mapped('CT')))
                r.DN = str(sum(r.return_stock_id.lines.mapped('DN')))
                r.TN = str(sum(r.return_stock_id.lines.mapped('TN')))
                r.AG = str(sum(r.return_stock_id.lines.mapped('AG')))
                r.BTH = str(sum(r.return_stock_id.lines.mapped('BTH')))
                r.BD = str(sum(r.return_stock_id.lines.mapped('BD')))
                r.TV = str(sum(r.return_stock_id.lines.mapped('TV')))
                r.VL = str(sum(r.return_stock_id.lines.mapped('VL')))
                r.HCM_2 = str(sum(r.return_stock_id.lines.mapped('HCM_2')))
                r.LA = str(sum(r.return_stock_id.lines.mapped('LA')))
                r.BP = str(sum(r.return_stock_id.lines.mapped('BP')))
                r.HG = str(sum(r.return_stock_id.lines.mapped('HG')))
                r.KG = str(sum(r.return_stock_id.lines.mapped('KG')))
                r.DL = str(sum(r.return_stock_id.lines.mapped('DL')))
                r.TG = str(sum(r.return_stock_id.lines.mapped('TG')))
            elif r.data_tele_id.code == 'tl':
                r.HCM = str(sum(r.return_stock_id.lines.mapped('HCM'))) + '%'
                r.DT = str(sum(r.return_stock_id.lines.mapped('HCM'))) + '%'
                r.CM = str(sum(r.return_stock_id.lines.mapped('HCM'))) + '%'
                r.BL = str(sum(r.return_stock_id.lines.mapped('HCM'))) + '%'
                r.BT = str(sum(r.return_stock_id.lines.mapped('HCM'))) + '%'
                r.VT = str(sum(r.return_stock_id.lines.mapped('HCM'))) + '%'
                r.ST = str(sum(r.return_stock_id.lines.mapped('HCM'))) + '%'
                r.CT = str(sum(r.return_stock_id.lines.mapped('HCM'))) + '%'
                r.DN = str(sum(r.return_stock_id.lines.mapped('HCM'))) + '%'
                r.TN = str(sum(r.return_stock_id.lines.mapped('HCM'))) + '%'
                r.AG = str(sum(r.return_stock_id.lines.mapped('HCM'))) + '%'
                r.BTH = str(sum(r.return_stock_id.lines.mapped('HCM'))) + '%'
                r.BD = str(sum(r.return_stock_id.lines.mapped('HCM'))) + '%'
                r.TV = str(sum(r.return_stock_id.lines.mapped('HCM'))) + '%'
                r.VL = str(sum(r.return_stock_id.lines.mapped('HCM'))) + '%'
                r.HCM_2 = str(sum(r.return_stock_id.lines.mapped('HCM'))) + '%'
                r.LA = str(sum(r.return_stock_id.lines.mapped('HCM'))) + '%'
                r.BP = str(sum(r.return_stock_id.lines.mapped('HCM'))) + '%'
                r.HG = str(sum(r.return_stock_id.lines.mapped('HCM'))) + '%'
                r.KG = str(sum(r.return_stock_id.lines.mapped('HCM'))) + '%'
                r.DL = str(sum(r.return_stock_id.lines.mapped('HCM'))) + '%'
                r.TG = str(sum(r.return_stock_id.lines.mapped('HCM'))) + '%'
            else:
                r.HCM = ''
                r.DT = ''
                r.CM = ''
                r.BL = ''
                r.BT = ''
                r.VT = ''
                r.ST = ''
                r.CT = ''
                r.DN = ''
                r.TN = ''
                r.AG = ''
                r.BTH = ''
                r.BD = ''
                r.TV = ''
                r.VL = ''
                r.HCM_2 = ''
                r.LA = ''
                r.BP = ''
                r.HG = ''
                r.KG = ''
                r.DL = ''
                r.TG = ''