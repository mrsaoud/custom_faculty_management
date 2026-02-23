from odoo import fields, models, api, _

class OpGrade(models.Model):
    _name = 'op.grade'
    _description = 'Grade des enseignants'
    _order = 'sequence, name'
    _rec_name = 'name'

    name = fields.Char(string='Grade', required=True, translate=True)
    code = fields.Char(string='Code', required=True)
    sequence = fields.Integer(string='Séquence', default=10)
    description = fields.Text(string='Description', translate=True)
    level = fields.Selection([
        ('bac+3', 'Bac+3'),
        ('bac+5', 'Bac+5'),
        ('master', 'Master'),
        ('doctorat', 'Doctorat'),
        ('desa', 'DESA'),
        ('other', 'Autre'),
    ], string='Niveau')
    active = fields.Boolean(string='Actif', default=True)
    faculty_count = fields.Integer(
        string='Nombre d\'enseignants',
        compute='_compute_faculty_count'
    )

    _sql_constraints = [
        ('unique_grade_code', 'unique(code)', 'Le code du grade doit être unique !'),
    ]

    @api.depends('name')
    def _compute_faculty_count(self):
        for grade in self:
            grade.faculty_count = self.env['op.faculty'].search_count(
                [('grade_ids.grade_id', '=', grade.id)]  # via les contrats
            )