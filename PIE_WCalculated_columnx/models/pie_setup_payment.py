# -*- coding: utf-8 -*-
from odoo import api ,fields, models,exceptions
import logging
from odoo.exceptions import ValidationError
_logger = logging.getLogger(__name__)


class Build_Property(models.Model):
    _name="pie.grid.payment_plan"
    prop_id = fields.Many2one('pie.grid.property')
    payment_plan = fields.Many2one('pie.setup.payment_plan',string="Payment Plan",size=150)
    name=fields.Char(related='payment_plan.name')
    property_id = fields.Many2one('pie.grid.property')
    price = fields.Float(string="Unit Price")
    years = fields.Integer(related='payment_plan.no_of_years')
    is_percentage = fields.Boolean(related='payment_plan.is_percentage')
    frst_deposit = fields.Float(related='payment_plan.frst_deposit')
    scnd_deposit = fields.Float(related='payment_plan.scnd_deposit')
    thrd_deposit = fields.Float(related='payment_plan.thrd_deposit')
    forth_deposit = fields.Float(related='payment_plan.forth_deposit')
    installments_count = fields.Integer(string="Installments Count",related='payment_plan.installments_count')
    total_deposite = fields.Float(string="Total Deposite", compute='calc_installment_amount')
    installment_amount = fields.Float(string="Installments Amount", compute='calc_installment_amount')
    bua = fields.Float(related='property_id.built_up')
    price = fields.Float(related='property_id.price')

    @api.one
    @api.depends('price','payment_plan')
    def calc_installment_amount(self):
      deposite_count = 0
      if self.is_percentage:
        due_months_count = 0
        due_months_amount = 0
        remaining_amount = 0
        d1 = (self.frst_deposit/100) * self.price
        d2 = (self.scnd_deposit/100) * self.price
        d3 = (self.thrd_deposit/100) * self.price
        d4 = (self.forth_deposit/100) * self.price
        self.total_deposite = d1 + d2 + d3 + d4
        remaining_amount = self.price - self.total_deposite
        if d1 != 0 and d2!= 0  and d3!= 0  and d4!= 0 :
          due_months_count = (self.years * 12) - 4
          due_months_amount = remaining_amount / due_months_count
        elif d1 != 0 and d2!= 0  and d3!= 0:
          due_months_amount = remaining_amount / due_months_count
        elif d1 != 0 and d2!= 0 :
          due_months_count = (self.years * 12) - 2
          due_months_amount = remaining_amount / due_months_count
        elif d1 != 0:
          due_months_count = (self.years * 12) - 1
          due_months_amount = remaining_amount / due_months_count
        self.installments_count = due_months_count
        self.installment_amount = due_months_amount
        
      else:
        self.total_deposite = self.frst_deposit + self.scnd_deposit +self.thrd_deposit +self.forth_deposit
        _logger.warn("total_deposite dfffff")
        _logger.warn(self.total_deposite)
        due_months_count = 0
        due_months_amount = 0
        remaining_amount = 0
        remaining_amount = self.price - self.total_deposite
        d1 = self.frst_deposit
        d2 = self.scnd_deposit
        d3 =self.thrd_deposit
        d4 = self.forth_deposit
        if d1 != 0 and d2 != 0  and d3 != 0  and d4 != 0 :
          due_months_count = (self.years * 12) - 4
          due_months_amount = remaining_amount / due_months_count
        elif d1 != 0 and d2!= 0  and d3!= 0:
          due_months_count = (self.years * 12) - 3
          due_months_amount = remaining_amount / due_months_count
        elif d1 != 0 and d2!= 0 :
          due_months_count = (self.years * 12) - 2
          due_months_amount = remaining_amount / due_months_count
        elif d1 != 0:
          due_months_count = (self.years * 12) - 1
          due_months_amount = remaining_amount / due_months_count
        self.installments_count = due_months_count
        self.installment_amount = due_months_amount

    
    @api.one
    @api.depends('payment_plan','price')
    def calc_data(self):
        deposite_count = 0
        if self.is_percentage:
            due_months_count = 0
            due_months_amount = 0
            remaining_amount = 0
            d1 = (self.frst_deposit/100) * self.price
            d2 = (self.scnd_deposit/100) * self.price
            d3 = (self.thrd_deposit/100) * self.price
            d4 = (self.forth_deposit/100) * self.price
            self.total_deposite = (d1 + d2 +d3 + d4)
            remaining_amount = self.price - self.total_deposite
            

            if d1 != 0 and d2!= 0  and d3!= 0  and d4!= 0 :
                due_months_count = (self.years * 12) - 4
                due_months_amount = remaining_amount / due_months_count

            elif d1 != 0 and d2!= 0  and d3!= 0:
                due_months_count = (self.years * 12) - 3
                due_months_amount = remaining_amount / due_months_count

            elif d1 != 0 and d2!= 0 :
                due_months_count = (self.years * 12) - 2
                due_months_amount = remaining_amount / due_months_count

            elif d1 != 0:
                due_months_count = (self.years * 12) - 1
                due_months_amount = remaining_amount / due_months_count
            
            
            
        else:
            self.total_deposite = self.frst_deposit + self.scnd_deposit +self.thrd_deposit +self.forth_deposit
            due_months_count = 0
            due_months_amount = 0
            remaining_amount = 0
            remaining_amount = self.price - self.total_deposite
            d1 = self.frst_deposit
            d2 = self.scnd_deposit
            d3 =self.thrd_deposit
            d4 = self.forth_deposit
            _logger.warn("total_deposite dfffff")
            _logger.warn(self.total_deposite)

            if d1 != 0 and d2 != 0  and d3 != 0  and d4 != 0 :
                due_months_count = (self.years * 12) - 4
                due_months_amount = remaining_amount / due_months_count

            elif d1 != 0 and d2!= 0  and d3!= 0:
                due_months_count = (self.years * 12) - 3
                due_months_amount = remaining_amount / due_months_count

            elif d1 != 0 and d2!= 0 :
                due_months_count = (self.years * 12) - 2
                due_months_amount = remaining_amount / due_months_count

            elif d1 != 0:
                due_months_count = (self.years * 12) - 1
                due_months_amount = remaining_amount / due_months_count
                