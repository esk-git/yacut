import random

from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import YacutForm
from .models import URLMap
from settings import ALLOWED_CHARACTERS, MAX_ATTEMPTS_CREATE_AUTO_SHORT_ID, AUTO_SHORT_ID_LENGTH


def get_unique_short_id():
    attempt = 0
    while True:
        attempt += 1
        if attempt > MAX_ATTEMPTS_CREATE_AUTO_SHORT_ID:
            break
        short_id = ''.join(
            random.choices(ALLOWED_CHARACTERS, k=AUTO_SHORT_ID_LENGTH)
        )
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = YacutForm()
    if form.validate_on_submit():
        original = form.original_link.data
        custom_id = form.custom_id.data
        existing_link = URLMap.query.filter_by(original=original).first()
        if URLMap.query.filter_by(short=custom_id).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('yacut.html', form=form)
        if custom_id is None or custom_id == '':
            custom_id = get_unique_short_id()
        if existing_link:
            short_url = url_for('index_view', _external=True) + existing_link.short
        else:
            link = URLMap(
                original=original,
                short=custom_id
            )
            db.session.add(link)
            db.session.commit()

            short_url = url_for('index_view', _external=True) + link.short
        return render_template('yacut.html', form=form, short=short_url)

    return render_template('yacut.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_view(short):
    url = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url.original)
