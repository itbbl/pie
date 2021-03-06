# -*- coding: utf-8 -*-

from odoo import api ,fields, models


class Area(models.Model):
    _name = "pie.setup.area"

    name = fields.Char(string="Area Name",size=150,required=True)
    region_id = fields.Many2one('pie.setup.region' , string='Parent Region',required=True)
    country_id=fields.Many2one(related='region_id.country_id',required=True)
    active = fields.Boolean('Active', default=True)


     

    @api.constrains('name')
    def _check_duplicate_code(self):
        names = self.search([])
        for c in names:
            if self.name.lower() == c.name.lower() and self.id != c.id:
                raise exceptions.ValidationError("Error: Name must be unique")