import re
from odoo.exceptions import ValidationError
from odoo import api, models, fields
from datetime import timedelta

class RealEstate(models.Model):
    _name = 'realestate.properties'
    _description = 'Here Real Estate information is stored.'

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    photo = fields.Binary(string="Photo", attachment=True)

    post_code = fields.Char(string='Post Code', required=True)
    expected_price = fields.Integer(string='Expected price', required=True)
    bedrooms = fields.Integer(string='Bedrooms', default=3, required=True)
    facades = fields.Integer(string='Facades')
    garden = fields.Boolean()
    garden_orient = fields.Selection([('north', 'North'), ('south', 'South'),
        ('east', 'East'), ('west', 'West')], string='Garden orientation')
    garden_area = fields.Float(string='Garden Area(sqm)')

    available_from = fields.Date(string='Available from', default= fields.datetime.now(), copy=False)
    deadline = fields.Date(string='Deadline', inverse="_inverse_total")
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False, compute="_compute_total")
    living_area = fields.Float(string='Living area(sqm)', required=True, default=1000)
    garage = fields.Boolean()
    status = fields.Selection([("new", "New"), ("offer_received", "Offer Received"),
        ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("canceled", "Canceled")], 
        copy=False, default="new")
    active = fields.Boolean(default=True)

    email_id = fields.Char(String="Email address", required=True)
    total_area = fields.Float(compute="_compute_total", readonly=True)

    # allows to create new users from realestate (delegation inheritance)
    # or choose old users from users
    # as it provides transparent access to the fields of this users record.

    _inherits = {'res.users':'owner_id'}
    owner_id = fields.Many2one("res.users", string="Owner/sales person")

    # implement sql constraints
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)', 'The expected price must be positive and greater than 0'),
        ('check_living_area', 'CHECK(living_area > 0)', 'The living area must be positive and greater than 0'),
        ('check_unique_email', 'UNIQUE(email_id)', "The Email must be unique"),
    ]
    
    # implement python constraints
    @api.constrains('expected_price', 'selling_price', 'garden')
    def _check_sellings_price(self):
        for record in self:
            if record.garden == False or record.garden == True:
                if record.expected_price < record.selling_price*0.9 or record.expected_price > record.selling_price:
                    raise ValidationError(f"""The expected price cannot be lower than 90% or more then 100% of selling price. 
                    Please make sure your price is between {record.selling_price*0.9} and {record.selling_price}""")
            # A bug:
            # when I don't change record.garden from current state and if I change
            # living_area or garden_area then new selling_price will be calculated.
            # But if I keep previous expected_price it won't check validation
            # for updated selling_price and can be able to save in the database

    @api.constrains('garden', 'garden_area')         
    def _check_garden_area(self):
        for record in self:
            if record.garden == True and record.garden_area <= 0:
                raise ValidationError("The garden area must be greater than 0")

    # implement computed fields and inverse function
    @api.depends("living_area", "garden", "garden_area", "selling_price", "available_from")
    def _compute_total(self):
        for record in self:
            if record.garden == False:
                record.garden_area = 0
                record.total_area = record.living_area
                record.selling_price = record.total_area * 20
            else:
                record.total_area = record.garden_area + record.living_area
                record.selling_price = record.total_area * 25

    def _inverse_total(self):
        for record in self:
            record.deadline = record.available_from + timedelta(days=10)
            
    # implement email validation regex
    @api.onchange('email_id')
    def validate_mail(self):
       if self.email_id:
           match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email_id)
           if match == None:
               raise ValidationError('Not a valid E-mail ID')