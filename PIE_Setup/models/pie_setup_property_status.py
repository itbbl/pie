# -*- coding: utf-8 -*-

from odoo import api ,fields, models,_

from odoo.exceptions import ValidationError
class property_status(models.Model):
    _name = "pie.setup.property_status"
     
    name = fields.Char(string="Property Status",size=150,required=True)
    active = fields.Boolean('Active', default=True)
     
    _sql_constraints = [
        ('proprety_status_unique', 'unique (name)',
         'This Property Status already exixts!')]
    @api.constrains('name')
    def _check_duplicate_code(self):
        names = self.search([])
        for c in names:
            if self.name.lower() == c.name.lower() and self.id != c.id:
                raise exceptions.ValidationError("Error: Name must be unique")