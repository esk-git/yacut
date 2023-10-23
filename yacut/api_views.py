import re
from flask import jsonify, request
from http import HTTPStatus

from settings import PATTERN, SHORT_USER_LENGTH
from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def add_short_url():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса', HTTPStatus.BAD_REQUEST)
    original_url = data.get('url')
    if not original_url:
        raise InvalidAPIUsage('\"url\" является обязательным полем!', HTTPStatus.BAD_REQUEST)
    short_id = data.get('custom_id')
    if short_id:
        if URLMap.query.filter_by(short=short_id).first():
            raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.', HTTPStatus.BAD_REQUEST)
        if len(short_id) > SHORT_USER_LENGTH or not re.match(PATTERN, short_id):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', HTTPStatus.BAD_REQUEST)
    if short_id is None or short_id == '':
        short_id = get_unique_short_id()
    existing_link = URLMap.query.filter_by(original=original_url).first()
    if existing_link:
        return jsonify(existing_link.to_dict()), HTTPStatus.OK
    else:

        link = URLMap(
            original=original_url,
            short=short_id
        )
        db.session.add(link)
        db.session.commit()
    return jsonify(link.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    short_url = URLMap.query.filter_by(short=short_id).first()
    if short_url is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': short_url.original}), HTTPStatus.OK