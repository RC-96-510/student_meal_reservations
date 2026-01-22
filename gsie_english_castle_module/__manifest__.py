# -*- coding: utf-8 -*-
{
    'name': "GESTIÓN ACADÉMICA - EC",
    "author": "Grupo SIE",
    'summary': 'Módulo EC.', 
    'version': "14.0.0.1",
	'category': "", 
    'description': """
        Módulo EC.
    """,          
    'depends': ['base', 'contacts', 'account','sale_subscription' ],
    'data': [
        "security/groups.xml",   
        "security/ir.model.access.csv",
        "views/gsie_inherit_respartner.xml",
        "views/gsie_padresec.xml",
        "views/gsie_family.xml",
        "views/gsie_grados.xml",
        "views/gsie_inherit_accmove.xml",
        "views/menu.xml",
  
    ],
    'installable': True,
	'auto_install': False,
	'application': True,
	"images":['static/description/icon.png'],


}

