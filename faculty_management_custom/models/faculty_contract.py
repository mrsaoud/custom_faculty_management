from odoo import fields, models, api, _

class FacultyContract(models.Model):
    _name = 'faculty.contract'
    _description = 'Contrat / Affectation annuelle de l\'enseignant'
    _rec_name = 'display_name'
    _order = 'annee_id desc, faculty_id'

    faculty_id = fields.Many2one('op.faculty', string='Enseignant', required=True, ondelete='cascade')
    annee_id = fields.Many2one('uni.annee', string='Année universitaire', required=True, ondelete='cascade')
    ecole_id = fields.Many2one('uni.ecole', string='Établissement', required=True)
    filiere_id = fields.Many2one('uni.filiere', string='Filière', domain="[('ecole_id', '=', ecole_id)]")
    department_id = fields.Many2one('op.department', string='Département')
    grade_id = fields.Many2one('op.grade', string='Grade', required=True)
    status = fields.Selection([
        ('permanent', 'Permanent'),
        ('vacataire', 'Vacataire'),
        ('visitor', 'Visiteur'),
        ('emeritus', 'Émérite'),
    ], string='Statut', required=True, default='permanent')
    is_primary = fields.Boolean(string='Affectation principale', default=True,
                                help="Une seule affectation principale par enseignant et par année.")
    start_date = fields.Date(string='Date de début')
    end_date = fields.Date(string='Date de fin')
    active = fields.Boolean(default=True)

    display_name = fields.Char(string='Affichage', compute='_compute_display_name', store=True)

    _sql_constraints = [
        ('unique_primary_per_year',
         'UNIQUE(faculty_id, annee_id, is_primary)',
         'Un enseignant ne peut avoir qu\'une seule affectation principale par année.'),
    ]

    @api.depends('faculty_id', 'annee_id', 'ecole_id', 'grade_id')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.faculty_id.name} - {rec.annee_id.name} - {rec.ecole_id.name} ({rec.grade_id.name})"