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
from openerp.osv.orm import setup_modifiers
from lxml import etree

class doctor_hc_control(osv.osv):


	_name = 'doctor.hc.control'


	_columns = {	
		'attentiont_id': fields.many2one('doctor.attentions', u'Atención', ondelete='restrict'),
		'patient_id': fields.many2one('doctor.patient', 'Paciente', ondelete='restrict'),
		'date_attention': fields.datetime('Fecha control', required=True, readonly=True),
		'asunto': fields.char('Asunto'),
		'evolucion': fields.text(u'Evolución/control'),
		'diseases_ids': fields.one2many('doctor.attentions.diseases', 'attentiont_control_id', 'Diagnostico', ondelete='restrict'),

		'diganosticos_resumen': fields.text('Diganosticos', readonly=True, store=False),
		'tipo_diagnostico': fields.text('Tipo diagnostico', readonly=True, store=False),
		'tratamiento_resumen': fields.text('Tratamientos', readonly=True, store=False),
		'analisis_resumen': fields.text('Analisis', readonly=True, store=False),
		'review_systems_id': fields.one2many('doctor.review.systems', 'attentiont_id', 'Revision por Sistema', readonly=True, store=False),
		'attentions_past_ids': fields.one2many('doctor.attentions.past', 'attentiont_id', 'Antecedentes',  readonly= True, store=False),
		'pathological_past': fields.one2many('doctor.diseases.past', 'attentiont_id', 'Pathological past', readonly=True, store=False),
		'drugs_past': fields.one2many('doctor.atc.past', 'attentiont_id', 'Drugs past', ondelete='restrict', readonly=True, store=False),
		'drugs_ids': fields.one2many('doctor.prescription', 'attentiont_id', 'Drugs prescription', readonly = True, store=False),
		'notas_confidenciales': fields.text('Notas Confidenciales', readonly=True, store=False),
		'examen_fisico_id': fields.one2many('doctor.attentions.exam', 'attentiont_id', 'Examen Fisico', readonly=True, store=False),
		'motivo_consulta': fields.text('Motivo consulta', readonly=True, store=False),

	}


	def default_get(self, cr, uid, fields, context=None):
		res = super(doctor_hc_control,self).default_get(cr, uid, fields, context=context)

		if 'active_model' in context:

			if context.get('active_model') != 'doctor.attentions':

				modelo_buscar = self.pool.get('doctor.attentions')
				paciente_id = context.get('patient_id')
				resumen_analisis = ''
				tratamiento_resumen = ''
				diagnosticos_resumen = ''
				tipo_diagnosticos_resumen =''
				notas_confidenciales =''
				motivo_consulta = ''
				diagnosticos_ids = []
				revision_por_sistema_ids = []
				antecedentes_ids = []
				antecedentes_patologicos_ids = []
				antecedentes_farmacologicos_ids = []
				medicamentos_ids = []
				examen_fisico = []
				if paciente_id:
					ids_ultimas_historias = modelo_buscar.search(cr, uid, [('patient_id', '=', paciente_id)], limit=3, context=context)

					for datos in modelo_buscar.browse(cr, uid, ids_ultimas_historias, context=context):
						
						if datos.analysis:
							resumen_analisis += datos.analysis + '\n'

						if datos.conduct: 
							tratamiento_resumen += datos.conduct + '\n'

						if datos.motivo_consulta: 
							motivo_consulta += datos.motivo_consulta + '\n'

						if uid == datos.professional_id.user_id.id:
							if datos.notas_confidenciales:
								notas_confidenciales += datos.notas_confidenciales
						
						if datos.diseases_ids:
							for i in range(0,len(datos.diseases_ids),1):
								if datos.diseases_ids[i].diseases_id not in diagnosticos_ids:

									if datos.diseases_ids[i].diseases_type == 'main':
										tipo_diagnosticos_resumen += 'Principal' + '\n'
									else:
										tipo_diagnosticos_resumen += 'Relacionado' + '\n'

									diagnosticos_resumen += datos.diseases_ids[i].diseases_id.name + '\n'
									diagnosticos_ids.append(datos.diseases_ids[i].diseases_id)

						if datos.review_systems_id:
							for i in range(0,len(datos.review_systems_id),1):
								_logger.info(datos.review_systems_id[i].review_systems)
								if datos.review_systems_id[i].review_systems:
									revision_por_sistema_ids.append((0,0,{'system_category' : datos.review_systems_id[i].system_category.id,
																		'review_systems': datos.review_systems_id[i].review_systems}))

						if datos.attentions_past_ids:
							for i in range(0,len(datos.attentions_past_ids),1):
								if datos.attentions_past_ids[i].past:
									antecedentes_ids.append((0,0,{'past_category' : datos.attentions_past_ids[i].past_category.id,
																	'past': datos.attentions_past_ids[i].past}))

						if datos.pathological_past:
							for i in range(0,len(datos.pathological_past),1):
								antecedentes_patologicos_ids.append((0,0,{'diseases_id' : datos.pathological_past[i].diseases_id.id}))

						if datos.drugs_past:
							for i in range(0,len(datos.drugs_past),1):
								antecedentes_farmacologicos_ids.append((0,0,{'atc_id' : datos.drugs_past[i].atc_id.id}))

						if datos.drugs_ids:
							for i in range(0,len(datos.drugs_ids),1):
								medicamentos_ids.append((0,0,{'drugs_id' : datos.drugs_ids[i].drugs_id.id}))


						if datos.attentions_exam_ids:
							for i in range(0,len(datos.attentions_exam_ids),1):

								if datos.attentions_exam_ids[i].exam:

									examen_fisico.append((0,0,{'exam_category' : datos.attentions_exam_ids[i].exam_category.id,
																'exam': datos.attentions_exam_ids[i].exam}))
							
					res['analisis_resumen'] = resumen_analisis
					res['tratamiento_resumen'] = tratamiento_resumen
					res['notas_confidenciales'] = notas_confidenciales
					res['diganosticos_resumen'] = diagnosticos_resumen
					res['tipo_diagnostico'] = tipo_diagnosticos_resumen
					res['review_systems_id'] = revision_por_sistema_ids
					res['attentions_past_ids'] = antecedentes_ids
					res['pathological_past'] = antecedentes_patologicos_ids
					res['drugs_past'] = antecedentes_farmacologicos_ids
					res['drugs_ids'] = medicamentos_ids
					res['examen_fisico_id'] = examen_fisico
					res['motivo_consulta'] = motivo_consulta

		return res

	def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
		
		res = super(doctor_hc_control, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
		doc = etree.XML(res['arch'])
		patient_id = context.get('patient_id')
		antecedentes_farmacologicos_ids = []
		revision_por_sistema_ids = []
		antecedentes_patologicos_ids = []
		medicamentos_ids = []
		antecedentes_ids = []
		examen_fisico = []
		motivo_consulta = []
		datos_notas_confidenciales = []
		resumen_analisis = []
		tratamiento_resumen = []
		diagnosticos_resumen= []
		diagnosticos_resumen_tipo= []

		if 'active_model' in context:
			if context.get('active_model') == 'doctor.attentions':
				for node in doc.xpath("//page[@id='resumen']"):
					node.set('invisible', repr(True))
					setup_modifiers(node)
			else:
				record = None
				if patient_id:
					modelo_buscar = self.pool.get('doctor.attentions')
					record = modelo_buscar.search(cr, uid, [('patient_id', '=', patient_id)], limit=3, context=context)

				for node in doc.xpath("//field[@name='notas_confidenciales']"):
						
						if record:
							for datos in modelo_buscar.browse(cr, uid, record, context=context):
								
								if datos.notas_confidenciales:
									datos_notas_confidenciales.append(datos.notas_confidenciales)
								
							if len(datos_notas_confidenciales) <= 0:
								node.set('invisible', repr(True))
								setup_modifiers(node, res['fields']['notas_confidenciales'])

				for node in doc.xpath("//field[@name='motivo_consulta']"):
						
						if record:
							for datos in modelo_buscar.browse(cr, uid, record, context=context):
								
								if datos.motivo_consulta:
									motivo_consulta.append(datos.notas_confidenciales)
								
							if len(motivo_consulta) <= 0:
								node.set('invisible', repr(True))
								setup_modifiers(node, res['fields']['motivo_consulta'])



				for node in doc.xpath("//field[@name='tratamiento_resumen']"):
						
						if record:
							for datos in modelo_buscar.browse(cr, uid, record, context=context):
								
								if datos.conduct:
									tratamiento_resumen.append(datos.conduct)
								
							if len(tratamiento_resumen) <= 0:
								node.set('invisible', repr(True))
								setup_modifiers(node, res['fields']['tratamiento_resumen'])


				for node in doc.xpath("//field[@name='analisis_resumen']"):
						
						if record:
							for datos in modelo_buscar.browse(cr, uid, record, context=context):
								
								if datos.analysis:
									resumen_analisis.append(datos.conduct)
								
							if len(resumen_analisis) <= 0:
								node.set('invisible', repr(True))
								setup_modifiers(node, res['fields']['analisis_resumen'])

					


				for node in doc.xpath("//field[@name='diganosticos_resumen']"):
						
						if record:
							for datos in modelo_buscar.browse(cr, uid, record, context=context):
								if datos.diseases_ids:
									for i in range(0,len(datos.diseases_ids),1):
										diagnosticos_resumen.append(datos.diseases_ids[i].diseases_id.name)
									
								
							if len(diagnosticos_resumen) <= 0:
								node.set('invisible', repr(True))
								setup_modifiers(node, res['fields']['diganosticos_resumen'])



				for node in doc.xpath("//field[@name='tipo_diagnostico']"):
						
						if record:
							for datos in modelo_buscar.browse(cr, uid, record, context=context):
								if datos.diseases_ids:
									for i in range(0,len(datos.diseases_ids),1):
										diagnosticos_resumen_tipo.append(datos.diseases_ids[i].diseases_type)
								
							if len(diagnosticos_resumen_tipo) <= 0:
								node.set('invisible', repr(True))
								setup_modifiers(node, res['fields']['tipo_diagnostico'])




				for node in doc.xpath("//field[@name='drugs_past']"):
						
						if record:
							for datos in modelo_buscar.browse(cr, uid, record, context=context):
								
								if datos.drugs_past:
									for i in range(0,len(datos.drugs_past),1):
										antecedentes_farmacologicos_ids.append(datos.drugs_past[i].atc_id.id)
								
							if len(antecedentes_farmacologicos_ids) <= 0:
								node.set('invisible', repr(True))
								setup_modifiers(node, res['fields']['drugs_past'])

				for node in doc.xpath("//field[@name='review_systems_id']"):
						if record:
							for datos in modelo_buscar.browse(cr, uid, record, context=context):
								for i in range(0,len(datos.review_systems_id),1):
									if datos.review_systems_id[i].review_systems:
										revision_por_sistema_ids.append(datos.review_systems_id[i].review_systems)
							
							if len(revision_por_sistema_ids) <= 0:
								node.set('invisible', repr(True))
								setup_modifiers(node, res['fields']['review_systems_id'])


				for node in doc.xpath("//field[@name='pathological_past']"):
						
						if record:
							for datos in modelo_buscar.browse(cr, uid, record, context=context):
								
								if datos.pathological_past:
									for i in range(0,len(datos.pathological_past),1):
										antecedentes_patologicos_ids.append(datos.pathological_past[i].diseases_id.id)
								
							if len(antecedentes_patologicos_ids) <= 0:
								node.set('invisible', repr(True))
								setup_modifiers(node, res['fields']['pathological_past'])


				for node in doc.xpath("//field[@name='drugs_ids']"):
						
						if record:
							for datos in modelo_buscar.browse(cr, uid, record, context=context):
								
								if datos.drugs_ids:
									for i in range(0,len(datos.drugs_past),1):
										medicamentos_ids.append(datos.drugs_ids[i].drugs_id.id)
								
							if len(medicamentos_ids) <= 0:
								node.set('invisible', repr(True))
								setup_modifiers(node, res['fields']['drugs_ids'])

				for node in doc.xpath("//field[@name='attentions_past_ids']"):
						
						if record:
							for datos in modelo_buscar.browse(cr, uid, record, context=context):
								for i in range(0,len(datos.attentions_past_ids),1):
									if datos.attentions_past_ids[i].past:
										antecedentes_ids.append(datos.attentions_past_ids[i].past)
								
							if len(antecedentes_ids) <= 0:
								node.set('invisible', repr(True))
								setup_modifiers(node, res['fields']['attentions_past_ids'])


				for node in doc.xpath("//field[@name='examen_fisico_id']"):
						
						if record:
							for datos in modelo_buscar.browse(cr, uid, record, context=context):
								for i in range(0,len(datos.attentions_exam_ids),1):
									if (datos.attentions_exam_ids[i].exam):
										examen_fisico.append(datos.attentions_exam_ids[i].exam)
								
							if len(examen_fisico) <= 0:
								node.set('invisible', repr(True))
								setup_modifiers(node, res['fields']['examen_fisico_id'])




		res['arch'] = etree.tostring(doc)
		
		return res

	def create(self, cr, uid, vals, context=None):

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

		return super(doctor_hc_control,self).create(cr, uid, vals, context=context)


	_defaults = {
		'date_attention': lambda *a: datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"),
	}


doctor_hc_control()