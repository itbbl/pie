# -*- coding: utf-8 -*-

from odoo import api ,fields, models


class hashtag(models.Model):
    _name = "pie.setup.hashtag"

    name = fields.Char(string="Hashtags",size=150,required=True)
    active = fields.Boolean('Active', default=True)


    @api.constrains('name')
    def _check_duplicate_code(self):
        names = self.search([])
        for c in names:
            if self.name.lower() == c.name.lower() and self.id != c.id:
                raise exceptions.ValidationError("Error: Name must be unique")