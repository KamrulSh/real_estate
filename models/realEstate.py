import re
from odoo.exceptions import ValidationError
from odoo import api, models, fields
from datetime import timedelta

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

    email_id = fields.Char(String="Email address")
    total_area = fields.Float(compute="_compute_total", readonly=True)

    # implement sql constraints
    _sql_constraints = [
        ('check_exp_price', 'CHECK(exp_price > 0)', 'The expected price must be strictly positive'),
        ('check_living_area', 'CHECK(living_area > 0)', 'The living area must be positive'),
        ('check_garden_area', 'CHECK(garden_area >= 0)', 'The garden area must be positive'),
        ('check_unique_email', 'UNIQUE(email_id)',   "The Email must be unique")
    ]
    
    # implement python constraints
    @api.constrains('exp_price')
    def _check_sellings_price(self):
        for record in self:
            if record.exp_price < record.selling_price*0.9 or record.exp_price > record.selling_price:
                raise ValidationError(f"""The expected price cannot be lower than 90% or more then 100% of selling price. 
                Please make sure your price is between {record.selling_price*0.9} and {record.selling_price}""")

    # implement computed fields and inverse function
    @api.depends("living_area","garden_area", "selling_price", "available")
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area
            record.selling_price = record.total_area * 20

    def _inverse_total(self):
        for record in self:
            record.deadline = record.available + timedelta(days=10)
            
    # implement email validation regex
    @api.onchange('email_id')
    def validate_mail(self):
       if self.email_id:
           match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email_id)
           if match == None:
               raise ValidationError('Not a valid E-mail ID')