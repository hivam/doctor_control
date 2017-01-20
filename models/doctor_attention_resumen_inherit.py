# -*- coding: utf-8 -*-
##############################################################################
#
#	OpenERP, Open Source Management Solution
#	Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU Affero General Public License as
#	published by the Free Software Foundation, either version 3 of the
#	License, or (at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU Affero General Public License for more details.
#
#	You should have received a copy of the GNU Affero General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import logging
_logger = logging.getLogger(__name__)
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import date, datetime, timedelta


class doctor_attention_resumen_inherit(osv.osv):


	_name = "doctor.attentions.resumen"
	

	_inherit = 'doctor.attentions.resumen'


	_columns = {
		'Controles_ids': fields.one2many('doctor.hc.control', 'attentiont_id', u'Controles', readonly=True),
	}

	def default_get(self, cr, uid, fields, context=None):

		res = super(doctor_attention_resumen_inherit,self).default_get(cr, uid, fields, context=context)

		modelo_buscar = self.pool.get('doctor.hc.control')
		paciente_id = context.get('patient_id')
		Controles_ids = []
		if paciente_id:
			ids_ultimas_historias = modelo_buscar.search(cr, uid, [('patient_id', '=', paciente_id)], limit=3, context=context)

			for datos in modelo_buscar.browse(cr, uid, ids_ultimas_historias, context=context):
				
				Controles_ids.append((0,0,{'attentiont_id' : datos.attentiont_id.id,
											'patient_id': datos.patient_id.id,
											'asunto': datos.asunto,
											'evolucion': datos.evolucion,
											'date_attention': datos.date_attention}))
			res['Controles_ids'] = Controles_ids
		return res


doctor_attention_resumen_inherit()