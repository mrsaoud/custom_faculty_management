from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    first_name_arabic = fields.Char(string='Prénom en arabe')
    last_name_arabic = fields.Char(string='Nom en arabe')
    some_number = fields.Char(string='N° SOME')
    cnss_number = fields.Char(string='N° CNSS')
    rib = fields.Char(string='RIB')

    _sql_constraints = [
        ('check_rib_format', 'CHECK(rib ~* \'^[0-9]{24}$\' OR rib IS NULL)',
         'Le RIB doit contenir 24 chiffres.'),
    ]