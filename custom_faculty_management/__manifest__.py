{
    'name': 'Custom Faculty Management',
    'version': '18.0.1.0.0',
    'category': 'Education',
    'summary': 'Gestion avancée des enseignants avec grades, contrats par année et affectations',
    'description': """
        Ajoute les fonctionnalités suivantes :
        - Grades des enseignants (op.grade)
        - Champs marocains : CNSS, SOME, RIB, noms en arabe
        - Contrats des enseignants par année universitaire (grade, statut, école)
        - Affectations pédagogiques (module/élément)
        - Assistant d'affectation multiple d'enseignants
    """,
    'author': 'UPM Team',
    'depends': [
        'base', 
        'mail',
        'openeducat_core',          
        'contacts',                 
        'hr',    
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/op_grade_views.xml',
        'views/faculty_contract_views.xml',
        'views/faculty_assignment_views.xml',
        'views/op_faculty_views.xml',
        'views/menus.xml',
        'wizards/assign_multiple_teachers_wizard_view.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}