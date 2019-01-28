
from odoo import api ,fields, models
from odoo.exceptions import ValidationError
import re



class Branch(models.Model):
    _name="pie.entity.branch"
    name=fields.Char('Branch Name',required=True ,store=True)
    address=fields.Char('Address' ,store=True)
    Phone=fields.Char('Phone' ,store=True)
    #head_quater=fields.Boolean('Head Quater')
    entity_id=fields.Many2one('pie.entity',ondelete='cascade', index=True, copy=False ,store=True)
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict',required=True ,store=True) 
    city = fields.Many2one('res.country.state', 'City',required=True ,store=True)
    area = fields.Many2one('pie.setup.area',string=" Area",required=True ,store=True)
    @api.onchange('Phone')
    def validation_mobile(self):

        res={}
        

        if self.Phone:
                match = re.match('^(?:\+?44)?[07]\d{9,13}$', self.Phone)
        
                if match == None:
                     
                    res = {'warning': {
                                    'title': ('Warning'),
                                    'message': ('Invalid Phone')
                                }}
                    if res:
                        return res

class BrokerAdmin(models.Model):
   
    _inherit="res.users"
    broker_admin=fields.Many2one('pie.entity',ondelete='cascade', index=True, copy=False)
    supplier_admin=fields.Many2one('pie.entity', ondelete='cascade',index=True, copy=False)
    publisher=fields.Many2one('pie.entity', ondelete='cascade',index=True, copy=False)
    internal_broker_admin=fields.Many2one('pie.entity', ondelete='cascade',index=True, copy=False)
    is_group = fields.Boolean(compute="_check_user_group")  
    @api.one
    def _check_user_group(self):
        self.is_group = self.user.has_group('PIE_Setup.group_pie_supplier_manager')
    
    
    @api.depends('login')
    def change_email(self):
     for rec in self:
      rec.update({'email':rec.login})
    
    @api.onchange('login')
    def validation(self): 
        res={}
        
         
    
        if self.login:
                match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.login)
        
                if match == None:
                    self.login=''
                    res = {'warning': {
                                    'title': ('Warning'),
                                    'message': ('Invalid Email')
                                }}
                    if res:
                        return res
    
        users=self.env['res.users'].search([])
        for rec in users:
            if self.login==rec.login:
                res = {'warning': {
                                    'title': ('Warning'),
                                    'message': (' Email must be unique' )
                                }}
                if res:
                        return res


    @api.onchange('mobile')
    def validation_mobile(self): 

        res={}
        

        if self.mobile:
                match = re.match('^(?:\+?44)?[07]\d{9,13}$', self.mobile)
        
                if match == None:
                     
                    res = {'warning': {
                                    'title': ('Warning'),
                                    'message': ('Invalid Mobile')
                                }}
                    if res:
                        return res
    
    
    
    
   