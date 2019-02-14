# -*- coding: utf-8 -*-

from odoo import api ,fields, models


class label(models.Model):
    _name = "pie.setup.label"

    name = fields.Char(string="Label",size=150,required=True)
    active = fields.Boolean('Active', default=True)
    broker = fields.Many2one('pie.entity',string="Broker",store=True,domain="[('pie_type','=','is_broker')]",default=lambda self: self.env.user.entity)
    
    @api.constrains('name')
    def _check_duplicate_code(self):
        names = self.search([])
        for c in names:
            if self.name.lower() == c.name.lower() and self.id != c.id and c.broker==self.broker:
                raise ValidationError("Error: Name must be unique")