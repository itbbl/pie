# -*- coding: utf-8 -*-

from odoo import api ,fields, models,exceptions
import logging
_logger = logging.getLogger(__name__)

class PIE_Export_Props(models.Model):
    _name = "pie.build.export"

    developer = fields.Many2one('pie.entity',string="Developer",required=True, domain="[('pie_type', '=', 'is_supplier')]" ,store=True,default=lambda self: self.env.user.entity)
    project = fields.Many2one('pie.project')

    def validate_prop(self,records):
        valid_props = []
        developer = self.developer
        project = self.project
        if self.project:
            recs = self.env['pie.build.import'].search([['supplier','=',developer.id],['project','=',project.id]],order='create_date Desc',limit=1)
            props = self.env['pie.build.draft'].search([['supplier','=',developer.id],['project','ilike',project.name]])
            _logger.warn(props)
        else:
            recs = self.env['pie.build.import'].search([['supplier','=',developer.id]],order='create_date DESC',limit=1)
            props = self.env['pie.build.draft'].search([['supplier','=',developer.id]])
            _logger.warn(props)
        
        
        try:
            #self.env['pie.build.draft'].validate_prop(prop)
            valid_props = self.env['pie.build.draft'].validate_project(props)
            
        except:
            raise exceptions.ValidationError("Invalid Data Found in Project Column")
        


        try:
            #self.env['pie.build.draft'].validate_prop(prop)
            valid_props = self.env['pie.build.draft'].validate_prop_type(props)
        except:
            raise exceptions.ValidationError("Invalid Data Found in Property Type Column")


        try:
            #self.env['pie.build.draft'].validate_prop(prop)
            valid_props = self.env['pie.build.draft'].validate_prop_design(props)
        except:
            raise exceptions.ValidationError("Invalid Data Found in Property Design Column")
        
        try:
            #self.env['pie.build.draft'].validate_prop(prop)
            valid_props = self.env['pie.build.draft'].validate_prop_built(props)
        except:
            raise exceptions.ValidationError("Invalid Data Found in Property Built Up Column")

        try:
            #self.env['pie.build.draft'].validate_prop(prop)
            valid_props = self.env['pie.build.draft'].validate_prop_finishing(props)
        except:
            raise exceptions.ValidationError("Invalid Data Found in Property Finishing Column")

        try:
            #self.env['pie.build.draft'].validate_prop(prop)
            valid_props = self.env['pie.build.draft'].validate_prop_status(props)
        except:
            raise exceptions.ValidationError("Invalid Data Found in Property Status Column")

        try:
            #self.env['pie.build.draft'].validate_prop(prop)
            valid_props = self.env['pie.build.draft'].validate_prop_price(props)
        except:
            raise exceptions.ValidationError("Invalid Data Found in Property Price Column")

        for prope in valid_props:
            _logger.warn(prope.built_up)
            p = {'active':prope.active,
            'property_code':prope.property_code,
            'project':prope.project,
            'property_type':prope.property_type,
            'property_design':prope.property_design,
            'price':prope.price,
            'built_up':prope.built_up,
            'finishing_type':prope.finishing_type,
            'property_status':prope.property_status,
            }
            

            valid_props = self.env['pie.build.property'].create(p)

    def export_prop(self,records):
        _logger.warn(self)
        valid_props = []
        developer = self.developer
        project = self.project
        if self.project:
            recs = self.env['pie.build.import'].search([['supplier','=',developer.id],['project','=',project.id]],order='create_date Desc',limit=1)
            props = self.env['pie.build.draft'].search([['supplier','=',developer.id],['project','ilike', project.name]])
            _logger.warn(props)
        else:
            recs = self.env['pie.build.import'].search([['supplier','=',developer.id]],order='create_date DESC',limit=1)
            props = self.env['pie.build.draft'].search([['supplier','=',developer.id]])
            _logger.warn(props)
        
        
        try:
            #self.env['pie.build.draft'].validate_prop(prop)
            valid_props = self.env['pie.build.draft'].validate_project(props)
            
        except:
            raise exceptions.ValidationError("Invalid Data Found in Project Column")
        


        try:
            #self.env['pie.build.draft'].validate_prop(prop)
            valid_props = self.env['pie.build.draft'].validate_prop_type(props)
        except:
            raise exceptions.ValidationError("Invalid Data Found in Property Type Column")


        try:
            #self.env['pie.build.draft'].validate_prop(prop)
            valid_props = self.env['pie.build.draft'].validate_prop_design(props)
        except:
            raise exceptions.ValidationError("Invalid Data Found in Property Design Column")
        
        try:
            #self.env['pie.build.draft'].validate_prop(prop)
            valid_props = self.env['pie.build.draft'].validate_prop_built(props)
        except:
            raise exceptions.ValidationError("Invalid Data Found in Property Built Up Column")

        try:
            #self.env['pie.build.draft'].validate_prop(prop)
            valid_props = self.env['pie.build.draft'].validate_prop_finishing(props)
        except:
            raise exceptions.ValidationError("Invalid Data Found in Property Finishing Column")

        try:
            #self.env['pie.build.draft'].validate_prop(prop)
            valid_props = self.env['pie.build.draft'].validate_prop_status(props)
        except:
            raise exceptions.ValidationError("Invalid Data Found in Property Status Column")

        try:
            #self.env['pie.build.draft'].validate_prop(prop)
            valid_props = self.env['pie.build.draft'].validate_prop_price(props)
        except:
            raise exceptions.ValidationError("Invalid Data Found in Property Price Column")
        
        if self.project:
            props = self.env['pie.build.property'].search([['supplier','=',developer.id],['project','=',project.id]])
            props2 = self.env['pie.grid.property'].search([['supplier','=',developer.id],['project','=',project.id]])
            _logger.warn(props)
        else:
            props = self.env['pie.build.property'].search([['supplier','=',developer.id]])
            props2 = self.env['pie.grid.property'].search([['supplier','=',developer.id]])
            _logger.warn(props)

        for rec in props:
            rec.unlink()
        for rec in props2:
            rec.unlink()
        self._cr.commit()

        for prope in valid_props:
            _logger.warn(prope.built_up)

            project = self.env['pie.project'].search([('name', '=ilike', prope.project)])
            category = self.env['pie.setup.category'].search([('name', '=ilike', prope.property_type)])
            property_design = self.env['pie.setup.property_design'].search([('name', '=ilike', prope.property_design)])
            property_status = self.env['pie.setup.property_status'].search([('name', '=ilike', prope.property_status)])
            finishing_type = self.env['pie.setup.finishing'].search([('name', '=ilike', prope.finishing_type)])
            p = {'active':prope.active,
            'property_code':prope.property_code,
            'property_id':prope.property_id,
            'project':project.id,
            'property_type':category.id,
            'property_design':property_design.id,
            'price':prope.price,
            'built_up':prope.built_up,
            'finishing_type':finishing_type.id,
            'property_status':property_status.id,
            'price':prope.price,
            'land_m':prope.land_m,
            'garden_m':prope.garden_m, 
            'terrace_m':prope.terrace_m,
            'basement_m':prope.basement_m,
            'roof_m':prope.roof_m,
            'rooms':prope.rooms, 
            'baths':prope.baths,
            'supplier':prope.supplier.id
            }
            #prop_dict = dict_from_class(prope)
            _logger.warn(p)
            valid_props = self.env['pie.build.property'].create(p)
            valid_props = self.env['pie.grid.property'].create(p)

            
        action = self.env.ref('PIE_Build.action_prop_list_active').read()[0]
        return action