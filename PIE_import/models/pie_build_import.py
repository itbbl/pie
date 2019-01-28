# -*- coding: utf-8 -*-
#import openpyxl
from odoo import api ,fields, models,exceptions
from odoo.api import Environment as env
from tempfile import TemporaryFile
import logging
import itertools
from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
_logger = logging.getLogger(__name__)
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
    _logger = logging.getLogger(__name__)
try:
    import xlrd
    try:
        from xlrd import xlsx
    except ImportError:
        xlsx = None
except ImportError:
    xlrd = xlsx = None


class Supplier_import(models.Model):
    _name = "pie.build.import"
    
    #supplier_list = fields.One2many('pie.entity')
    supplier = fields.Many2one('pie.entity',string='File Owner',default=lambda self: self.env.user.entity)
    #developer = fields.Many2one('pie.entity',string='File Owner', required=True )
   
    mapping_id=fields.Many2one('pie.build.mapping')
    imported_file = fields.Binary(string='File To Import', required=True)
    import_date = fields.Date(string='File Date' ,required=True)
    has_project = fields.Boolean(string='File Has Project Column ?',default=True)
    project = fields.Many2one('pie.project',string="Project")
    binary_fname = fields.Char('File Name')
    
    sharing_level = fields.Selection([('public','Public'),('private','Private')],default='public')
    
    #active_import = fields.Boolean(string='IS Active import',default=False)
   
    @api.model
    def _get_default_supplier(self):
        if self.env.user.company_id.id == 1:
            _logger.warn(self.env['pie.entity'].search([['id','=',2]]))
            return  self.env['pie.entity'].search([['id','=',2]])




    @api.model
    def create(self, values):
        # Override the original create function for the res.partner model
        record = super(Supplier_import, self).create(values)
        _logger.warn(record)
        data = values
        #data['form'] = self.read(['supplier','has_project','imported_file','mapping_id','project','import_date'])[0]
        supplier = data['supplier']
        has_project = data['has_project']
        imported_file = data['imported_file']
        
        upload_date = data['import_date']
        file_to_import = imported_file.decode('base64')
        sharing_level = "public"
        
        

        

        _logger.warn(record)
	return record
   
    def _get_suppliers(self):
        sups_list = self.env['pie.entity'].search([[('id','=',2)]])
        _logger.warn(sups_list)
        return sups_list
    def Preview_Data(self, data):
        """Redirects to the report with the values obtained from the wizard
        'data['form']': name of employee and the date duration"""
        data = {}
        data['form'] = self.read(['supplier','has_project','imported_file','mapping_id','project','import_date','sharing_level'])[0]
        
        supplier = data['form']['supplier'][0]
        has_project = data['form']['has_project']
        imported_file = data['form']['imported_file']
        mapping_id = data['form']['mapping_id']
        upload_date = data['form']['import_date']
        file_to_import = imported_file.decode('base64')
        sharing_level = data['form']['sharing_level']
        
        if not has_project:
            
            if data['form']['project'][0]:
                project_id = data['form']['project'][0]
                _logger.warn(project_id)
            else:
                raise exceptions.ValidationError("No Project is Selected in Project Menu")

            
        book = xlrd.open_workbook(file_contents=file_to_import)
        sheet = book.sheet_by_index(0)
        headers_in_file = sheet.row(0)
        text_headers = []
        sup_id = supplier
        
        for cell in headers_in_file:
            text_headers.append(unicode(cell.value).lower())
        
        column_mapping = self.env['pie.build.mapping'].search([['active','=',True],['developer','=',supplier]], limit=1)
        if column_mapping:
            
            supplier = self.env['pie.entity'].search([['id','=',sup_id]])
            columns_headers_map = []
            for col_record in column_mapping:
                #columns = record.columns_mapping_ids.mapped('supplier_column')
                property_code_column_header = ''
                project_column_header = ''

                for mapped_column in col_record.columns_mapping_ids:
                    if mapped_column.pie_column2 == 'property_code':
                        if mapped_column.supplier_column.lower() in text_headers:
                            property_code_column_header = mapped_column.supplier_column
                        else:
                            raise exceptions.ValidationError("We Cannot Find Property Code Column in the File.\n  Check your Inventory Structure , Or Headers in uploaded file")

                    if mapped_column.pie_column2 == 'project':
                        if mapped_column.supplier_column.lower() in text_headers:
                            project_column_header = mapped_column.supplier_column

                    entity = self.env['pie.entity'].search([['id','=',sup_id],['pie_type','=','is_supplier']])

                    if mapped_column.pie_column2 == 'developer' and not entity:
                        if mapped_column.supplier_column.lower() in text_headers:
                            project_column_header = mapped_column.supplier_column
                        else:
                            raise exceptions.ValidationError("We Cannot Find Developer Column in the File. \n  Check your Inventory Structure , Or Headers in uploaded file")

                    try:
                        columns_headers_map.append((text_headers.index(unicode(mapped_column.supplier_column).lower()),unicode(mapped_column.supplier_column).lower(),unicode(mapped_column.pie_column2).lower()))
                    except:
                        _logger.warn(mapped_column.pie_column2 + " Wasn't find in mapping")
            

                if property_code_column_header == '' and has_project:
                    raise exceptions.ValidationError("We Cannot Find Project Column in the File , Kindly Check your File Mapping , Or Select Project From DropDown Menu")

                if not has_project:
                    project_id = project_id
                    projectt = self.env['pie.project'].search([['id','=',project_id]])
                    recs = self.env['pie.build.draft'].search([['supplier','=',supplier.id],['project','=',projectt.name]])
                    for rec in recs:
                        rec.unlink()
                    self._cr.commit()

                else:
                    recs = self.env['pie.build.draft'].search([['supplier','=',supplier.id]])
                    for rec in recs:
                        rec.unlink()
                    self._cr.commit()
                #_logger.warn(columns)

                for row in itertools.imap(sheet.row, range(1,sheet.nrows)):
                    prop = {}
                    for r in columns_headers_map:
                        prop.update({unicode(r[2]):unicode(row[r[0]].value)})
                        entity = self.env['pie.entity'].search([['id','=',sup_id],['pie_type','=','is_supplier']])
                        
                        if entity:
                            prop.update({'developer':entity.id})
                            prop.update({'is_secondary':False})
                            prop.update({'is_primary':True})
                        else:
                            prop.update({'is_secondary':True})
                            prop.update({'is_primary':False})

                        if not has_project:
                            project = self.env['pie.project'].search([['id','=',project_id]])
                            if project:
                                prop.update({'project':project.name})
                        #_logger.warn(text_headers)
                        prop.update({'property_id':str(sup_id)+'-'+row[text_headers.index(property_code_column_header.lower())].value})
                        prop.update({'upload_date':upload_date})
                        prop.update({'has_errors':True})
                        prop.update({'supplier':supplier.id})
                        prop.update({'sharing_level':sharing_level})
                        #_logger.warn(record.id)
                        #_logger.warn(self)
                        #prop.update({'import_id':record.id})
                    #_logger.warn(prop)
                    iddd = self.env['pie.build.draft'].create(prop)
                    
                    iddd_history = self.env['pie.build.history'].create(prop)
                    self._cr.commit()

                _logger.warn("######################## mapped headers")
                _logger.warn(columns_headers_map)

            #raise exceptions.ValidationError("Data Imported into the PIE Draft")
        else:
            _logger.warn("No Header")
            #_logger.warn(headers_in_file)
            raise exceptions.ValidationError("Kindly Make Sure you have an active File Mapping.")
        
   
    def Import_Data(self, data):

        data['form'] = self.read(['supplier','has_project','imported_file','project','import_date','sharing_level'])[0]
        
        supplier_id = data['form']['supplier'][0]
        has_project = data['form']['has_project']
        imported_file = data['form']['imported_file']
        upload_date = data['form']['import_date']
        file_to_import = imported_file.decode('base64')
        sharing_level = data['form']['sharing_level']

        if not has_project: 
            if data['form']['project'][0]:
                project_id = data['form']['project'][0]
                _logger.warn(project_id)
            else:
                raise exceptions.ValidationError("No Project is Selected in Project Menu")

        #reading file From Excel sheet
        book = xlrd.open_workbook(file_contents=file_to_import)
        sheet = book.sheet_by_index(0)
        headers_in_file = sheet.row(0)
        file_columns_headers = []
        
        Mapped_columns = []
        property_code_column_header =''
        for cell in headers_in_file:
            file_columns_headers.append(unicode(cell.value.lower().strip()))
        _logger.warn("File Columns headers")
        _logger.warn(file_columns_headers)
        if len(headers_in_file) == 0:
            raise exceptions.ValidationError("Make Sure that the First Row has the Right Column header")

        column_mapping = self.env['pie.build.mapping'].search([['active','=',True],['developer','=',supplier_id]], limit=1)

        if not column_mapping:
            raise exceptions.ValidationError("Kindly Make Sure you have an active File Mapping.")
        
        project_mapped_name = column_mapping.columns_mapping_ids
        
        for col in column_mapping.columns_mapping_ids:
            if col.pie_column2 == 'project' and has_project:
                if not col.supplier_column.lower() in file_columns_headers:
                    raise exceptions.ValidationError("We Cannot Find Project Column in Uploaded File. \n  Check your Inventory Structure , Or Headers in uploaded file")
                else:
                    col_index = file_columns_headers.index(unicode(col.supplier_column.lower()))
                    projects_list = sheet.col_values(col_index, 1)
                    #_logger.warn(projects_list)
                    if '' in projects_list:
                        raise exceptions.ValidationError("Empty Values in Project Column")

            if col.pie_column2 == 'property_code':
                if not col.supplier_column.lower() in file_columns_headers:
                    raise exceptions.ValidationError("We Cannot Find Property Code Column in Uploaded File. \n  Check your Inventory Structure , Or Headers in uploaded file")
                else:
                    property_code_column_header = col.supplier_column
                    col_index = file_columns_headers.index(unicode(col.supplier_column.lower()))
                    codes_list = sheet.col_values(col_index, 1)
                    #_logger.warn(codes_list)
                    if '' in codes_list:
                        raise exceptions.ValidationError("Empty Values in Property Code Column")


            try:

                Mapped_columns.append((file_columns_headers.index(unicode(col.supplier_column.lower())),col.supplier_column.lower(),col.pie_column2.lower()))
                _logger.warn(Mapped_columns)
            except:
                _logger.warn(col.pie_column2 + " Wasn't find in mapping")


        if not has_project:
            projectt = self.env['pie.project'].search([['id','=',project_id]])
            recs = self.env['pie.build.draft'].search([['supplier','=',supplier_id],['project','=',projectt.name]])
            for rec in recs:
                rec.unlink()
            self._cr.commit()
        else:
            recs = self.env['pie.build.draft'].search([['supplier','=',supplier_id]])
            for rec in recs:
                rec.unlink()
            self._cr.commit()
            #_logger.warn(columns)
        
        for row in itertools.imap(sheet.row, range(1,sheet.nrows)):
            prop = {}
            for r in Mapped_columns:
                prop.update({unicode(r[2]):unicode(row[r[0]].value)})
                entity = self.env['pie.entity'].search([['id','=',supplier_id],['pie_type','=','is_supplier']])
                
                if entity:
                    prop.update({'developer':entity.name})
                    prop.update({'is_secondary':False})
                    prop.update({'is_primary':True})
                else:
                    prop.update({'is_secondary':True})
                    prop.update({'is_primary':False})

                if not has_project:
                    project = self.env['pie.project'].search([['id','=',project_id]])
                    if project:
                        prop.update({'project':project.name})
                #_logger.warn(text_headers)
                prop.update({'property_id':str(supplier_id)+'-'+row[file_columns_headers.index(property_code_column_header.lower())].value})
                prop.update({'upload_date':upload_date})
                prop.update({'has_errors':True})
                prop.update({'supplier':supplier_id})
                prop.update({'sharing_level':sharing_level})
                #_logger.warn(record.id)
                #_logger.warn(self)
                _logger.warn(self)
                prop.update({'importid':self.id})
            #_logger.warn(prop)
            iddd = self.env['pie.build.draft'].create(prop)
            
            iddd_history = self.env['pie.build.history'].create(prop)
            self._cr.commit()
            _logger.warn("Row Imported")

        
        action = self.env.ref('PIE_Build.action_prop_list_draft').read()[0]
        return action