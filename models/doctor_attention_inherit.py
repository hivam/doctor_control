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


class doctor_attention_inherit(osv.osv):


	_name = "doctor.attentions"
	

	_inherit = 'doctor.attentions'


	_columns = {
		'control_ids': fields.one2many('doctor.hc.control', 'attentiont_id', u'Controles',states={'closed': [('readonly', True)]}),
	}

	def historia_control(self, cr, uid, ids, context=None):

		data_obj = self.pool.get('ir.model.data')
		result = data_obj._get_id(cr, uid, 'doctor_control', 'doctor_hc_control_form_view')
		view_id = data_obj.browse(cr, uid, result).res_id

		context['attentiont_id'] = ids[0]
		return {
			'type': 'ir.actions.act_window',
			'name': 'Historia Control',
			'view_type': 'form',
			'view_mode': 'form',
			'res_id': False,
			'res_model': 'doctor.hc.control',
			'context': context or None,
			'view_id': [view_id] or False,
			'nodestroy': False,
			'target': 'new',
			'flags': {'form': {'action_buttons': True}} 
		}


doctor_attention_inherit()