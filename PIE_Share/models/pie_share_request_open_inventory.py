from odoo import api ,fields, models,exceptions

from datetime import date,datetime,timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
import logging
from datetime import datetime as dt
class open_inventory(models.Model):
    _name='pie.share.open.inventory'
    
    active = fields.Boolean('Active', default=True)
    developer = fields.Many2one('pie.entity',string="Supplier",store=True,domain="['&',('type','=','is_supplier'),('type_inventory','=','open_inventory')]")
    status = fields.Selection([('Disable','Disable'),('Enable','Enable')]
    ,default='Enable')
    broker_id=fields.Integer(related='developer.id')
    name=fields.Char('Contact Person',size=150 )
    open_inventory=fields.Boolean('Open Inventory',default=False)
    
     
     
  
  
    
    def action_enable_broker(self):
     self.update({
        'status':'Enable',
         
        

        })

    def action_disable(self):
     self.update({
        'status':'Disable',
         
        

        })

    
    @api.constrains('developer')
    def _duplicate_name(self):
        broker_admin=self.env['res.users'].search([('id','=',self.env.uid)])
        self.broker_id=broker_admin.entity_id
        request_user=self.env['pie.share.sharing_request'].search([('create_uid','=',self.env.uid)])
        new_period='' 
        
        checked=False    
        for rec in request_user:
            if rec.developer==self.developer and rec.id!=self.id :
				raise ValidationError('Error :supplier  sent new request before ....')
                 
     


 