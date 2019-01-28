# -*- coding: utf-8 -*-

from odoo import api ,fields, models


class bathrooms(models.Model):
    _name = "pie.setup.bathrooms"

    name = fields.Char(string="Bathrooms",size=150,required=True)
    bathrooms_count= fields.Integer(string="Count of Bathrooms",required=True)
    active = fields.Boolean('Active', default=True)


    _sql_constraints = [
        ('bathrooms_unique', 'unique (name)',
         'This Bathrooms Count already exixts!')
    ]
    @api.constrains('name')
    def _check_duplicate_code(self):
        names = self.search([])
        for c in names:
            if self.name.lower() == c.name.lower() and self.id != c.id:
                raise exceptions.ValidationError("Error: Name must be unique")