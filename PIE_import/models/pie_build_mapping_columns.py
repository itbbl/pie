# -*- coding: utf-8 -*-

from odoo import api ,fields, models,exceptions
import logging
import operator
_logger = logging.getLogger(__name__)

class Supplier_Mapping_columns(models.Model):
    _name = "pie.build.mapping.column"

    
    active = fields.Boolean('Active', default=True ,store=True )
    selected = fields.Boolean('Selected', default=False ,store=True)
    required = fields.Boolean('Required', default=False,store=True )
    supplier_column = fields.Char(string='Column Name',size=100,store=True )
    mapping_id=fields.Many2one('pie.build.mapping',store=True)
    supplier_id=fields.Many2one(related='mapping_id.developer',store=True)
    pie_column2 = fields.Selection(selection='prop_to_exp', string="Pie Column" ,store=True)


    
    def prop_to_exp(self):
        fields = self.env['pie.build.draft'].fields_get()
        sorted_x = sorted(fields.items(), key=operator.itemgetter(1))
        res=[]
        blacklisted = ['create_date','write_uid','id','supplier_id','current_user','create_uid','is_secondary','write_date','active','is_primary','__last_update','has_errors','import_id','sharing_level','name','supplier']
        
        for k, v in sorted_x:
            if not k in blacklisted:
                res.append((k, v['string']))
            
        _logger.warn(res)
        #sorted_x = sorted(res.items(), key=operator.itemgetter(1))

        return res

    @api.constrains('supplier_column')
    def _check_duplicate_code(self):
        #_logger.warn(self.mapping_id.id)
        names = self.env['pie.build.mapping.column'].search([['mapping_id','=',self.mapping_id.id]])
        #_logger.warn(names)
        for c in names:
            if self.supplier_column:
                if self.supplier_column.lower() == c.supplier_column.lower() and self.id != c.id:
                    raise exceptions.ValidationError("Error: Column Name must be unique")

    