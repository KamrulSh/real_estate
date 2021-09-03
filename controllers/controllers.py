# -*- coding: utf-8 -*-
# from odoo import http


# class RealState(http.Controller):
#     @http.route('/real_state/real_state/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/real_state/real_state/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('real_state.listing', {
#             'root': '/real_state/real_state',
#             'objects': http.request.env['real_state.real_state'].search([]),
#         })

#     @http.route('/real_state/real_state/objects/<model("real_state.real_state"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('real_state.object', {
#             'object': obj
#         })
