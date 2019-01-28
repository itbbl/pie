from odoo import api ,fields, models,exceptions

from datetime import date,datetime,timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
import logging
_logger=logging.getLogger(__name__)

class advance_search(models.Model):
 _name="pie.advanced.search"
 region = fields.Many2many('pie.setup.region',string="Governorate",store=True)#done

  
 name=fields.Char('name',default="Search property")  
 district = fields.Char(string="District" ,size=100)
 property_type = fields.Many2many('pie.setup.category',store=True)#done

 property_status = fields.Many2many('pie.setup.property_status',store=True)#done
 property_design = fields.Many2many('pie.setup.property_design',store=True)#done

 area = fields.Many2many('pie.setup.area',string="Area",size=150,store=True)#done
 finishing = fields.Many2many('pie.setup.finishing',string="Finishing Type",store=True)#done

 developers = fields.Many2many('pie.entity',string='Developer' ,store=True)#done
 projects = fields.Many2many('pie.project',size=150,store=True)#done
 rooms = fields.Many2many('pie.setup.room',string="Count of Rooms",store=True)#done
  
 #property_code_list = fields.Selection(('',''),string="Property Code",size=100)
 property_code =fields.Char(string="Property code")
 bathrooms = fields.Many2many('pie.setup.bathrooms',string="Bathroom",store=True)#done
 Basement = fields.Boolean(string="Basement") #done
 Garden = fields.Boolean(string="Garden") #done
 Terrace = fields.Boolean(string="Terrace") #done
 Garage = fields.Boolean(string="Garage") #done
 Roof = fields.Boolean(string="Roof") #done
 Land = fields.Boolean(string="Land") #done
 bua_from = fields.Float(string="BUA From",size=10)#done 
 bua_to = fields.Float(string="BUA To ",size=10)#done
 price_from  = fields.Float(string="Price From",size=10,default=0)#done
 price_to = fields.Float(string="Price To",size=10)#done
 price_to_m = fields.Float(string="Price to_m",size=10)#done not find in grid
 price_from_m  = fields.Float(string="Price/m from",size=10)#done not find in grid
 
 deposit_from  = fields.Float(string="Deposit From",size=10)#done not find in grid
 deposited_to = fields.Float(string="Deposit To",size=10)#done not find in grid
 installment_from =  fields.Float(string="Installment From",size=10)#done not find in grid
 installment_to =  fields.Float(string="Installment To",size=10)#done not find in grid
 Market = fields.Selection([('primary','Primary Market'),('secondary','Secondary Market')])

 @api.onchange('projects','developers')
 def projects_list(self):
    
    project = self.env['pie.grid.property'].search([])

    res = []
    dev=[]
    if project:
        for record in project:
     
            res.append((record.project.id))
    _logger.warn('project')
    _logger.warn(res)
    res=list(set(res))
    if self.developers:
        for rec in self.developers:
            dev.append(rec.id)
        
        dev=list(set(dev))
        if self.projects:
            records=self.env['pie.project'].search(['&',('developer','in',dev),('id','in',res)])
            self.projects=[]
        else:
            return {'domain':{'projects':['&',('id','in',res),('developer','in',dev)]}} 
    else:
        return {'domain':{'projects':[('id','in',res)]}}
 

 

 @api.onchange('property_type')
 def property_type_list(self):
    category = self.env['pie.grid.property'].search([])
    res = []
    if category:
        for record in category:
            
            res.append((record.property_type.id))
    _logger.warn('property_type')
    _logger.warn(res)
    res=list(set(res))
    return {'domain':{'property_type':[('id','in',res)]}}

 @api.onchange('property_design')
 def property_design_list(self):
    property_design = self.env['pie.grid.property'].search([])
    res = []
    if property_design:
        for record in property_design:
            
            res.append((record.property_design.id))
    _logger.warn('property_design')
    _logger.warn(res)
    res=list(set(res))
    return {'domain':{'property_design':[('id','in',res)]}}

 @api.onchange('property_status')
 def property_status_list(self):
    property_status = self.env['pie.grid.property'].search([])
    res = []
    if property_status:
        for record in property_status:
            res.append((record.property_status.id))
    _logger.warn('property_status')
    _logger.warn(res) 
     
    res=list(set(res))
    return {'domain':{'property_status':[('id','in',res)]}}


 @api.onchange('region')
 def region_list(self):
    regions = self.env['pie.grid.property'].search([])
    res = []
    if regions:
        for record in regions:
            
            res.append((record.region.id))
    _logger.warn('region')
    _logger.warn(res)
    res=list(set(res))
    
    
    return {'domain':{'region':[('id','in',res)]}}


 @api.onchange('area','region')
 def area_list(self):
    regions = self.env['pie.grid.property'].search([])
    res = []
    dev=[]
    if regions:
        for record in regions:
            
            res.append((record.area.id))
    _logger.warn('region')
    _logger.warn(res)
    res=list(set(res))
    if self.region:
        for rec in self.region:
            dev.append(rec.id)
         
        dev=list(set(dev))
        _logger.warn('devvvvvvvvvvv')
        _logger.warn(dev)
        area_project=self.env['pie.project'].search([('region','in',dev)])
        dev=[]
        for rec in area_project:
            dev.append(rec.area.id)
        if self.area:
            self.area=[]
        else:
            return {'domain':{'area':['&',('id','in',res),('id','in',dev)]}}
    else:
        return {'domain':{'area':[('id','in',res)]}}
  
 

 @api.onchange('property_code')
 def get_property_code_d(self):
     if self.property_code:
        res = []
        
        property_code = self.env['pie.grid.property'].search([('property_code','like',self.property_code)])
        for record in property_code:
            res.append((record.property_code))

        
        #sorted_x = sorted(res.items(), key=operator.itemgetter(1))
        res=list(set(res))
        return res

 @api.onchange('finishing')
 def finishing_list(self):
    finishing = self.env['pie.grid.property'].search([])
    res = []
    if finishing:
        for record in finishing:
            res.append((record.finishing_type.id))
    _logger.warn('finishing')
    _logger.warn(res) 
     
    res=list(set(res))
    return {'domain':{'finishing':[('id','in',res)]}}


 @api.onchange('developers')
 def developers_list(self):
    developers = self.env['pie.grid.property'].search([])
    res = []
    if developers:
        for record in developers:
            res.append((record.supplier.id))
         
    _logger.warn('developers')
    _logger.warn(res) 
     
    res=list(set(res))
    
    return {'domain':{'developers':[('id','in',res)]}}
  
 @api.onchange('rooms')
 def rooms_list(self):
    rooms = self.env['pie.grid.property'].search([])
    res = []
    if rooms:
        for record in rooms:
            res.append((record.rooms.id))
    _logger.warn('rooms')
    _logger.warn(res) 
     
    res=list(set(res))
    return {'domain':{'rooms':[('id','in',res)]}}

 @api.onchange('bathrooms')
 def bathrooms_list(self):
    bathrooms = self.env['pie.grid.property'].search([])
    res = []
    if bathrooms:
        for record in bathrooms:
            res.append((record.baths.id))
    _logger.warn('rooms')
    _logger.warn(res) 
     
    res=list(set(res))
    return {'domain':{'bathrooms':[('id','in',res)]}}
 
 
 
 
 
 
 def advance_search_property(self):
  dev,pro,property_type,property_status,property_design,finishing,area,region=([] for i in range(8))
  strs=""
  domain={}
  str_domain=""
  values=""
  property_code="'"+"'"
  if self.developers:
         strs=""
         for subjj in self.developers:
            strs+=str(subjj.id)+","
         strs=strs[:-1]  
         strs="("+strs+")"
         str_domain+="supplier in"+strs+" and "

  if self.projects:
         strs=""
         for subjj in self.projects:
            strs+=str(subjj.id)+","
         strs=strs[:-1] 
         strs="("+strs+")"
         str_domain+="project in"+strs+" and "
    
    
  if self.rooms:
         strs=""
         for subjj in self.rooms:
            strs+=str(subjj.id)+","
         strs=strs[:-1] 
         strs="("+strs+")"
         str_domain+="rooms in"+strs+" and "
  if self.bathrooms:
         strs=""
         for subjj in self.bathrooms:
            strs+=str(subjj.id)+","
         strs=strs[:-1] 
         strs="("+strs+")"
         str_domain+="bathrooms in"+strs+" and "
  
  if self.property_type:
         strs=""
         for subjj in self.property_type:
            strs+=str(subjj.id)+","
         strs=strs[:-1]  
         strs="("+strs+")"
         str_domain+="property_type in"+strs+" and "

  if self.property_status:
         strs=""
         for subjj in self.property_status:
            strs+=str(subjj.id)+","
         strs=strs[:-1]  
         strs="("+strs+")"
         str_domain+="property_status in"+strs+" and "

  if self.property_design:
         strs=""
         for subjj in self.property_design:
            strs+=str(subjj.id)+","
         strs=strs[:-1]  
         strs="("+strs+")"
         str_domain+="property_design in"+strs+" and "

  if self.finishing:
         strs=""
         for subjj in self.finishing:
            strs+=str(subjj.id)+","
         strs=strs[:-1] 
         strs="("+strs+")"
         str_domain+="finishing_type in"+strs+" and "

  if self.property_code:
    str_domain+="property_code like '%"+self.property_code+"%'"+" and "
  if self.district:
    str_domain+="district like '%"+self.district+"%'"+" and "
  if self.area:
         strs=""
         dev=[]
         #raise ValidationError(self.area)
         for rec in self.area:
             dev.append(rec.id)
         area=self.env['pie.project'].search([('area','in',dev)])
         
         for subjj in area:
            strs+=str(subjj.id)+","
         strs=strs[:-1] 
         strs="("+strs+")"

         str_domain+="project in"+strs+" and "
         #raise ValidationError(str_domain)

  if self.region:
         strs=""
         dev=[]
         for rec in self.region:
             dev.append(rec.id)
         region=self.env['pie.project'].search([('region','in',dev)])
         for subjj in region:
            strs+=str(subjj.id)+","
         strs=strs[:-1] 
         strs="("+strs+")"

         str_domain+="project in"+strs+" and "
  if self.price_from:
        str_domain+="price >="+str(self.price_from)+" and "
  if self.price_to:
        str_domain+="price <="+str(self.price_to)+" and "
  if self.bua_from:
        str_domain+="built_up >="+str(self.bua_from)+" and "
  if self.bua_to:
        str_domain+="built_up <="+str(self.bua_to)+" and "
  if self.Basement:
    str_domain+="basement_m ="+str(self.Basement)+" and "
  if self.Garden:
    str_domain+="garden_m ="+str(self.Garden)+" and "
  if self.Terrace:
    str_domain+="terrace_m ="+str(self.Terrace)+" and "
  """if self.Garage:
    str_domain+="basement_m ="+str(self.Basement)+" and """
  if self.Roof:
    str_domain+="roof_m ="+str(self.Roof)+" and "

  if self.Land:
    str_domain+="land_m ="+str(self.Land)+" and "
  """if self.installment_from:
        str_domain+="installment >="+str(self.price_from_m)+" and "
   if self.installment_to:
        str_domain+="installment <="+str(self.price_to_m)+" and
  if self.deposit_from:
        str_domain+="deposit >="+str(self.price_from_m)+" and "
   if self.deposit_to:
        str_domain+="deposit <="+str(self.price_to_m)+" and
  if self.price_from_m:
        str_domain+="built_up >="+str(self.price_from_m)+" and "
  if self.price_to_m:
        str_domain+="built_up <="+str(self.price_to_m)+" and """
  #domain="['&',('project','in',%s),('developers','in',%s),('property_type','in',%s),('property_status','in',%s),('property_design','in',%s),('fin#ishing_type','in',%s),('property_code','like',%s),('basement_m','=',%s),('terrace_m','=',%s),('garden_m','=',%s),('roof_m','=',%s),('land_m','=#',%s),('area','in',%s),('region','in',%s),('price','>=',%s)]"%(pro,dev,property_type,property_status,property_design,finishing,property_code,se#lf.Basement,self.Terrace,self.Garage,self.Roof,self.Land,area,region,self.price_from)
     
  if self.Market=="primary":
        str_domain+="is_primary ="+'True'+" and "
    
  elif self.Market=="secondary":
        str_domain+="is_secondary ="+'True'+" and "
  
   

  #str_domain="["+str_domain+"]"
  #domain= str_domain 
   
  sql = "select id from pie_grid_property where "+ str_domain+" 1=1"
  
  self.env.cr.execute(sql)
  res_name = self.env.cr.fetchall()
  self.name="Search property"
  domain="[('id','in',%s)]"%(res_name)
  
  return { 'name':'/',
         'view_type': 'form',
        'view_mode': 'tree,form',
        'res_model': 'pie.grid.property',
        'target': 'current',
         'domain':domain,
         'context':{},
        'type': 'ir.actions.act_window',
        
         
                   }


