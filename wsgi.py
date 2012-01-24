#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for, request
import config
from gily.models import Wiki

app = Flask(__name__)
app.config.from_object(config)
wiki = Wiki(
        app.config['REPOSITORY'],
        app.config['FILE_EXTENSION'],
        app.config['HOMEPAGE']
        )


@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))


@app.route('/')
def toppage():
    try:
        data = wiki.find(wiki.homepage)
        return render_template('page.html', page=data)
    except PageNotFound, notfound:
        return redirect(url_for('edit_page', page=wiki.homepage))


@app.route('/pages')
def index_page():
    pages = wiki.find_all()
    return render_template('pages.html', pages=pages)


@app.route('/<page>/edit')
def edit_page(page):
    data = wiki.find_or_create(page)
    return render_template('edit.html', page=data)


@app.route('/<page>', methods=['GET'])
def view_page(page):
    try:
        data = wiki.find(page)
        return render_template('page.html', page=data)
    except PageNotFound, notfound:
        return redirect(url_for('edit_page', page=page))


@app.route('/<page>', methods=['POST'])
def update_page(page):
    data = wiki.find_or_create(page)
    body = request.form.get('body', '')
    data.content = body

    return redirect(url_for('view_page', page=page))

application = app


def main():
    application.run(debug=True)


if __name__ == '__main__':
    main()
