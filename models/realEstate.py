from odoo import api, models, fields
from datetime import datetime, timedelta

class RealEstate(models.Model):
    _name = 'realestate.properties'
    _description = 'Here Real Estate information is stored.'

    name = fields.Char(string='Title')
    description = fields.Text(string='Description')

    post_code = fields.Char(string='Post Code')
    exp_price = fields.Integer(string='Expected price')
    bedrooms = fields.Integer(string='Bedrooms', default=3)
    facades = fields.Integer(string='Facades')
    garden = fields.Boolean()
    garden_orient = fields.Selection([('north_south', 'North to south'),
        ('east_west', 'East to west')], string='Garden orientation')
    
    available = fields.Date(string='Available from', default= fields.datetime.now(), copy=False)
    deadline = fields.Date(string='Deadline', inverse="_inverse_total")
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False, compute="_compute_total")
    living_area = fields.Integer(string='Living area(sqm)')
    garage = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area(sqm)')
    status = fields.Selection([("new", "New"), ("offer_received", "Offer Received"),
        ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("canceled", "Canceled")], 
        copy=False, default="new")

    total_area = fields.Float(compute="_compute_total", readonly=True)

    @api.depends("living_area","garden_area", "selling_price", "available")
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area
            record.selling_price = record.total_area * 20

    def _inverse_total(self):
        for record in self:
            record.deadline = record.available + timedelta(days=10)