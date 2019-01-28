from odoo import api ,fields, models,_
from odoo.exceptions import ValidationError
import re



class service(models.Model):

    _name='pie.entity.service'
    name=fields.Char('name',store=True)