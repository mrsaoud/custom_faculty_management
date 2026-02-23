from odoo import fields, models, api

class OpInstitution(models.Model):
    _name = 'op.institution'
    _description = 'Établissement / Organisme d\'origine'
    _order = 'name'

    name = fields.Char(string='Nom', required=True, translate=True)
    code = fields.Char(string='Code', required=True)
    type = fields.Selection([
        ('university', 'Université'),
        ('school', 'École'),
        ('institute', 'Institut'),
        ('company', 'Entreprise'),
        ('other', 'Autre'),
    ], string='Type', default='university')
    country_id = fields.Many2one('res.country', string='Pays')
    city = fields.Char(string='Ville')
    active = fields.Boolean(string='Actif', default=True)

    _sql_constraints = [
        ('unique_institution_code', 'unique(code)', 'Le code de l\'établissement doit être unique !'),
    ]