# -*- coding: utf-8 -*-

from odoo import api ,fields, models,exceptions
import logging
from odoo.exceptions import ValidationError
_logger = logging.getLogger(__name__)

class Build_Property_history(models.Model):
    _name = "pie.build.history"

    #name = fields.Char(related='property_code')
    #project = fields.Char(string="Project",size=150)
    active = fields.Boolean('Active', default=True)
    developer = fields.Char(string="Developer",size=150)
    project = fields.Char(string="Project",size=150)
    zone = fields.Char(string="Zone",size=150)
    district = fields.Char(string="District",size=150)
    plot = fields.Char(string="Plot",size=150)
    region = fields.Char(string="Region",size=150)
    area = fields.Char(string="Area",size=150)
    

    property_id = fields.Char(string="Property PIE ID",size=350)
    property_code = fields.Char(string="Property Code",size=150)
    design_code = fields.Char(string="Design Code",size=150)
    property_type = fields.Char(string="Property Type",size=150)
    property_design = fields.Char(string="Property Design",size=150)

    rooms = fields.Char(string="Count of Rooms",size=150)
    baths = fields.Char(string="Count of Baths",size=150)
    price = fields.Float(string="Property Cash Price",size=150)
    delivery_date = fields.Date(string="Property Delivery Date",size=150)
    built_up = fields.Float(string="Built Space",size=150)
    land_m = fields.Float(string="Land Space",size=150)
    garden_m = fields.Float(string="Garden Space",size=150)
    terrace_m = fields.Float(string="Terrace Space",size=150)
    basement_m = fields.Float(string="Basement Space",size=150)
    roof_m = fields.Float(string="roof Space",size=150)
    garage_slot = fields.Integer(string="Count of Garage Slots",size=150)

    finishing_type =fields.Char(string="Finishing Type",size=150)
    property_status =fields.Char(string="Property Status",size=150)
    property_category =fields.Char(string="Property Category",size=150)
    property_commercial =fields.Char(string="Property Category",size=150)
    property_residental =fields.Char(string="Property Category",size=150)
    property_floor =fields.Char(string="Property Category",size=150)
    maintne_fee =fields.Float(string="Maintenance Fees",size=150)
    clubhouse_fee =fields.Float(string="Clubhouse Fees",size=150)
    garage_price =fields.Float(string="Garage Slot Price",size=150)
    media_link =fields.Char(string="Media link",size=150)
    remark =fields.Char(string="Property Remark",size=150)


    is_primary = fields.Boolean(string='Primary Market')
    has_errors = fields.Boolean(string='Has Errors')
    is_secondary = fields.Boolean(string='Secondary Market')
    sharing_level = fields.Selection([('public','Public'),('private','Private')],default='public')
    upload_date = fields.Date(string='Upload Date')


    current_user = fields.Many2one('res.users','Current User', default=lambda self: self.env.user)
    supplier_id = fields.Integer('Supplier ID')
    supplier = fields.Many2one('pie.entity',size=150)
    importid = fields.Integer(string="Import ID",size=150)

    @api.multi
    def validate_prop(self):
        for record in self:
            gl_project = ''
            gl_region = ''
            gl_area = ''
            gl_property_type = ''
            gl_property_design =''
            gl_finishing_type =''
            gl_property_status =''
            _logger.warn(record.project)
            #project = self.env['pie.project'].search(['name', 'Like', self.project])
            if record.project:
                project = self.env['pie.project'].search([('project_name', 'like', record.project.name)])
                if project:
                    _logger.warn(project.region)
                    gl_project = project
                    prop = self.env['pie.build.draft'].search([('id', '=', record.id)])
                    
                else:
                    _logger.warn("Project Wasn't Found")
                    raise exceptions.ValidationError("Project Wasn't Found on System")
                
            
            else:
                _logger.warn("No Project")
                raise exceptions.ValidationError("You Have to enter Project")

            if record.region:
                
                region = self.env['pie.setup.region'].search([('name', 'like', record.region)])
                gl_region= region
                if region:
                    _logger.warn(record.region)
                else:
                    _logger.warn("Region Wasn't Found")
                    raise exceptions.ValidationError("Region Wasn't Found on System")
                
            
            else:
                _logger.warn("No Region")
                raise exceptions.ValidationError("You Have to enter Region") 

            if record.area:
                area = self.env['pie.setup.area'].search([('name', 'like', record.area)])
                gl_area=area
                if area:
                    _logger.warn(record.area)
                else:
                    _logger.warn("Area Wasn't Found")
                    raise exceptions.ValidationError("Area Wasn't Found on System")
                
            
            else:
                _logger.warn("No area")
                raise exceptions.ValidationError("You Have to enter area") 

            if not record.property_type:
                gl_property_type = property_type
                _logger.warn("Property Type Wasn't Found")
                raise exceptions.ValidationError("Property Type isn't present")

            if not record.price or record.price == 0:
                _logger.warn("Price Wasn't Found")
                raise exceptions.ValidationError("Price Cannot be empty or 0")

            if not record.built_up or record.built_up == 0:
                _logger.warn("Price Wasn't Found")
                raise exceptions.ValidationError("Built Space Cannot be empty or 0")

            if record.finishing_type:
                
                finishing_type = self.env['pie.setup.finishing'].search([('name', '=', record.finishing_type)])
                gl_finishing_type = finishing_type
                if finishing_type:
                    _logger.warn(record.finishing_type)
                else:
                    _logger.warn("Finishing Type Wasn't Found")
                    raise exceptions.ValidationError("Finishing Type Wasn't Found on System")
                
            
            else:
                _logger.warn("No finishing_type")
                raise exceptions.ValidationError("You Have to enter Finishing Type") 

            if record.property_status:

                property_status = self.env['pie.setup.property_status'].search([('name', '=', record.property_status)])
                gl_property_status = property_status
                if property_status:
                    _logger.warn(record.property_status)
                else:
                    _logger.warn("property_status Type Wasn't Found")
                    raise exceptions.ValidationError("Property Status Wasn't Found on System")
                
            
            else:
                _logger.warn("No property_status")
                raise exceptions.ValidationError("You Have to enter Property Status") 
            _logger.warn(record.project.id)
            _logger.warn(gl_region)
            self.env['pie.build.property'].create({'active':prop.active,
            'property_code':prop.property_code,
            'project':record.project.id,
            'region':gl_region.id,
            'area':gl_area.id,
            'property_type':gl_property_type,
            'property_design':record.property_design,
            'price':prop.price,
            'built_up':prop.built_up,
            'finishing_type':gl_finishing_type.id,
            'property_status':gl_property_status.id,
            })