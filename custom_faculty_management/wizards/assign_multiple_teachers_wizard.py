from odoo import fields, models, api, _

class AssignMultipleTeachersWizard(models.TransientModel):
    _name = 'assign.multiple.teachers.wizard'
    _description = 'Assistant d\'affectation multiple d\'enseignants'

    annee_id = fields.Many2one(
        'uni.annee', string='Année universitaire', required=True,
        default=lambda self: self.env['uni.annee'].search([('state', '=', 'current')], limit=1)
    )
    ecole_id = fields.Many2one('uni.ecole', string='École', required=True)
    niveau_id = fields.Many2one(
        'uni.niveau', string='Niveau', required=True,
        domain="[('option_id.filiere_id.ecole_id', '=', ecole_id)]"
    )
    semestre_id = fields.Many2one(
        'uni.semestre', string='Semestre', required=True,
        domain="[('niveau_id', '=', niveau_id), ('annee_id', '=', annee_id)]"
    )
    classe_id = fields.Many2one('op.class', string='Classe')  # si vous utilisez op.class
    module_id = fields.Many2one(
        'uni.module', string='Module', required=True,
        domain="[('semestre_id', '=', semestre_id)]"
    )
    element_id = fields.Many2one(
        'uni.element', string='Élément',
        domain="[('module_id', '=', module_id)]"
    )
    role = fields.Selection([
        ('responsable', 'Responsable de module'),
        ('intervenant', 'Intervenant'),
        ('td', 'Encadrant TD'),
        ('tp', 'Encadrant TP'),
    ], string='Rôle', required=True, default='intervenant')
    volume_horaire = fields.Float(string='Volume horaire par enseignant (h)')
    faculty_ids = fields.Many2many('op.faculty', string='Enseignants', required=True)

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    def action_assign(self):
        self.ensure_one()
        Assignment = self.env['faculty.assignment']
        created = 0
        for faculty in self.faculty_ids:
            vals = {
                'faculty_id': faculty.id,
                'annee_id': self.annee_id.id,
                'semestre_id': self.semestre_id.id,
                'module_id': self.module_id.id,
                'element_id': self.element_id.id if self.element_id else False,
                'role': self.role,
                'volume_horaire': self.volume_horaire,
            }
            # Éviter les doublons (la contrainte SQL fera le nécessaire mais on peut vérifier)
            existing = Assignment.search([
                ('faculty_id', '=', faculty.id),
                ('annee_id', '=', self.annee_id.id),
                ('module_id', '=', self.module_id.id),
                ('element_id', '=', self.element_id.id if self.element_id else False),
                ('role', '=', self.role)
            ])
            if not existing:
                Assignment.create(vals)
                created += 1

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Affectations créées'),
                'message': _('%d enseignant(s) ont été affectés à %s') % (created, self.module_id.display_name),
                'type': 'success',
                'sticky': False,
            }
        }