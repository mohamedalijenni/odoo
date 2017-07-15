from odoo import api, fields, models, _


class Client(models.Model):   
    _inherit='res.partner'
    
    matricule_fiscale=fields.Char('Matricule fiscale')
#     tva = fields.Boolean('Exonore TVA')
#     fodec = fields.Boolean('Exonore fodec')
    garantie = fields.Boolean('Garantie')
#     name=fields.Char('nom')
#     telephone=fields.Integer('contact')
#     commercial=fields.Char('Commercial')
#     fodec=fields.Selection([('oui', 'Oui'), ('non', 'Non')], string='Exonore FODEC')
#     tva=fields.Char('TVA')