from odoo import api ,models,fields
class labels_property(models.Model):
    _name="pie.setup.property.labels"
    share_type=fields.Selection([('public','Public'),('private','Private'),('specific ','Specific ')],'Share type',default='public')
    share_with=fields.Many2many('res.users',string="Share With")
    label=fields.Many2many('pie.setup.label',string='labels')
    broker = fields.Many2one('pie.entity',string="Broker",store=True,domain="[('pie_type','=','is_broker')]",default=lambda self: self.env.user.entity)
    comment=fields.Char('Comment')
    @api.constrains('label')
    def duplicate_label(self):
        records=self.env['pie.setup.property.labels'].search([('create_uid','=',self.env.uid)])
        _logger.warn(records)
        ids="("
        for rec in records:
            ids+=str(rec.id)+","
        
        if records:
            ids=ids[:-1] 
            ids+=")"
            sql = "SELECT pie_setup_label_id FROM pie_setup_label_pie_setup_property_labels_rel WHERE pie_setup_property_labels_id IN"+ids
            self.env.cr.execute(sql)
            res_name = self.env.cr.fetchall()  
            res_name2=list(set(res_name))
            _logger.warn('result')
            _logger.warn(len(res_name))
            _logger.warn(len(res_name2))
            if len(res_name)>len(res_name2):
                raise ValidationError('label is selected before .....')
             
             
             
    @api.onchange('share_type')
    def remove_share_with(self):
        for rec in self:

            if rec.share_type !='specific':
                 rec.share_with=[]
   