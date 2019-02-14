# -*- coding: utf-8 -*-
from odoo import api ,fields, models,exceptions
import logging
from odoo.exceptions import ValidationError
_logger = logging.getLogger(__name__)

class PPlan(models.Model):
    _inherit='pie.setup.payment_plan'
    project_ids = fields.Many2one('pie.project')
    
class Project(models.Model):
    _inherit='pie.project'
    payment_plan = fields.Many2many('pie.setup.payment_plan')
    
    @api.constrains('payment_plan')
    @api.depends('payment_plan')
    def calc_payment_plan(self):
      _logger.warn("We are in project")
      grid_props = self.env['pie.grid.property'].search([('project','=',self.id)])
      for prop in grid_props:
        prop.payment_plans_for_prop = [(5,0,0)]
        for payment_plan in self.payment_plan:
          vals = {'payment_plan':payment_plan.id,'price':prop.price,'property_id':prop.id}
          prop.payment_plans_for_prop = [(0,0,vals)]
          
      
class Build_Property(models.Model):
    _inherit='pie.grid.property'
    payment_plan = fields.Many2many(related='project.payment_plan')
    payment_plans_for_prop = fields.One2many('pie.grid.payment_plan','property_id')
    finishing_price = fields.Float(size=50)
    price_per_meter = fields.Float(size=20, compute='calc_price_per_meter')
    finish_per_meter = fields.Float(size=20, compute='calc_finish_per_meter')
    
    @api.one
    @api.depends('built_up','finishing_price')
    def calc_finish_per_meter(self):
      self.finish_per_meter = self.finishing_price / self.built_up
    
    @api.one
    @api.depends('built_up','price')
    def calc_price_per_meter(self):
        self.price_per_meter = self.price / self.built_up


