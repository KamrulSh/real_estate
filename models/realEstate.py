from odoo import models, fields

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
    
    available = fields.Date(string='Available from', default=lambda self: fields.Datetime.now(), copy=False)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    living_area = fields.Integer(string='Living area(sqm)')
    garage = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area(sqm)')
    status = fields.Selection([("new", "New"), ("offer_received", "Offer Received"),
        ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("canceled", "Canceled")], 
        copy=False, default="new")
