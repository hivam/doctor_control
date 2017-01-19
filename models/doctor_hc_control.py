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
		'asunto': fields.char('Asunto'),
		'evolucion': fields.text(u'Evolución/control'),

	}

	def create(self, cr, uid, vals, context=None):
		_logger.info(vals)
		vals['patient_id'] = context.get('patient_id')
		vals['attentiont_id'] = context.get('attentiont_id')
		return super(doctor_hc_control,self).create(cr, uid, vals, context=context)



doctor_hc_control()