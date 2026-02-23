from odoo import fields, models, api, _

class FacultyAssignment(models.Model):
    _name = 'faculty.assignment'
    _description = 'Affectation pédagogique d\'un enseignant'
    _rec_name = 'display_name'
    _order = 'annee_id desc, semestre_id, module_id'

    faculty_id = fields.Many2one('op.faculty', string='Enseignant', required=True, ondelete='cascade')
    annee_id = fields.Many2one('uni.annee', string='Année universitaire', required=True, ondelete='cascade')
    semestre_id = fields.Many2one('uni.semestre', string='Semestre', required=True,
                                  domain="[('annee_id', '=', annee_id)]")
    module_id = fields.Many2one('uni.module', string='Module', required=True,
                                domain="[('semestre_id', '=', semestre_id)]")
    element_id = fields.Many2one('uni.element', string='Élément',
                                 domain="[('module_id', '=', module_id)]")
    role = fields.Selection([
        ('responsable', 'Responsable de module'),
        ('intervenant', 'Intervenant'),
        ('td', 'Encadrant TD'),
        ('tp', 'Encadrant TP'),
    ], string='Rôle', required=True, default='intervenant')
    volume_horaire = fields.Float(string='Volume horaire prévu (h)')
    notes = fields.Text(string='Notes')

    display_name = fields.Char(string='Affichage', compute='_compute_display_name', store=True)

    _sql_constraints = [
        ('unique_assignment',
         'UNIQUE(faculty_id, annee_id, module_id, element_id, role)',
         'Cet enseignant est déjà affecté à cet élément/module avec ce rôle pour cette année.'),
    ]

    @api.depends('faculty_id', 'module_id', 'element_id', 'role')
    def _compute_display_name(self):
        for rec in self:
            if rec.element_id:
                rec.display_name = f"{rec.faculty_id.name} - {rec.module_id.code}/{rec.element_id.code} ({rec.role})"
            else:
                rec.display_name = f"{rec.faculty_id.name} - {rec.module_id.code} ({rec.role})"