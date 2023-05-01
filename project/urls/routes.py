# Need to update this code so that it uses WTF forms rather than the method used in the tutorial
# https://testdriven.io/courses/learn-flask/blueprints/

from . import urls_blueprint
from hashids import Hashids
from flask import current_app, render_template, request, session, flash, redirect, url_for
from project.models import Url
from project import db
from urllib.parse import urlparse
from flask_login import login_required

# from pydantic import BaseModel, validator, ValidationError


@urls_blueprint.route("/")
def index():
    return render_template('urls/index.html')


@urls_blueprint.route("/shorten_url", methods=("GET", "POST"))
@login_required
def shorten_url():
    hashids = Hashids(min_length=4, salt=current_app.config['SECRET_KEY'])

    if request.method == 'POST':
        url = request.form['url']

        if not url:
            flash('The URL is required!')
            return redirect(url_for('urls/shorten_url.html'))

        check_url = urlparse(url)
        if not check_url.scheme:
            url = "//" + url

        new_url = Url(original_url=url)
        db.session.add(new_url)
        db.session.commit()

        url_id = new_url.id
        hashid = hashids.encode(url_id)
        short_url = request.host_url + hashid

        new_url.short_url = short_url
        db.session.commit()

        return render_template('urls/shorten_url.html', short_url=short_url)

    return render_template('urls/shorten_url.html')


@urls_blueprint.route('/<id>')
def url_redirect(id):
    hashids = Hashids(min_length=4, salt=current_app.config['SECRET_KEY'])

    original_id = hashids.decode(id)
    if original_id:
        original_id = original_id[0]

        url_data = db.session.query(Url).filter_by(id=original_id).first()

        original_url = url_data.original_url

        url_data.clicks = url_data.clicks + 1
        db.session.commit()

        return redirect(original_url)
    else:
        flash('Invalid URL')
        return redirect(url_for('urls.index'))


@urls_blueprint.route('/stats')
@login_required
def stats():
    urls = Url.query.order_by(Url.id).all()
    return render_template('urls/stats.html', urls=urls)

    # db_urls = Url.query.order_by(Url.id).all()

    # urls = []
    # for url in db_urls:
    #     url = dict(url)
    #     url['short_url'] = request.host_url + hashids.encode(url['id'])
    #     urls.append(url)

    return render_template('urls/stats.html', urls=urls)
