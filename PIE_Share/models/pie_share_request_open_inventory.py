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
    broker = fields.Many2one('pie.entity',string="Broker",store=True,domain="[('pie_type','=','is_broker')]",default=lambda self: self.env.user.entity)
    developer = fields.Many2one('pie.entity',string="Supplier",store=True  ,domain="['&',('pie_type','=','is_supplier'),('type_inventory','=','open_inventory')]", required=True)

     
     
  
  
    
    def action_enable_broker(self):
      self.update({
        'status':'Enable',
        })
         
      self.broker.sudo().active_suppliers_open = [(2,self.developer.id)]
      self.developer.sudo().active_brokers_open = [(2,self.broker.id)]
      self.env.cr.commit() 
      self.env['ir.cron'].clear_caches()
         
    def action_disable(self):
        self.update({
                'status':'Disable', })

        
        
        self.broker.sudo().active_suppliers_open = [(4,self.developer.id)]
        self.developer.sudo().active_brokers_open = [(4,self.broker.id)]
        self.env.cr.commit() 
        self.env['ir.cron'].clear_caches()
        

    
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
                 
     

    @api.multi
    def unlink(self):
       
        self.broker.sudo().active_suppliers_open = [(2,self.developer.id)]
        self.developer.sudo().active_brokers_open = [(2,self.broker.id)]
         
        self.env.cr.commit()
        return models.Model.unlink(self)

class inherited_entity(models.Model):
  _inherit='pie.entity'
  active_suppliers_open=fields.Many2many(comodel_name='pie.entity',relation='supplier_entity_rel_open',column1='id',column2='broker_id',store=True,auto_join= True)
  active_brokers_open=fields.Many2many(comodel_name='pie.entity',relation='broker_entity_rel_open',column1='id',column2='supplier_id',store=True,auto_join= True)
  #suppliers_list = fields.One2many(comodel_name='pie.entity',store=True,auto_join= True)


 