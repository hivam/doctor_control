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


class doctor_hc_control(osv.osv):


	_name = 'doctor.hc.control'


	_columns = {	
		'attentiont_id': fields.many2one('doctor.attentions', u'Atención', ondelete='restrict'),
		'patient_id': fields.many2one('doctor.patient', 'Paciente', ondelete='restrict'),
		'date_attention': fields.datetime('Fecha control', required=True, readonly=True),
		'asunto': fields.char('Asunto'),
		'evolucion': fields.text(u'Evolución/control'),

	}

	def create(self, cr, uid, vals, context=None):

		vals = {}
		patient_id = context.get('patient_id')
		vals['patient_id'] = patient_id
		atencion = 0
		_logger.info(context)
		if 'attentiont_id' in context:
			vals['attentiont_id'] = context.get('attentiont_id')
		
		else:
			cita = context.get('tipo_cita_id')

			if cita.lower().find('psicologia') != -1 or cita.lower().find(u'psicología') != -1:
				atencion = self.pool.get('doctor.psicologia').search(cr, uid, [('patient_id', '=', patient_id)], context=context, limit=1)

			if cita.lower().find('medicina') != -1 or cita.lower().find(u'médicina') != -1:
				atencion = self.pool.get('doctor.attentions').search(cr, uid, [('patient_id', '=', patient_id)], context=context, limit=1)

			if cita.lower().find('Riesgo Biologico') != -1:
				atencion = self.pool.get('doctor.atencion.ries.bio').search(cr, uid, [('patient_id', '=', patient_id)], context=context, limit=1)

			

			if atencion[0]:
				vals['attentiont_id']= atencion[0]

		_logger.info(atencion)	
		return super(doctor_hc_control,self).create(cr, uid, vals, context=context)


	_defaults = {
		'date_attention': lambda *a: datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"),
	}


doctor_hc_control()