# -*- coding: utf-8 -*-
import json

from flask import Flask, jsonify, send_from_directory, render_template, redirect, make_response

from flask_app.to_elastic import *

app = Flask(__name__)


@app.route('/')
def start():
    return redirect('/lithuania/api/docs')


@app.route('/lithuania/api/docs')
def swagger_ui():
    return render_template('swagger_ui.html')


@app.route('/spec')
def get_spec():
    return send_from_directory(app.root_path, 'api.yaml')


@app.route('/lithuania/api/<key>')
def embassy(key):
    try:
        if key == 'embassy':
            data = get_res(get_consulates())
        elif key == 'visa-centre':
            data = get_res(get_visa_centers())
        elif key == 'news':
            data = get_res(get_news())
        else:
            return make_response(jsonify({'error': 'Key not found'}), 404)
        if data is None:
            return make_response(jsonify({'error': 'Data not found'}), 404)
        try:
            return jsonify({f'{key}': data})
        except KeyError:
            return make_response(jsonify({'error': 'No content'}), 204)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
