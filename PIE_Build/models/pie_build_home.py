# -*- coding: utf-8 -*-
from odoo import api ,fields, models,exceptions
import logging
from odoo.exceptions import ValidationError
_logger = logging.getLogger(__name__)


class Build_Property(models.TransientModel):
    _name = "pie.build.home"

    name = fields.Char(string="Property Name",size=150)

    project_count = fields.Integer(compute='_get_project_count')
    prop_count=fields.Integer(compute='_get_prop_count',required=True)
    import_supplier = fields.Many2one('pie.entity')
    import_project = fields.Many2one('pie.project')
    import_file=fields.Binary(string="File")
    view_project = fields.Many2one('pie.project')
    publish_supplier = fields.Many2one('pie.entity')
    publish_project = fields.Many2one('pie.project')


    @api.depends('project_count')
    def _get_project_count(self):
        self.project_count = self.env['pie.project'].search_count([])

    @api.depends('prop_count')
    def _get_prop_count(self):
        self.prop_count = self.env['pie.build.property'].search_count([])