# -*- coding: utf-8 -*-

from odoo import api ,fields, models


class floors(models.Model):
    _name = "pie.setup.floor"

    name = fields.Char(string="Floors",size=150,required=True)
    floor_value= fields.Integer(string="Nth of the Floor",required=True)
    active = fields.Boolean('Active', default=True)



    @api.constrains('name')
    def _check_duplicate_code(self):
        names = self.search([])
        for c in names:
            if self.name.lower() == c.name.lower() and self.id != c.id:
                raise exceptions.ValidationError("Error: Name must be unique")