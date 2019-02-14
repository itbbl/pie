# -*- coding: utf-8 -*-
from odoo import api ,fields, models,exceptions
import logging
from odoo.exceptions import ValidationError
_logger = logging.getLogger(__name__)


class Build_Property(models.Model):
    _name = "pie.build.property"

    name = fields.Char(string="Property Name",size=150)

    project = fields.Many2one('pie.project',size=150,required=True)
    zone = fields.Char(related='project.zone',size=150)
    district = fields.Char(related='project.district',size=150)
    plot = fields.Char(string="Plot",size=150)
    governorate = fields.Many2one(related='project.governorate',string="Region",size=150)
    area = fields.Many2one(related='project.area',string="Area",size=150)
    district = fields.Many2one(related='project.district',string="Area",size=150)
    developer = fields.Many2one(related='project.developer',string="Developer",size=150)
    
    property_id = fields.Char(string="Property PIE ID",size=350)
    property_code = fields.Char(string="Property Code",size=150)
    design_code = fields.Char(string="Design Code",size=150)
    
    #property_type = fields.Char(string="Property Type",size=150)
    #property_design = fields.Char(string="Property Design",size=150)
    
    property_type = fields.Many2one('pie.setup.category',string="Property Type",size=150)
    property_design = fields.Many2one('pie.setup.property_design',string="Property Design",size=150)
    
    rooms = fields.Integer(string="Count of Rooms",size=150)
    baths = fields.Integer(string="Count of Baths",size=150)
    price = fields.Float(string="Property Cash Price",size=150)
    delivery_date = fields.Date(string="Property Delivery Date",size=150)
    built_up = fields.Float(string="Built Space",size=150)
    land_m = fields.Float(string="Land Space",size=150)
    garden_m = fields.Float(string="Garden Space",size=150)
    terrace_m = fields.Float(string="Terrace Space",size=150)
    basement_m = fields.Float(string="Basement Space",size=150)
    roof_m = fields.Float(string="roof Space",size=150)
    garage_slot = fields.Integer(string="Count of Garage Slots",size=150)
    finishing_type =fields.Many2one('pie.setup.finishing',string="Finishing Type",size=150)
    property_status =fields.Many2one('pie.setup.property_status',string="Property Status",size=150)
    property_category =fields.Many2one('pie.setup.category',string="Property Category",size=150)
    property_floor =fields.Many2one('pie.setup.floor',string="Property Floor",size=150)
    maintne_fee =fields.Float(string="Maintenance Fees",size=150)
    clubhouse_fee =fields.Float(string="Clubhouse Fees",size=150)
    garage_price =fields.Float(string="Garage Slot Price",size=150)
    media_link =fields.Char(string="Media link",size=150)
    remark =fields.Char(string="Property Remark",size=150)
    is_primary = fields.Boolean(string='Primary Market')
    is_secondary = fields.Boolean(string='Secondary Market')
    has_errors = fields.Integer(string='Has Errors')
    sharing_level = fields.Selection([('public','Public'),('private','Private')],default='public')

    current_user = fields.Many2one('res.users','Current User', default=lambda self: self.env.user)
    supplier_id = fields.Integer('Supplier ID')
 
    supplierid = fields.Integer('Supplier ID')
    supplier = fields.Many2one('pie.entity')


    @api.constrains('comments')
    def get_number_comment_bar_user(self):
         
        if len(self.comments)>1:
            raise exceptions.ValidationError('Not Vaild to add other Comment')

    @api.constrains('property_code')
    def validate_property_code(self):
         
        if not self.property_code:
            raise exceptions.ValidationError('Property Code Cannot Be Empty')

    @api.constrains('region')
    def validate_region(self):
         
        if not self.region:
            raise exceptions.ValidationError('Region Code Cannot Be Empty')




    @api.constrains('property_category')
    def validate_property_category(self):
         
        if not self.property_category:
            raise exceptions.ValidationError('Property Category Code Cannot Be Empty')

    @api.constrains('property_design')
    def validate_property_design(self):
         
        if not self.property_design:
            raise exceptions.ValidationError('Property Design Code Cannot Be Empty')

    @api.constrains('price')
    def validate_price(self):
         
        if not self.price or self.price ==0:
            raise exceptions.ValidationError('Price Cannot Be Empty or 0')
    
    @api.constrains('built_up')
    def validate_built_up(self):
         
        if not self.built_up:
            raise exceptions.ValidationError('Built Cannot Be Empty')

    @api.constrains('property_status')
    def validate_property_status(self):
         
        if not self.property_status:
            raise exceptions.ValidationError('Property status Code Cannot Be Empty')

    @api.constrains('finishing_type')
    def validate_finishing_type(self):
         
        if not self.finishing_type:
            raise exceptions.ValidationError('Finishing type Code Cannot Be Empty')

    @api.constrains('name')
    def _check_duplicate_code(self):
        names = self.search([])
        for c in names:
            if self.name.lower() == c.name.lower() and self.id != c.id:
                raise exceptions.exceptions.ValidationError("Error: Name must be unique")
