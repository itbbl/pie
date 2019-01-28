# -*- coding: utf-8 -*-

from odoo import api ,fields, models,exceptions
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import ValidationError

class Supplier_Mapping(models.Model):
    _name = "pie.build.mapping"
    #name=fields.Char(related=developer.name)
    
    active = fields.Boolean('Active', default=True,store=True)
    developer = fields.Many2one('pie.entity',string="Developer",required=True, domain="[('pie_type', '=', 'is_supplier')]" ,store=True,default=lambda self: self.env.user.entity)
    
    columns_mapping_ids=fields.One2many('pie.build.mapping.column','mapping_id',store=True)
    other_columns_mapping_ids=fields.One2many('pie.build.mapping.column','mapping_id', domain=[('selected','=',False)],store=True)
    #other_columns_mapping_ids=fields.One2many(related='columns_mapping_ids',store=True, domain=[('selected', '=', False)])
    #columns_mapping_ids=fields.One2many('pie.supplier.mapping.column','mapping_id',default=lambda self: self._get_default_name())
    project_field = fields.Char(string="Project" ,store=True,default="Project")
    #region_field = fields.Char(string="Region Field",store=True )
    #area_field = fields.Char(string="Area Field" ,store=True)
    developer_column= fields.Char(string="Developer" ,store=True)
    property_code_field = fields.Char(string="Property Code" ,store=True,default="Property Code")
    property_type_field = fields.Char(string="Property Type" ,store=True,default="Type")
    property_design_field = fields.Char(string="Property Design",store=True ,default="Design")
    price_field = fields.Char(string="Price" ,store=True,default="Price")
    built_up_field = fields.Char(string="Built Up Space",store=True,default="BUA")
    finishing_field = fields.Char(string="Finishing",store=True,default="finishing" )
    property_status_field = fields.Char(string="Property Status" ,store=True,default="Status")
    developer_id = fields.Integer(related='developer.id')


    @api.model
    def create(self, values):

        #_logger.warn(values)
        old_mapping_exist = self.env['pie.build.mapping'].search_count([['developer', '=', values['developer']]])
        
        if old_mapping_exist >= 1:
            raise exceptions.ValidationError("This Supplier Has already a defined File Mapping")
            return
        record = super(Supplier_Mapping, self).create(values)
        #_logger.warn(record.developer)
        #_logger.warn(record.developer.id)
        
        


        #mapped_region = self.env['pie.build.mapping.column'].create({'supplier_column':values['region_field'],'pie_column2':'region','mapping_id':record.id,'selected':True})

        mapped_developer_column = self.env['pie.build.mapping.column'].create({'supplier_column':values['developer_column'],'pie_column2':'developer','mapping_id':record.id,'selected':True})

        mapped_price = self.env['pie.build.mapping.column'].create({'supplier_column':values['price_field'],'pie_column2':'price','mapping_id':record.id,'selected':True})

        mapped_project = self.env['pie.build.mapping.column'].create({'supplier_column':values['project_field'],'pie_column2':'project','mapping_id':record.id,'selected':True})

        mapped_built = self.env['pie.build.mapping.column'].create({'supplier_column':values['built_up_field'],'pie_column2':'built_up','mapping_id':record.id,'selected':True})

        mapped_prop_code = self.env['pie.build.mapping.column'].create({'supplier_column':values['property_code_field'],'pie_column2':'property_code','mapping_id':record.id,'selected':True})

        mapped_prop_type = self.env['pie.build.mapping.column'].create({'supplier_column':values['property_type_field'],'pie_column2':'property_type','mapping_id':record.id,'selected':True})

        mapped_prop_type = self.env['pie.build.mapping.column'].create({'supplier_column':values['property_design_field'],'pie_column2':'property_design','mapping_id':record.id,'selected':True})

        mapped_prop_type = self.env['pie.build.mapping.column'].create({'supplier_column':values['finishing_field'],'pie_column2':'finishing_type','mapping_id':record.id,'selected':True})

        mapped_prop_type = self.env['pie.build.mapping.column'].create({'supplier_column':values['property_status_field'],'pie_column2':'property_status','mapping_id':record.id,'selected':True})
        #record['columns_mapping_ids'].append(mapped_region)
        return record

    @api.multi
    def write(self, values):
        
        record = super(Supplier_Mapping, self).write(values)
        #_logger.warn(values)
        #_logger.warn(self)
        if 'developer_column' in values:
            area_record = self.env['pie.build.mapping.column'].search([['mapping_id', '=', self.id], ['pie_column2', '=', 'developer']])
            #_logger.warn(region_record)
            for records in area_record:
                records.write({'supplier_column': values['developer_column']})
         
        if 'region_field' in values:
            area_record = self.env['pie.build.mapping.column'].search([['mapping_id', '=', self.id], ['pie_column2', '=', 'region']])
            #_logger.warn(region_record)
            for records in area_record:
                records.write({'supplier_column': values['region_field']})

        if 'price_field' in values:
            area_record = self.env['pie.build.mapping.column'].search([['mapping_id', '=', self.id], ['pie_column2', '=', 'price']])
            #_logger.warn(region_record)
            for records in area_record:
                records.write({'supplier_column': values['price_field']})

        if 'project_field' in values:
            area_record = self.env['pie.build.mapping.column'].search([['mapping_id', '=', self.id], ['pie_column2', '=', 'project']])
            #_logger.warn(region_record)
            for records in area_record:
                records.write({'supplier_column': values['project_field']})

        if 'built_up_field' in values:
            area_record = self.env['pie.build.mapping.column'].search([['mapping_id', '=', self.id], ['pie_column2', '=', 'built_up']])
            #_logger.warn(region_record)
            for records in area_record:
                records.write({'supplier_column': values['built_up_field']})

        if 'property_code_field' in values:
            area_record = self.env['pie.build.mapping.column'].search([['mapping_id', '=', self.id], ['pie_column2', '=', 'property_code']])
            #_logger.warn(region_record)
            for records in area_record:
                records.write({'supplier_column': values['property_code_field']})


        if 'property_type_field' in values:
            area_record = self.env['pie.build.mapping.column'].search([['mapping_id', '=', self.id], ['pie_column2', '=', 'property_type']])
            #_logger.warn(region_record)
            for records in area_record:
                records.write({'supplier_column': values['property_type_field']})


        if 'property_design_field' in values:
            area_record = self.env['pie.build.mapping.column'].search([['mapping_id', '=', self.id], ['pie_column2', '=', 'property_design']])
            #_logger.warn(region_record)
            for records in area_record:
                records.write({'supplier_column': values['property_design_field']})

        if 'finishing_field' in values:
            area_record = self.env['pie.build.mapping.column'].search([['mapping_id', '=', self.id], ['pie_column2', '=', 'finishing_type']])
            #_logger.warn(region_record)
            for records in area_record:
                records.write({'supplier_column': values['finishing_field']})

        if 'property_status_field' in values:
            area_record = self.env['pie.build.mapping.column'].search([['mapping_id', '=', self.id], ['pie_column2', '=', 'property_status']])
            #_logger.warn(region_record)
            for records in area_record:
                records.write({'supplier_column': values['property_status_field']})

            
        return record