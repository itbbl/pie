# -*- coding: utf-8 -*-

from odoo import api ,fields, models


class rooms(models.Model):
    _name = "pie.setup.room"

    name = fields.Char(string="Rooms",size=150,required=True)
    rooms_count= fields.Integer(string="Count of Rooms",required=True)
    active = fields.Boolean('Active', default=True)

    _sql_constraints = [
        ('Rooms_unique', 'unique (name)',
         'This Rooms Count already exixts!')]
    @api.constrains('name')
    def _check_duplicate_code(self):
        names = self.search([])
        for c in names:
            if self.name.lower() == c.name.lower() and self.id != c.id:
                raise exceptions.ValidationError("Error: Name must be unique")