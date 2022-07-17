# -*- coding: utf-8 -*-
# from odoo import http


# class InheritStockPicking(http.Controller):
#     @http.route('/inherit_stock_picking/inherit_stock_picking/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inherit_stock_picking/inherit_stock_picking/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inherit_stock_picking.listing', {
#             'root': '/inherit_stock_picking/inherit_stock_picking',
#             'objects': http.request.env['inherit_stock_picking.inherit_stock_picking'].search([]),
#         })

#     @http.route('/inherit_stock_picking/inherit_stock_picking/objects/<model("inherit_stock_picking.inherit_stock_picking"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inherit_stock_picking.object', {
#             'object': obj
#         })
