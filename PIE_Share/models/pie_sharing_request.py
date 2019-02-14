# -*- coding: utf-8 -*-

from odoo import api ,fields, models,exceptions
from datetime import date,datetime,timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
import datetime as dt
import logging

_logger = logging.getLogger(__name__)
class sharing_request(models.Model):
    _name = "pie.share.sharing_request"
    #_inherit = ['mail.thread', 'ir.needaction_mixin']
    name=fields.Char('Contact Person',size=150 )
    active = fields.Boolean('Active', default=True)
    developer = fields.Many2one('pie.entity',string="Supplier",store=True  ,domain="['&',('pie_type','=','is_supplier'),('type_inventory','=','Control_inventory')]", required=True)
    broker = fields.Many2one('pie.entity',string="Broker",store=True,domain="[('pie_type','=','is_broker')]",default=lambda self: self.env.user.entity)
    #developer_open = fields.Many2one('pie.entity',string="Supplier",
    contract_sign_start_date = fields.Date(string="Contract Start Date")
    contract_sign_end_date = fields.Date(string="Contract End Date")
    status = fields.Selection([('Expired', 'Expired'), ('Pending', 'Pending'),('Disable','Disable'),('Enable','Enable'),('Renewal','Renewal'),('Rejected','Rejected'),('Activated','Activated'),('Approved','Approved')]
    ,default='Pending')
    is_pending=fields.Boolean('is_pending',default=True)
    no_contract=fields.Boolean('No Contract',default=False)
    broker_id=fields.Integer(related='developer.id')
    supplier_id=fields.Integer(related='developer.id')
    head_office=fields.Char(related='developer.city.name',string="Head Of Office") 
    #broker_id=fields.related('developer', 'sharesrequest__ids', type='many2one', string='Currency', relation="res.entity")
    """@api.constrains('no_contract')
    def remove_date_(self):
     for rec in self:
      if rec.no_contract==True:
       rec.update({
       'contract_sign_start_date':null,
       'contract_sign_end_date':null

       
       })
    """

    @api.one
    @api.depends('developer')
    def _compute_o2m_field(self):
        _logger.warn(self.env.user)
        
        user = self.env['res.users'].browse(self.env.uid)
        _logger.warn(user.entity)
        result=[]
        res = self.env['pie.entity'].sudo().search([])
        for en in res:
          result.append(en.id)
        
        _logger.warn("Hiiiiiiiii")
        _logger.warn(res)
        #self.sups_list = [(6,0,res)]
        #self.sups_list = res
        _logger.warn(result)
        _logger.warn("You are user")
        
    
    @api.multi
    @api.constrains('contract_sign_end_date', 'contract_sign_start_date','no_contract')
    def date_constrains(self):

        if not self.contract_sign_start_date and self.contract_sign_end_date and self.no_contract==False:
            raise ValidationError('Sorry, Enter Start Date...')
        elif not self.contract_sign_end_date and self.contract_sign_start_date and self.no_contract==False:
            raise ValidationError('Sorry, Enter End Date...')
        elif self.contract_sign_start_date==self.contract_sign_end_date and self.no_contract==False and  self.contract_sign_start_date  :
          raise ValidationError('Contract Period is greater than Zero  ')
        #if self.contract_sign_start_date< dt.datetime.strftime(dt.datetime.today(),'%Y-%m-%d') and  self.contract_sign_start_date:
            #raise exceptions.ValidationError('Sorry, Start Date Must be greater Than Date today...')
        if not self.contract_sign_start_date and self.no_contract==False:
            raise exceptions.ValidationError('Sorry, Cannot send request empty...')

        for rec in self:
            if rec.contract_sign_end_date < rec.contract_sign_start_date:
                raise exceptions.ValidationError('Sorry, End Date Must be greater Than Start Date...')

    def action_reject(self):
        self.update({
        'status':'Rejected',
        })
        self.broker.sudo().active_suppliers = [(2,self.developer.id)]
        self.developer.sudo().active_brokers = [(2,self.broker.id)]
        self.env.cr.commit()
    
    def action_confirm(self):
        if not self.contract_sign_start_date or not self.contract_sign_end_date:
            raise ValidationError('Sorry Please select start and end date.....')
         
        self.update({
        'status':'Approved',
         
        })
        
            
 
    def  action_approve(self):
        
        self.update({
        'status':'Renewal',
         
        })
        
    def action_enable(self):
        self.update({
        'status':'Activated',
        })
        self.env['pie.grid.property'].clear_caches()
        #self.broker.sudo().suppliers_list = (0,False,self.developer.id)
        self.broker.sudo().active_suppliers = [(4,self.developer.id)]
        self.developer.sudo().active_brokers = [(4,self.broker.id)]
        self.env.cr.commit()
    @api.multi
    def unlink(self):
        self.broker.sudo().active_suppliers = [(2,self.developer.id)]
        self.developer.sudo().active_brokers = [(2,self.broker.id)]
        self.env.cr.commit()
        
        return models.Model.unlink(self)
    def action_disable(self):
        self.update({
        'status':'Disable',
        })
        self.env['pie.grid.property'].clear_caches()
        self.broker.sudo().active_suppliers = [(2,self.developer.id)]
        #self.broker.active_suppliers = 
        self.developer.sudo().active_brokers = [(2,self.broker.id)]
        self.env.cr.commit()
     
    def change_statue_activated(self):
        sharing_requests_ids = self.env['pie.share.sharing_request'].search([])
        self.action_disable()
         
        for rec in self:
            rec.xx=1
        try:
             _logger.info('Successfu;;')
        except:
             _logger.info('Failedhh')         
    @api.constrains('developer')
    def _duplicate_name(self):
        broker_admin=self.env['res.users'].search([('id','=',self.env.uid)])
        self.broker_id = broker_admin.entity_id
        self.supplier_id=self.developer.id
        #_logger.warn(self.broker)
        #_logger.warn(self.developer)
        dev = self.env['pie.entity'].browse(self.developer.id)
        _logger.warn(dev)
        developers_ids = []
        brokers_ids = []

        developers_ids.append(self.developer.id)
        brokers_ids.append(self.broker.id)
        #dev.active_suppliers = [(6,0,[self.broker])]
        #dev.write({'active_suppliers': [(1,False,self.broker.id)]})
        #_logger.warn(ids)
        #_logger.warn(dev.active_suppliers)
        #dev.active_suppliers.append(self.broker.id)
        
        #dev.active_suppliers = 
        
        
        request_user=self.env['pie.share.sharing_request'].search(['&',('broker','=',self.broker.id),('developer','=',self.developer.id)])
        new_period='' 
        if  self.contract_sign_start_date and self.contract_sign_end_date:
            new_period=datetime.strptime(self.contract_sign_end_date, '%Y-%m-%d')-datetime.strptime(self.contract_sign_start_date, '%Y-%m-%d')
        checked=False    
        for rec in request_user:
            if (rec.id!=self.id) and (rec.developer == self.developer) and (rec.broker == self.broker):
                if  rec.contract_sign_start_date and rec.contract_sign_end_date :
                    old_period=datetime.strptime(rec.contract_sign_end_date, '%Y-%m-%d')-datetime.strptime(rec.contract_sign_start_date, '%Y-%m-%d')
                    if old_period==new_period :
                        raise ValidationError('Error:supplier submitted before in the same Contract Date. ')
                    
                     

                if not rec.status=='Rejected' and not rec.status=='Expired' and(not rec.status=='Activated') :
                  raise ValidationError('Error :supplier  sent new request before ....')
                if rec.status=='Activated':
                    end_date=datetime.strftime(dt.datetime.today(),'%Y-%m-%d')
                   
                    _logger.info(end_date)
                    _logger.info(type(end_date))
                    _logger.info('end_date')
                    _logger.info(rec.contract_sign_end_date)
                    
                    dif=dt.datetime.strptime(rec.contract_sign_end_date, '%Y-%m-%d')-dt.datetime.strptime(end_date, '%Y-%m-%d')
                    _logger.info(dif)
                     
                    if dif.days<=31 :
                        start_date=datetime.strptime(rec.contract_sign_end_date, '%Y-%m-%d')+dt.timedelta(days=1)
                        end_date=datetime.strptime(rec.contract_sign_end_date, '%Y-%m-%d')+dt.timedelta(days=365)
                        self.update({
                          
                         'status':'Renewal',
                         'contract_sign_start_date':start_date,
                         'contract_sign_end_date':end_date
                          
                          
                         })
                        
                    else:
                        raise ValidationError('sorry:request still active')
                        
     

class inherited_entity(models.Model):
  _inherit='pie.entity'
  broker_shared_request=fields.One2many('pie.share.sharing_request','supplier_id',store=True)
  active_suppliers=fields.Many2many(comodel_name='pie.entity',relation='supplier_entity_rel',column1='id',column2='broker_id',store=True,auto_join= True)
  active_brokers=fields.Many2many(comodel_name='pie.entity',relation='broker_entity_rel',column1='id',column2='supplier_id',store=True,auto_join= True)
  #suppliers_list = fields.One2many(comodel_name='pie.entity',store=True,auto_join= True)