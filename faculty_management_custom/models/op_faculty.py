from odoo import fields, models, api, _

class OpFaculty(models.Model):
    _inherit = 'op.faculty'

    faculty_code = fields.Char(string='Code enseignant', required=True, copy=False,
                               default=lambda self: _('New'))
    first_name_arabic = fields.Char(related='partner_id.first_name_arabic', store=True)
    last_name_arabic = fields.Char(related='partner_id.last_name_arabic', store=True)
    some_number = fields.Char(related='partner_id.some_number', store=True)
    cnss_number = fields.Char(related='partner_id.cnss_number', store=True)
    rib = fields.Char(related='partner_id.rib', store=True)

    # Liens vers les modèles spécifiques
    contract_ids = fields.One2many('faculty.contract', 'faculty_id', string='Contrats')
    assignment_ids = fields.One2many('faculty.assignment', 'faculty_id', string='Affectations')

    @api.model
    def create(self, vals):
        if vals.get('faculty_code', _('New')) == _('New'):
            vals['faculty_code'] = self.env['ir.sequence'].next_by_code('op.faculty') or _('New')
        return super().create(vals)