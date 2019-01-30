 # -*- coding: utf-8 -*-

from odoo import api ,fields, models,exceptions
from odoo.exceptions import ValidationError,UserError
import re
import logging
_logger = logging.getLogger(__name__)
class Entity(models.Model):
    _name = "pie.entity"
     
    #_inherit='res.company'
    #active=fields.Boolean('Active', default=True)
    #parent_id_entity = fields.Many2one('pie.entity', string='Related Company', index=True)
    #---------------------------------------\
    name = fields.Char(index=True,required=True,size=60,store=True)
    street = fields.Char('street',size=150,required=True)
    street2 = fields.Char('street',size=150)
    code = fields.Integer('Code',Store=True)
    
 
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict') 
    city = fields.Many2one('res.country.state', 'City')
     
    
    
    email = fields.Char('email',size=60 ,store=True)
    phone = fields.Char('phone',size=15 ,store=True)
    fax = fields.Char('fax',size=50 ,store=True)
    mobile = fields.Char()
    image = fields.Binary("Image", attachment=True,
        help="This field holds the image used as avatar for this contact, limited to 1024x1024px",) 
    active=fields.Boolean('Active', default=True ,store=True)
    website = fields.Char(help="Website of Partner or Company" ,store=True)
    #-----------------------------------------
   
	 
    
    number_branches=fields.Integer('Number of branches',compute='_get_number_branches',store=True)
    Description=fields.Char(string="Description",size=150)
    #head_of_adddress=fields.Char(string="Head Of Address",size=150,required=True)
    contract_contant_name=fields.Char(string="Contract  Contant Name",size=150,required=True ,store=True)
    contract_contant_position=fields.Char(string="Contract contant Position",size=150 ,store=True)
    contract_contant_mobile=fields.Char(string="Contract Contant Mobile" ,store=True)
    contract_contant_mail=fields.Char(string="Contract Contant Mail",size=60 ,store=True)
    landline=fields.Char('landline',size=15 ,store=True)
	 
    #-------broker information-----#
    borker_type=fields.Selection([('Company','Company'),('Individual','Individual')] )
    broker_name=fields.Char(string="Broker Name",size=150 ,store=True )
    
    number_sales_agents=fields.Integer( default='1' ,store=True)
    sevice_list=fields.Many2many('pie.entity.service',store=True)
    
    pie_access_right=fields.Selection([('broker','Broker Company'),('supplier','Supplier Company'),('both','Both Supplier and Broker')],'Acces Right' ,store=True)
    pie_type=fields.Selection([('is_supplier','Supplier'),('is_broker','Broker')],string="Type",required=True,store=True)

    zip = fields.Char(string="Postal Code" , size=10)
    comments = fields.Text(string='Internal Notes')
    image = fields.Binary(string='Company Logo')
    state_id = fields.Many2one('res.country.state' , string="City")
    country_id=fields.Many2one('res.country',string="Country")
    offline=fields.Boolean(string="Offline Access", default=True)
    
    @api.one
    @api.depends('name')
    def _compute_offline_state(self):
        _logger.warn(self)
        for rec in self:
            is_users = self.env['res.users'].search([('entity','=',rec.id)])
            _logger.warn(is_users)
            if is_users:
                rec.offline_state = "Online with Users"
            else:
                rec.offline_state =  "Offline"

    
    offline_state = fields.Char(string='Offline',required=True,compute='_compute_offline_state',size=100)

    branches=fields.One2many('pie.entity.branch','entity_id')
    entity_broker_mail= fields.One2many('res.users','broker_admin',copy=True ,store=True)
    internal_broker=fields.Boolean('Internal Broker')
    internal_broker_admin=fields.One2many('res.users','internal_broker_admin',copy=True ,store=True)
    #------supplier inf----------
    supplier_type=fields.Selection([('Developer','Developer'),('Reseller','Reseller')] ,store=True)
    type_inventory=fields.Selection([('open_inventory','Open Inventory'),('Control_inventory','Controlled Inventory')] ,store=True)
    
    entity_supplier_mail= fields.One2many('res.users','supplier_admin',copy=True ,store=True)
    supplier_share=fields.Boolean('Show Supplier on Share',default=False ,store=True)
    publisher= fields.One2many('res.users','publisher',copy=True ,store=True)
   
    @api.multi
    def add_broker(self):
       
        view_id = self.env.ref('PIE_Brokers.pie_broker_admin_form_view').id
    	context = self._context.copy()
        
        return {
            'name':'Add Broker',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'pie_broker',
            'views': [(view_id, 'form')],
            'view_id': view_id,
            'target': 'new',
            'context': context,
        }
     
    @api.constrains('email')
    def validate_mail(self):

       if self.email:
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.com)$', self.email)
        if match == None:
            raise ValidationError('Not vaild mail')
    
    @api.constrains('contract_contant_mobile')
    def validate_contractnumber(self):
        userInput=0
        try:

            userInput = int(self.contract_contant_mobile) 
       
        except ValueError:

            raise ValidationError('Not a valid Contrat Mobile ')    
           
    @api.constrains('contract_contant_mail')
    def validate_contract_mail(self):
       if self.contract_contant_mail:
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.com)$', self.contract_contant_mail)
        if match == None:
            raise ValidationError('Not a valid Contract E-mail ID')
    
   
    
    @api.model
    def create(self, vals):

        partner = super(Entity, self).create(vals)
       
       
        return partner
    @api.one
    @api.depends('branches')
    def _get_number_branches(self):
        #self.number_branches=3
        branches_account=len(self.branches)
        self.number_branches=branches_account
        for rec in self:
            self.number_branches=branches_account
        #if branches_account>self.number_branches:
    @api.constrains('name')
    def _check_duplicate_code(self):
        names = self.search([])
        for c in names:
            if self.name:
                if self.name == c.name and self.id != c.id:
                    raise ValidationError("Error: Name must be unique")
        
		          
    @api.constrains('website')
    def _valdation_url(self):
        if self.website:
            match = re.match('^(?:(?:http(?:s)?|ftp)://)(?:\\S+(?::(?:\\S)*)?@)?(?:(?:[a-z0-9\u00a1-\uffff](?:-)*)*(?:[a-z0-9\u00a1-\uffff])+)(?:\\.(?:[a-z0-9\u00a1-\uffff](?:-)*)*(?:[a-z0-9\u00a1-\uffff])+)*(?:\\.(?:[a-z0-9\u00a1-\uffff]){2,})(?::(?:\\d){2,5})?(?:/(?:\\S)*)?$', self.website)
            if match == None:
                raise ValidationError('Not valid a website')
            
    @api.constrains('entity_broker_mail')
    def _check_broker(self):
        if self.internal_broker==False:
            group_id=self.env['ir.model.data'].search([('name','=','group_pie_broker_manager')])
            group_user_broker = self.env['res.groups'].search([('id','=',group_id.res_id)]) 
            users=self.env['res.users'].search([('broker_admin','!=',False)])
            group = group_user_broker.update({ 'users':users})
            users=self.env['res.users'].search([('broker_admin','=',self.id)])
            if len(users)>1:

                raise ValidationError('select only one Admin .....')


            """else:
                 template = self.env.ref('auth_signup.set_password_email', raise_if_not_found=False)
            
                 if not template:

                     template = self.env.ref('auth_signup.reset_password_email')
                 assert template._name == 'mail.template'

                 template_values = {
                              'email_to': self.entity_broker_mail.login,
                                'email_cc': False,
                                 'auto_delete': True,
                             'partner_to': False,
                              'scheduled_date': False,
                                     }
                 template.write(template_values)

                 for user in self:
                     if not user.entity_broker_mail.login:
                        raise UserError(_("Cannot send email: user %s has no email address.") % user.name)
                     with self.env.cr.savepoint():

                         template.with_context(lang="en_AU").send_mail(user.entity_broker_mail.id, force_send=True, raise_exception=True)
                     _logger.info("Password reset email sent for user <%s> to <%s>", user.entity_broker_mail.login, user.entity_broker_mail.login)"""
                    
        
    @api.constrains('internal_broker_admin')
    def _check_inliner_broker(self):
            group_id=self.env['ir.model.data'].search([('name','=','group_pie_broker_internal')])
            group_user_broker = self.env['res.groups'].search([('id','=',group_id.res_id)])
             
             
            users=self.env['res.users'].search([('internal_broker_admin','=',self.id)])
            group = group_user_broker.update({ 'users':users})
            users=self.env['res.users'].search([('internal_broker_admin','=',self.id)])
            if len(users)>1:
             raise ValidationError('select only one Admin .....')
            """else:
                 template = self.env.ref('auth_signup.set_password_email', raise_if_not_found=False)
            
                 if not template:

                     template = self.env.ref('auth_signup.reset_password_email')
                 assert template._name == 'mail.template'

                 template_values = {
                              'email_to': self.internal_broker_admin.login,
                                'email_cc': False,
                                 'auto_delete': True,
                             'partner_to': False,
                              'scheduled_date': False,
                                     }
                 template.write(template_values)

                 for user in self:
                     if not user.internal_broker_admin.login:
                        raise UserError(_("Cannot send email: user %s has no email address.") % user.name)
                     with self.env.cr.savepoint():

                         template.with_context(lang="en_AU").send_mail(user.internal_broker_admin.id, force_send=True, raise_exception=True)
                     _logger.info("Password reset email sent for user <%s> to <%s>", user.internal_broker_admin.login, user.internal_broker_admin.login)"""
    @api.constrains('entity_supplier_mail')
    def _check_supplier(self):
        group_id=self.env['ir.model.data'].search([('name','=','group_pie_supplier_manager')])
        group_user_supplier = self.env['res.groups'].search([('id','=',group_id.res_id)])
         
        """if self.entity_supplier_mail.id>0:
            
            for rec in group_user_supplier:
                if rec.users.id.id==self.entity_supplier_mail.id:
                    raise ValidationError('Admin is selected before......')
        group_user_supplier = self.env['res.groups'].search([('id','=',14)])    """    
        users_supplier=self.env['res.users'].search([('supplier_admin','!=',False)])
        group_supplier = group_user_supplier.update({'users':users_supplier})
        users=self.env['res.users'].search([('supplier_admin','=',self.id)])
        if len(users)>1:
            raise ValidationError('select only one Admin .....')
        """else:
                 template = self.env.ref('auth_signup.set_password_email', raise_if_not_found=False)
            
                 if not template:

                     template = self.env.ref('auth_signup.reset_password_email')
                 assert template._name == 'mail.template'

                 template_values = {
                              'email_to': self.entity_supplier_mail.login,
                                'email_cc': False,
                                 'auto_delete': True,
                             'partner_to': False,
                              'scheduled_date': False,
                                     }
                 template.write(template_values)

                 for user in self:
                     if not user.entity_supplier_mail.login:
                        raise UserError(_("Cannot send email: user %s has no email address.") % user.name)
                     with self.env.cr.savepoint():

                         template.with_context(lang="en_AU").send_mail(user.entity_supplier_mail.id, force_send=True, raise_exception=True)
                     _logger.info("Password reset email sent for user <%s> to <%s>", user.entity_supplier_mail.login, user.entity_supplier_mail.login)"""
    @api.constrains('publisher')
    def _check_publisher(self):
        group_id=self.env['ir.model.data'].search([('name','=','group_pie_supplier_publisher')])
        group_user_supplier = self.env['res.groups'].search([('id','=',group_id.res_id)])
            
        publisher=self.env['res.users'].search([('publisher','!=',False)])
        group_supplier = group_user_supplier.update({'users':publisher})
        template = self.env.ref('auth_signup.set_password_email', raise_if_not_found=False)
            
        """if not template:
            template = self.env.ref('auth_signup.reset_password_email')
        assert template._name == 'mail.template'

        template_values = {
            'email_to': self.publisher.login,
            'email_cc': False,
            'auto_delete': True,
            'partner_to': False,
            'scheduled_date': False,
        }
        template.write(template_values)

        for user in self:

             
            if not user.publisher.login:
                raise UserError(_("Cannot send email: user %s has no email address.") % user.name)
            with self.env.cr.savepoint():
                template.with_context(lang="en_AU").send_mail(user.publisher.id, force_send=True, raise_exception=True)
            _logger.info("Password reset email sent for user <%s> to <%s>", user.publisher.login, user.publisher.login)"""
            
        
        
 
				 



    @api.constrains('number_sales_agents')
    def _get_number_sales(self):
        if (self.number_sales_agents >999) or (self.number_sales_agents <= 0):
            raise ValidationError('You Cannot add Define Sales Agents Count more than 999 or less than 0.')

    
    @api.constrains('phone')
    def _get_valdition_phone(self):
        if self.phone:

                match = re.match('^(?:\+?44)?[09]\d{10,13}$', self.phone)
        
                if match == None:
                    raise ValidationError('Invalid Phone Number ')

                                 
    @api.constrains('active')
    def change_entity_state(self):
         
        if self.entity_supplier_mail.id>0:
         users=self.env['res.users'].search([('login','=',self.entity_supplier_mail.login)])
         users.write({'active':False})
        elif self.entity_broker_mail.id>0:
         users=self.env['res.users'].search([('login','=',self.entity_broker_mail.login)])
         users.write({'active':False})
            
        
         
            
        
    @api.onchange('entity_broker_mail')
    def onchange_entity_broker_mail(self):
        return {'domain':{'entity_broker_mail':[('id','=',-1)]}}
    @api.onchange('entity_supplier_mail')
    def onchange_sb_sector_id(self):
        return {'domain':{'entity_supplier_mail':[('id','=',-1)]}}
    
    @api.onchange('internal_broker_admin')
    def onchange_sb_internalbroker(self):
        return {'domain':{'internal_broker_admin':[('id','=',-1)]}}
    @api.onchange('publisher')
    def onchange_publisher(self):
        return {'domain':{'publisher':[('id','=',-1)]}}
    @api.constrains('internal_broker')
    def _remove_broker_admin(self):
     
     if self.internal_broker==True and self.entity_broker_mail.id>0:
      users=self.env['res.users'].search([('login','=',self.entity_broker_mail.login)])
      users.write({'active':False})
       
                                 
    @api.constrains('active')
    def change_entity_state(self):
      if self.active==False:
            users=self.env['res.users'].search([('entity','=',self.id)])
            for rec in users:
              rec.write({'active':False})
      if self.active==True:
        users=self.env['res.users'].search([('entity','=',self.id)])
        sql = " UPDATE res_users SET active = true  WHERE entity ="+ str(self.id)
        self.env.cr.execute(sql)
            
        
         
            
        
 