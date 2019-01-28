# -*- coding: utf-8 -*-

from odoo import api ,fields, models


class label(models.Model):
    _name = "pie.setup.label"

    name = fields.Char(string="Label",size=150,required=True)
    active = fields.Boolean('Active', default=True)
    logo = fields.Binary("Image", attachment=True,
        help="This field holds the image used as avatar for this contact, limited to 1024x1024px",)
    
    state=fields.Selection([('public','Public'),('private','Private')],default="public",string="State")

    @api.constrains('name')
    def _check_duplicate_code(self):
        names = self.search([])
        for c in names:
            if self.name.lower() == c.name.lower() and self.id != c.id:
                raise exceptions.ValidationError("Error: Name must be unique")