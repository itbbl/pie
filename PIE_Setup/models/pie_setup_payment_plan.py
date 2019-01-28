# -*- coding: utf-8 -*-

from odoo import api ,fields, models


class Payment(models.Model):
    _name = "pie.setup.payment_plan"

    name = fields.Char(string="Plan Name",size=100,required=True)
    code = fields.Char(string="Plan Code",size=50,required=True)
    active = fields.Boolean('Active', default=True)
    is_percentage = fields.Boolean('Is Deposit a Percentage?',required=False)
    frst_deposit = fields.Float(string="1st Deposit Amount",required=True,default=0)
    scnd_deposit = fields.Float(string="2nd Deposit Amount",default=0)
    thrd_deposit = fields.Float(string="3rd Deposit Amount",default=0)
    forth_deposit = fields.Float(string="4th Deposit Amount",default=0)
    installments_count = fields.Integer(string="Installments Months",default=0) 
    no_of_years = fields.Integer(string="Years")

    
    @api.constrains('code')
    def _check_duplicate_codeeee(self):

        if self.code.isspace():
          raise exceptions.ValidationError("Error: Code Cannot Have Spaces.")
        names = self.search([])
        for c in names:
            if self.code.lower() == c.code.lower() and self.id != c.id:
                raise exceptions.ValidationError("Error: Code must be unique")
    @api.constrains('name')
    def _check_duplicate_code(self):
        names = self.search([])
        for c in names:
            if self.name.lower() == c.name.lower() and self.id != c.id:
                raise exceptions.ValidationError("Error: Name must be unique")

    @api.constrains('frst_deposit','scnd_deposit','thrd_deposit','forth_deposit')
    def _check_positive_deposit(self):
        for record in self:
            if record.frst_deposit < 0 or record.scnd_deposit < 0 or record.thrd_deposit < 0 or record.forth_deposit < 0:
                raise exceptions.ValidationError("Error : The deposit cannot be negative ")

    @api.constrains('no_of_years')
    def _check_positive_installments_count(self):
        for record in self:
            if record.no_of_years < 0:
                raise exceptions.ValidationError("The No of years cannot be negative : %s" % record.no_of_years)