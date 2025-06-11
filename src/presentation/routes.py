from src.main.composers.DiagnosticGeneratorComposer import diagnostic_generator_composer
from src.errors.error_handler import error_handler

from flask import Blueprint, request, jsonify

diagnostic_creation_bp = Blueprint('diagnostic_creation_bp', __name__)

@diagnostic_creation_bp.route('/', methods= ['POST'])
async def diagnose():
    try:
        controller_handle = diagnostic_generator_composer()
        http_response = await controller_handle(request)
    except Exception as e:
        http_response = error_handler(error= e)

    return jsonify(http_response.body), http_response.status_code