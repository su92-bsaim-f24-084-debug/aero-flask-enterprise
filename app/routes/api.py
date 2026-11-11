from flask import Blueprint, jsonify
from app.models import Airport, FlightInstance, Aircraft, db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/health')
def health():
    """Health check endpoint for Render monitoring."""
    return jsonify({
        'status': 'healthy',
        'service': 'aero-flask-enterprise',
        'version': '1.0.0'
    }), 200

@bp.route('/airports')
def get_airports():
    """Returns active airports."""
    airports = Airport.query.filter_by(is_deleted=False).all()
    data = [{
        'id': a.id,
        'name': a.name,
        'iata': a.iata_code,
        'icao': a.icao_code,
        'city': a.city.name,
        'country': a.city.country.name
    } for a in airports]
    return jsonify(data)

@bp.route('/stats')
def get_stats():
    """API metrics for front-end widgets."""
    from app.models import __all__ as model_names
    return jsonify({
        'models_count': len(model_names) - 3,
        'airports': Airport.query.filter_by(is_deleted=False).count(),
        'flights': FlightInstance.query.filter_by(is_deleted=False).count(),
        'aircraft': Aircraft.query.filter_by(is_deleted=False).count()
    })
