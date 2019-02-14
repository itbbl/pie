# -*- coding: utf-8 -*-

from odoo import api ,fields, models,exceptions
from datetime import datetime, timedelta
from datetime import datetime as dt
import logging
_logger = logging.getLogger(__name__)

class sharing_scheduler(models.Model):
    _name = "pie.share.scheduler"

    name = fields.Char(required=True)
    numberOfUpdates = fields.Integer('Number of updates', help='The number of times the scheduler has run and updated this field')
    lastModified = fields.Date('Last updated')

    #This function is called when the scheduler goes off
    def process_demo_scheduler_queue(self):
        sharing_requests_ids = self.env['pie.share.sharing_request'].search([])
        


        for sharing_request_id in sharing_requests_ids :
           
            #sharing_request =self.env['pie.share.sharing_request'].search([])
            #shareeee = self.env['pie.share.sharing_request'].browse([sharing_request_id])
            #shareeee.write({'contract_sign_end_date':datetime.now()})
            #shareeee.write({'contract_sign_end_date':datetime.now()})
            #sharing_request_end_date = sharing_request.contract_sign_end_date
            if sharing_request_id.contract_sign_end_date :
             if dt.strptime(sharing_request_id.contract_sign_end_date, '%Y-%m-%d')<= dt.today():
              _logger.info('Exipred')
              sharing_request_id.update({'status':'Expired'})
              sharing_request_id.broker.sudo().active_suppliers = [(2,sharing_request_id.developer.id)]
              sharing_request_id.developer.sudo().active_brokers = [(2,sharing_request_id.broker.id)]

            if sharing_request_id.contract_sign_start_date :
             _logger.info(dt.today()  )
             
             if dt.strptime(sharing_request_id.contract_sign_start_date, '%Y-%m-%d')<= dt.today() and sharing_request_id.status=='Approved':
              _logger.info('Activated')
              sharing_request_id.update({'status':'Activated'})
              sharing_request_id.broker.sudo().active_suppliers = [(4,sharing_request_id.developer.id)]
              sharing_request_id.developer.sudo().active_brokers = [(4,sharing_request_id.broker.id)]
             self.env['ir.cron'].clear_caches()  
                