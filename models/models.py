# -*- coding: utf-8 -*-

from odoo import models, fields, api


class inherit_stock_picking_2(models.Model):
    _inherit = 'stock.rule'

    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id,
                               values):
        result = super(inherit_stock_picking_2, self)._get_stock_move_values(product_id, product_qty, product_uom,
                                                                             location_id, name,
                                                                             origin, company_id, values)
        if values['sale_line_id']:
            sessions = self.env['sale.order.line'].browse(values['sale_line_id'])
            result['price_unit'] = sessions.price_unit
            result['tax_id'] = sessions.tax_id
        return result


class inherit_stock_picking_1(models.Model):
    _inherit = 'stock.picking'

    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all', tracking=4)
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all', tracking=5)
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all')
    currency_id = fields.Many2one(
        'res.currency', string='Currency')

    @api.depends('move_lines.price_total')
    def _amount_all(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.move_lines:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax,
            })


class inherit_stock_picking(models.Model):
    _inherit = 'stock.move'

    price_unit = fields.Monetary('Unit Price', required=True, digits='Product Price', default=0.0)
    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', readonly=True, store=True)
    price_tax = fields.Monetary(compute='_compute_amount', string='Total Tax', readonly=True, store=True)
    price_total = fields.Monetary(compute='_compute_amount', string='Total', readonly=True, store=True)
    tax_id = fields.Many2many('account.tax', string='Taxes',
                              domain=['|', ('active', '=', False), ('active', '=', True)])
    currency_id = fields.Many2one('res.currency', string='Currency')

    @api.depends('product_uom_qty', 'price_unit', 'tax_id')
    def _compute_amount(self):
        for line in self:
            price = line.price_unit
            taxes = line.tax_id.compute_all(price, line.picking_id.currency_id, line.product_uom_qty,
                                            product=line.product_id, partner=line.picking_id.partner_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
