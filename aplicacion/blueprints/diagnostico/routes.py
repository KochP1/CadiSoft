from flask import Blueprint, jsonify, session, request, current_app
from flask_login import current_user
import datetime

diagnostico = Blueprint('diagnostico', __name__)

@diagnostico.route('/debug/detailed')
def debug_detailed():
    """Endpoint de diagnóstico completo"""
    
    # Información del usuario actual
    user_info = {
        'is_authenticated': current_user.is_authenticated,
        'user_id': current_user.get_id() if current_user.is_authenticated else None,
        'user_rol': getattr(current_user, 'rol', None) if current_user.is_authenticated else None,
        'user_cedula': getattr(current_user, 'cedula', None) if current_user.is_authenticated else None,
    }
    
    # Información de la sesión Flask
    session_info = {
        'session_keys': list(session.keys()),
        'session_id': session.get('_id', 'No _id en session'),
        '_fresh': session.get('_fresh', 'No _fresh'),
        '_permanent': session.get('_permanent', 'No _permanent'),
        'user_id': session.get('_user_id', 'No _user_id en session'),
    }
    
    # Información de cookies
    cookies_info = {
        'all_cookies': list(request.cookies.keys()),
        'has_session_cookie': 'session' in request.cookies,
        'has_remember_cookie': 'remember_token' in request.cookies,
        'session_cookie_length': len(request.cookies.get('session', '')),
        'remember_cookie_length': len(request.cookies.get('remember_token', '')),
    }
    
    # Información de la request
    request_info = {
        'user_agent': request.headers.get('User-Agent'),
        'remote_addr': request.remote_addr,
        'host': request.host,
        'url': request.url,
        'method': request.method,
        'timestamp': datetime.datetime.now().isoformat(),
    }
    
    return jsonify({
        'user': user_info,
        'session': session_info,
        'cookies': cookies_info,
        'request': request_info,
        'current_app_config': {
            'session_cookie_name': current_app.config.get('SESSION_COOKIE_NAME'),
            'remember_cookie_name': current_app.config.get('REMEMBER_COOKIE_NAME'),
            'secret_key_set': bool(current_app.config.get('SECRET_KEY')),
        }
    })

@diagnostico.route('/debug/clear')
def debug_clear():
    """Limpiar toda la sesión"""
    session.clear()
    return jsonify({'status': 'session cleared'})

@diagnostico.route('/debug/set-test')
def debug_set_test():
    """Establecer valores de prueba en la sesión"""
    session['test_value'] = f"test_{datetime.datetime.now().isoformat()}"
    session['test_user_agent'] = request.headers.get('User-Agent')
    session.modified = True
    return jsonify({'status': 'test values set', 'test_value': session['test_value']})

@diagnostico.route('/health')
def health():
    return jsonify({
        'message': 'ping a la app'
    }), 200