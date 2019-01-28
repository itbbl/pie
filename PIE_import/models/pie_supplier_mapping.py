# -*- coding: utf-8 -*-

from odoo import api ,fields, models
import logging
_logger = logging.getLogger(__name__)

class Supplier_Mapping(models.Model):
    _name = "pie.supplier.mapping"
    _inherit = ['mail.thread']
    
    active = fields.Boolean('Active', default=True)
    developer = fields.Many2one('pie.entity',string="Developer",required=True, domain="['|',('acces_right', '=', 'supplier'),('acces_right', '=', 'both')]" )
    
    columns_mapping_ids=fields.One2many('pie.supplier.mapping.column','mapping_id')
    #other_columns_mapping_ids=fields.One2many(related='columns_mapping_ids',store=True, domain=[('selected', '=', False)])
    #columns_mapping_ids=fields.One2many('pie.supplier.mapping.column','mapping_id',default=lambda self: self._get_default_name())
    project_field = fields.Char(string="Project Field" )
    region_field = fields.Char(string="Region Field" )
    area_field = fields.Char(string="Area Field" )
    property_code_field = fields.Char(string="Property Code Field" )
    property_type_field = fields.Char(string="Property Type Field" )
    property_design_field = fields.Char(string="Property Design Field" )
    price_field = fields.Char(string="Price Field" )
    built_up_field = fields.Char(string="Built Up Space" )
    finishing_field = fields.Char(string="Finishing Field" )
    property_status_field = fields.Char(string="Property Status" )


    @api.model
    def create(self, values):
        record = super(Supplier_Mapping, self).create(values)
        _logger.warn(values)
        mapped_region = self.env['pie.supplier.mapping.column'].create({'supplier_column':values['region_field'],'pie_column2':'region','mapping_id':record.id,'required':True})
        #record['columns_mapping_ids'].append(mapped_region)
        return record

    @api.multi
    def write(self, values):
        
        record = super(Supplier_Mapping, self).write(values)
        _logger.warn(self)
        region_record = self.env['pie.supplier.mapping.column'].search([['mapping_id', '=', self.id], ['pie_column2', '=', 'region']])
        _logger.warn(region_record)
        for records in region_record:
            records.write({'supplier_column': values['region_field']})
        
        return record