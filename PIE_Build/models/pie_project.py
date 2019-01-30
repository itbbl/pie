# -*- coding: utf-8 -*-

from odoo import api ,fields, models,exceptions


class Project(models.Model):
    _name = "pie.project"
    
    active = fields.Boolean('Active', default=True)
    
    
    name = fields.Char(string="Project Name",size=150)
    project_code = fields.Char(string="Project Code",size=150)
    developer = fields.Many2one('pie.entity',string="Project Developer",domain="[('pie_type','=','is_supplier')]",required=True,default=lambda self: self.env.user.entity )
    country = fields.Many2one('res.country', string='Country',required=True)
    governorate = fields.Many2one('pie.setup.region',string='Governorate',required=True)
    area = fields.Many2one('pie.setup.area',string="Area",required=True)
    district = fields.Many2one('pie.setup.district',string="District")
    zone = fields.Char(string="Zone",size=100)
    description = fields.Text(string="Project Description",size=600)
    


    name = fields.Char(string='Name')
    
    developer_id = fields.Integer(string="Dev ID")
    @api.depends('developer')
    def _dev_id(self):
        self.developer_id = self.developer.id
        
    @api.constrains('name')
    def _check_duplicate_code(self):
        names = self.search([])
        for c in names:
            if self.name.lower() == c.name.lower() and self.id != c.id:
                raise exceptions.ValidationError("Error:Project Name must be unique ")