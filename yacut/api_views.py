import re
from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id

PATTERN = r'^[A-Za-z0-9]*$'
SHORT_USER_LENGTH = 16


@app.route('/api/id/', methods=['POST'])
def add_short_url():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса', 400)
    original_url = data.get('url')
    if not original_url:
        raise InvalidAPIUsage('\"url\" является обязательным полем!', 400)
    short_id = data.get('custom_id')
    if short_id:
        if URLMap.query.filter_by(short=short_id).first():
            raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.', 400)
        if len(short_id) > SHORT_USER_LENGTH or not re.match(PATTERN, short_id):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', 400)
    if short_id is None or short_id == '':
        short_id = get_unique_short_id()
    existing_link = URLMap.query.filter_by(original=original_url).first()
    if existing_link:
        return jsonify(existing_link.to_dict()), 200
    else:

        link = URLMap(
            original=original_url,
            short=short_id
        )
        db.session.add(link)
        db.session.commit()
    return jsonify(link.to_dict()), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    short_url = URLMap.query.filter_by(short=short_id).first()
    if short_url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': short_url.original}), 200