# -*- coding: utf-8 -*-

from odoo import api ,fields, models,exceptions
import logging
from odoo.exceptions import ValidationError
_logger = logging.getLogger(__name__)

class Build_Property_draft(models.Model):
    _name = "pie.build.draft"

    #name = fields.Char(related='property_code')
    #project = fields.Char(string="Project",size=150)
    active = fields.Boolean(string='Active', default=True)
    developer = fields.Char(string= 'Developer',size=150)
    project = fields.Char(string='Project',size=150)

    zone = fields.Char(string="Zone",size=150)
    district = fields.Char(string="District",size=150)
    phase = fields.Char(string="Phaze",size=150)
    plot = fields.Char(string="Plot",size=150)
    region = fields.Char(string="Region",size=150)
    area = fields.Char(string="Area",size=150)
    

    property_id = fields.Char(string="Property PIE ID",size=350)
    property_code = fields.Char(string="Property Code",size=150)
    design_code = fields.Char(string="Design Code",size=150)
    property_type = fields.Char(string="Property Type",size=150)
    property_design = fields.Char(string="Property Design",size=150)

    rooms_l = fields.Many2one('pie.setup.rooms',string="Rooms",size=150)
    baths_l = fields.Many2one('pie.setup.bathrooms',string="Baths",size=150)
    
    rooms = fields.Integer(string="Rooms",size=150)
    baths = fields.Integer(string="Baths",size=150)
    price = fields.Float(string="Property Cash Price",size=150)
    delivery_date = fields.Date(string="Property Delivery Date",size=150)

    built_up = fields.Float(string="Built Space",size=150)
    land_m = fields.Float(string="Land Space",size=150)
    garden_m = fields.Float(string="Garden Space",size=150)
    terrace_m = fields.Float(string="Terrace Space",size=150)
    basement_m = fields.Float(string="Basement Space",size=150)
    roof_m = fields.Float(string="roof Space",size=150)
    garage_slot = fields.Float(string="Count of Garage Slots",size=150)
    garage_slot_price = fields.Float(string="Price of Garage Slot",size=150)

    finishing_type =fields.Char(string="Finishing Type",size=150)
    finishing_price = fields.Float(string="Finishing Price",size=150)

    property_status =fields.Char(string="Property Status",size=150)

    property_category =fields.Char(string="Property Category",size=150)

    property_floor =fields.Char(string="Property Floor",size=150)
    maintne_fee =fields.Float(string="Maintenance Fees",size=150)
    clubhouse_fee =fields.Float(string="Clubhouse Fees",size=150)
    
    media_link =fields.Char(string="Media link",size=150)
    remark =fields.Text(string="Property Remark",size=150)


    is_primary = fields.Boolean(string='Primary Market')
    has_errors = fields.Boolean(string='Has Errors')
    is_secondary = fields.Boolean(string='Secondary Market')
    sharing_level = fields.Selection([('public','Public'),('private','Private')],default='public')
    upload_date = fields.Date(string='Upload Date')


    #current_user = fields.Many2one('res.users','Current User', default=lambda self: self.env.user)
    supplier_id = fields.Integer('Supplier ID')
    supplier = fields.Many2one('pie.entity',size=150)
    #import_id = fields.Integer(string="Import ID",size=150)
    #import_id = fields.Many2one('pie.build.import',string="Import ID",size=150)
    importid = fields.Integer(string="Import ID",size=150)


  
    def validate_project(self,props):
        for prop in props:
            gl_project = ''
            _logger.warn(prop)
            #project = self.env['pie.project'].search(['name', 'Like', self.project])
            if prop.project:
                _logger.warn(prop.project)
                project = self.env['pie.project'].search([('name', '=ilike', prop.project)])
                _logger.warn(project)
                if project:
                    gl_project = project
                    #prop = self.env['pie.build.draft'].search([('id', '=', record.id)])
                    prop.project = project.name
                else:
                    _logger.warn("Project Wasn't Found for Record")
                    raise exceptions.ValidationError("Project Wasn't Found on System")
            else:
                _logger.warn("No Project")
                raise exceptions.ValidationError("You Have to enter Project")
        return props

    def validate_prop_type(self,props):
        for prop in props:
            

            res = self.env['pie.setup.category'].search([])
            _logger.warn(res)
            #project = self.env['pie.project'].search(['name', 'Like', self.project])
            if prop.property_type:
                _logger.warn(prop.property_type)
                _logger.warn('#########################')
                typee = self.env['pie.setup.category'].search([('name', '=ilike', prop.property_type)])
                _logger.warn(typee)
                if typee:
                    _logger.warn(typee)
                    _logger.warn('ppppppppp#########################')
                    #prop = self.env['pie.build.draft'].search([('id', '=', record.id)])
                    prop.property_type = typee.name
                else:
                    _logger.warn("Project Wasn't Found for Record")
                    raise exceptions.ValidationError("Project Wasn't Found on System")
                
            
            else:
                _logger.warn("No Project")
                raise exceptions.ValidationError("You Have to enter Project")
        return props

    def validate_prop_design(self,props):
        for prop in props:
            _logger.warn(prop)
            #_logger.warn(prop.project)
            #project = self.env['pie.project'].search(['name', 'Like', self.project])
            if prop.property_design:
                _logger.warn(prop.property_design)
                property_design = self.env['pie.setup.property_design'].search([('name', '=ilike', prop.property_design)])
                if property_design:
                    
                    #gl_project = property_design
                    #prop = self.env['pie.build.draft'].search([('id', '=', record.id)])
                    prop.property_design = property_design.name
                else:
                    _logger.warn("Project Wasn't Found for Record")
                    raise exceptions.ValidationError("Project Wasn't Found on System")
                
            
            else:
                _logger.warn("No Project")
                raise exceptions.ValidationError("You Have to enter Project")
        return props
    def validate_prop_finishing(self,props):
        for prop in props:
            
            #_logger.warn(prop.project)
            #project = self.env['pie.project'].search(['name', 'Like', self.project])
            if prop.finishing_type:
                project = self.env['pie.setup.finishing'].search([('name', '=ilike', prop.finishing_type)])
                if project:
                    
                    gl_project = project
                    #prop = self.env['pie.build.draft'].search([('id', '=', record.id)])
                    prop.finishing_type = project.name
                else:
                    _logger.warn("Project Wasn't Found for Record")
                    raise exceptions.ValidationError("Project Wasn't Found on System")
                
            
            else:
                _logger.warn("No Project")
                raise exceptions.ValidationError("You Have to enter Project")
        return props

    def validate_prop_status(self,props):
        for prop in props:
            
            #_logger.warn(prop.project)
            #project = self.env['pie.project'].search(['name', 'Like', self.project])
            if prop.property_status:
                project = self.env['pie.setup.property_status'].search([('name', '=ilike', prop.property_status)])
                if project:
                    
                    gl_project = project
                    #prop = self.env['pie.build.draft'].search([('id', '=', record.id)])
                    prop.property_status = project.name
                else:
                    _logger.warn("Project Wasn't Found for Record")
                    raise exceptions.ValidationError("Project Wasn't Found on System")
                
            
            else:
                _logger.warn("No Project")
                raise exceptions.ValidationError("You Have to enter Project")
        return props

    def validate_prop_built(self,props):
        for prop in props:
            
            #_logger.warn(prop.project)
            #project = self.env['pie.project'].search(['name', 'Like', self.project])
            if prop.built_up == 0:
                raise exceptions.ValidationError("Project Wasn't Found on System")
                

        return props

    def validate_prop_price(self,props):
        for prop in props:
            
            #_logger.warn(prop.project)
            #project = self.env['pie.project'].search(['name', 'Like', self.project])
            if prop.price == 0:
                raise exceptions.ValidationError("Project Wasn't Found on System")
                

        return props