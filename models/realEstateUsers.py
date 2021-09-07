from odoo import models, fields

class RealEstateUsersInherite(models.Model):

    # display the list of properties linked to the owner directly 
    # in the Settings / Users & Companies / Users form view
    # (view inheritance)
    _inherit = "res.users"
    property_ids = fields.One2many("realestate.properties", "owner_id", string = "Property name", readonly=True)