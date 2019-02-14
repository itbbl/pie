# -*- coding: utf-8 -*-
from odoo import api ,fields, models,exceptions
import logging
from odoo.exceptions import ValidationError
from odoo.http import request
_logger = logging.getLogger(__name__)


class Project(odoo.http.Controller):
    _name = "pie.clicks.listener"
    
    @http.route('/')
    def handler(self):
        httprequest = request.httprequest
        if not httprequest:
            return False
        _logger.warn()
        if httprequest:
            _logger.warn("Reqaaaaaaaaaaaaaa")
            _logger.warn(httprequest)