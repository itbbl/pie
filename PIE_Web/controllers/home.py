# -*- coding: utf-8 -*-
import odoo.http as http

class your_class(http.Controller):
     @http.route('/about', type='http', auth='public', website=True)
     def show_about_webpage(self, **kw):
          return http.request.render('PIE_Web.PIE_About_Page', {})

     @http.route('/register', type='http', auth='public', website=True)
     def show_register_webpage(self, **kw):
          return http.request.render('PIE_Web.PIE_register_Page', {})

     @http.route('/terms', type='http', auth='public', website=True)
     def show_terms_webpage(self, **kw):
          return http.request.render('PIE_Web.PIE_terms_Page', {})

     @http.route('/privacy', type='http', auth='public', website=True)
     def show_privacy_webpage(self, **kw):
          return http.request.render('PIE_Web.PIE_privacy_Page', {})

     @http.route('/contact', type='http', auth='public', website=True)
     def show_contact_webpage(self, **kw):
          return http.request.render('PIE_Web.PIE_contact_Page', {})

     @http.route('/broker-company', type='http', auth='public', website=True)
     def show_broker_company_webpage(self, **kw):
          return http.request.render('PIE_Web.PIE_Broker_Company_page', {})

     @http.route('/broker-individual', type='http', auth='public', website=True)
     def show_broker_indv_webpage(self, **kw):
          return http.request.render('PIE_Web.PIE_Broker_individual_page', {})

     @http.route('/supplier-developer', type='http', auth='public', website=True)
     def show_supplier_developer_webpage(self, **kw):
          return http.request.render('PIE_Web.PIE_supplier_developer_Page', {})

     @http.route('/supplier-reseller', type='http', auth='public', website=True)
     def show_supplier_broker_webpage(self, **kw):
          return http.request.render('PIE_Web.PIE_supplier_reseller_Page', {})
        
