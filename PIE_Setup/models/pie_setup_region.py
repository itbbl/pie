# -*- coding: utf-8 -*-

from odoo import api ,fields, models , exceptions




class Region(models.Model):
    _name = "pie.setup.region"

    name = fields.Char(string="Region Name",size=150,required=True)
    active = fields.Boolean('Active', default=True)
    country_id= fields.Many2one('res.country',string='Country',required=True)


    _sql_constraints = [
        ('region_unique', 'unique (name)',
         'This Region already exixts!')]

    @api.constrains('name')
    def _check_duplicate_code(self):
        names = self.search([])
        for c in names:
            if self.name.lower() == c.name.lower() and self.id != c.id:
                raise exceptions.ValidationError("Error: Name must be unique")