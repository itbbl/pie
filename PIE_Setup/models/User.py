from odoo import fields,models,api,exceptions
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)
class pie_admin(models.Model):
    _inherit='res.users'
    #_inherits=['res.users']
    entity_id = fields.Integer(string='Company ID')
    Manage_Admins=fields.Boolean('Manage Admins' ,default=False)
    PIE_Admin =fields.Boolean('PIE Admin' ,default=False)
    is_broker_admin =fields.Boolean(string='Broker Admin' ,default=False)
    is_broker_agent =fields.Boolean(string='Broker Agent' ,default=False)
    is_supplier_admin =fields.Boolean(string='Supplier Admin' ,default=False)
    is_supplier_editor =fields.Boolean(string='Supplier Editor' ,default=False)
    entity = fields.Many2one('pie.entity',string="Company")
    entity_type = fields.Selection(related='entity.pie_type',string="entity_type")
    entity_access_right = fields.Selection(related='entity.pie_access_right',string="entity_access_right")
    
    @api.model
    def create(self, vals):
      user = super(pie_admin, self).create(vals)
      _logger.warn("Test")
      _logger.warn(user)
      _logger.warn(user.entity_type)
      return user

    @api.onchange('entity')
    def _entity_chng(self):
        self.entity_type= self.entity.pie_type
        self.entity_access_right = self.entity.pie_access_right
        


    @api.constrains('PIE_Admin')
    def PIE_Admin_listener(self):
        _logger.warn(self.PIE_Admin)
        _logger.warn("Log From PIE Admin")
        if self.PIE_Admin == True:
            #_logger.warn(user_id)
            Managers_group = self.env.ref('PIE_Setup.group_pie_admin_admin')
            Managers_group.write({'users': [(4, self.id)]})
        else:
            Managers_group = self.env.ref('PIE_Setup.group_pie_admin_admin')
            Managers_group.write({'users': [(3, self.id)]})

       

    @api.constrains('Manage_Admins')
    def Manage_Admin_listenr(self):
        _logger.warn("Log From PIE Manage")
        _logger.warn(self.Manage_Admins)
        if self.Manage_Admins == True:
                #_logger.warn(user_id)
            Managers_group = self.env.ref('PIE_Setup.group_pie_admin_manager')
            Managers_group.write({'users': [(4, self.id)]})
        else:
            Managers_group = self.env.ref('PIE_Setup.group_pie_admin_manager')
            Managers_group.write({'users': [(3, self.id)]})
         
       
    @api.constrains('is_broker_admin')
    def Broker_adminlistenr(self):
        _logger.warn("Log From PIE is_broker_admin")
        _logger.warn(self.is_broker_admin)
        if self.is_broker_admin == True:
            exist_admin = self.env['res.users'].search_count(['&',('entity.id','=',self.entity.id),('is_broker_admin','=','True'),('active','=','True'),('id','!=',self.id)])
            _logger.warn(exist_admin)
            if exist_admin >= 1 :
                raise exceptions.ValidationError("There is already active Admin for " + self.entity.name)
            #_logger.warn(user_id)
            Managers_group = self.env.ref('PIE_Setup.group_pie_broker_manager')
            Managers_group.write({'users': [(4, self.id)]})
        else:
            Managers_group = self.env.ref('PIE_Setup.group_pie_broker_manager')
            Managers_group.write({'users': [(3, self.id)]})

    @api.constrains('is_broker_agent')
    def Broker_Agent_listenr(self):
        _logger.warn("Log From PIE is_broker_agent")
        _logger.warn(self.is_broker_agent)
        if self.is_broker_agent == True:
            exist_agents = self.env['res.users'].search_count(['&',('entity.id','=',self.entity.id),('active','=','True')])
            agents_count = self.entity.number_sales_agents + 1
            _logger.warn(exist_agents)
            if exist_agents >= agents_count :
                raise exceptions.ValidationError("You Cannot Assign More Sales Agents to this company " + self.entity.name)
                #_logger.warn(user_id)
            Managers_group = self.env.ref('PIE_Setup.group_pie_broker_agent')
            Managers_group.write({'users': [(4, self.id)]})
        else:
            Managers_group = self.env.ref('PIE_Setup.group_pie_broker_agent')
            Managers_group.write({'users': [(3, self.id)]})


    @api.constrains('is_supplier_admin')
    def Supplier_Admin_listenr(self):
        _logger.warn("Log From PIE is_broker_admin")
        _logger.warn(self.is_broker_admin)
        if self.is_supplier_admin == True:
            exist_admin = self.env['res.users'].search_count(['&',('entity.id','=',self.entity.id),('is_supplier_admin','=','True'),('active','=','True'),('id','!=',self.id)])
            _logger.warn(exist_admin)
            if exist_admin >= 1 :
                raise exceptions.ValidationError("There is already active Admin for " + self.entity.name)
            #_logger.warn(user_id)
            Managers_group = self.env.ref('PIE_Setup.group_pie_supplier_manager')
            Managers_group.write({'users': [(4, self.id)]})
        else:
            Managers_group = self.env.ref('PIE_Setup.group_pie_supplier_manager')
            Managers_group.write({'users': [(3, self.id)]})

    @api.constrains('is_supplier_editor')
    def Supplier_Editor_listenr(self):
        _logger.warn("Log From PIE is_broker_agent")
        _logger.warn(self.is_broker_agent)
        if self.is_supplier_editor == True:
                #_logger.warn(user_id)
            Managers_group = self.env.ref('PIE_Setup.group_pie_supplier_editor')
            Managers_group.write({'users': [(4, self.id)]})
        else:
            Managers_group = self.env.ref('PIE_Setup.group_pie_supplier_editor')
            Managers_group.write({'users': [(3, self.id)]})