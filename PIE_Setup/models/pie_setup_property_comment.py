from odoo import models,fields,api
from odoo.exceptions import ValidationError
class comment(models.Model):
    _name="pie.setup.property_comments"
    comment=fields.Char('comment',size=255)
    share_type=fields.Selection([('public','Public'),('Specific ','Specific'),('private','Private')],'Share type',default='private',store=True)
    share_with=fields.Many2many('res.users',string="Share With",relation="comment_userd",column1="comment_id",column2="user_id")
    comments_line=fields.Many2one('pie.setup.property_status',string='Comments',ondelete='cascade',index=True, copy=False)
    entity_id=fields.Integer('entity Id')
    shared_user_id=fields.Integer('shared_user_id')
    @api.constrains('share_type')
    def get_number_comment(self):
     user_in_entity=self.env['res.users'].browse(self.env.uid)
      
      
     
     
     
     if self.share_type=="public":
      if user_in_entity.sale_agent>0:
       self.entity_id=user_in_entity.sale_agent
       
      else:
       self.entity_id=user_in_entity.broker_admin.id
      com=self.search([('create_uid','=',self.env.uid),('share_type','=','public'),('comments_line','=',self.comments_line.id)])
     
      if len(com)>1:
       raise ValidationError('user can add only public comment')
     elif self.share_type=="private":
      com=self.search([('create_uid','=',self.env.uid),('share_type','=','private'),('comments_line','=',self.comments_line.id)])
      if len(com)>1:
       raise ValidationError('user can add only private comment')
     else:
      values = {}
      values['comment'] = 'dddd'
      values['share_type']=self.share_type
      
     
    
        
         
     

     
