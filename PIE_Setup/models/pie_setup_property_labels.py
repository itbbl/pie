from odoo import models,fields
class labels_property(models.Model):
    _name="pie.setup.property.labels"
    share_type=fields.Selection([('public','Public'),('private','Private'),('specific ','Specific ')],'Share type',default='public')
    share_with=fields.Many2many('res.users',string="Share With")
    label=fields.Many2many('pie.setup.label',string='labels')
   