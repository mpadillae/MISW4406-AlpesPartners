import alpespartners.seedwork.presentacion.api as api
import json
from alpespartners.modulos.afiliaciones.aplicacion.servicios import ServicioCampana
from alpespartners.modulos.afiliaciones.aplicacion.dto import CampanaDTO
from alpespartners.seedwork.dominio.excepciones import ExcepcionDominio

from flask import redirect, render_template, request, session, url_for
from flask import Response
from alpespartners.modulos.afiliaciones.aplicacion.mapeadores import MapeadorCampanaDTOJson
from alpespartners.modulos.afiliaciones.aplicacion.comandos.crear_campana import CrearCampana
from alpespartners.modulos.afiliaciones.aplicacion.queries.obtener_campana import ObtenerCampana
from alpespartners.seedwork.aplicacion.comandos import ejecutar_commando
from alpespartners.seedwork.aplicacion.queries import ejecutar_query

bp = api.crear_blueprint('afiliaciones', '/afiliaciones')

@bp.route('/campana', methods=('POST',))
def crear_campana():
    try:
        session.clear()
        campana_dict = request.json

        map_campana = MapeadorCampanaDTOJson()
        campana_dto = map_campana.externo_a_dto(campana_dict)

        sc = ServicioCampana()
        dto_final = sc.crear_campana(campana_dto)

        return map_campana.dto_a_externo(dto_final)
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/campana-comando', methods=('POST',))
def crear_campana_asincrona():
    try:
        campana_dict = request.json

        map_campana = MapeadorCampanaDTOJson()
        campana_dto = map_campana.externo_a_dto(campana_dict)

        comando = CrearCampana(campana_dto.fecha_creacion, campana_dto.fecha_actualizacion, campana_dto.id, campana_dto.influencers)
        
        # Revise la clase Despachador de la capa de infraestructura
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/campana', methods=('GET',))
@bp.route('/campana/<id>', methods=('GET',))
def dar_campana(id=None):
    if id:
        sc = ServicioCampana()
        map_campana = MapeadorCampanaDTOJson()
        
        return map_campana.dto_a_externo(sc.obtener_campana_por_id(id))
    else:
        return [{'message': 'GET!'}]

@bp.route('/campana-query', methods=('GET',))
@bp.route('/campana-query/<id>', methods=('GET',))
def dar_campana_usando_query(id=None):
    if id:
        query_resultado = ejecutar_query(ObtenerCampana(id))
        map_campana = MapeadorCampanaDTOJson()
        
        return map_campana.dto_a_externo(query_resultado.resultado)
    else:
        return [{'message': 'GET!'}]