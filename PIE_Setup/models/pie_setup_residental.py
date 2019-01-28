# -*- coding: utf-8 -*-

from odoo import api ,fields, models


class residental(models.Model):
    _name = "pie.setup.residental"

    name = fields.Char(string="Residental Type",size=150,required=True)
    active = fields.Boolean('Active', default=True)

    _sql_constraints = [
        ('residintal_Type_unique', 'unique (name)',
         'This Type already exixts!')]
    @api.constrains('name')
    def _check_duplicate_code(self):
        names = self.search([])
        for c in names:
            if self.name.lower() == c.name.lower() and self.id != c.id:
                raise exceptions.ValidationError("Error: Name must be unique")