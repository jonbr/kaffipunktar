import functools
import json
from pprint import pprint
import pickle

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from .db import get_db
from . import score_card

"""users = {
    1: {'id': 11, 'name': 'Jon Masson', 'email': 'jon@jon.com', 'handicap': 12.3, 'score_cards': [score_card.get_score_card_by_user_id(1)]},
    2: {'id': 22, 'name': 'Arnar Masson', 'email': 'arnar@arnar.com', 'handicap': 32.3, 'score_cards': []},
    3: {'id': 33, 'name': 'Agust Audunsson', 'email': 'agust@agust.com', 'handicap': 16.3},
    4: {'id': 44, 'name': 'Gudjon Tomasson', 'email': 'gudjon@gudjon.com', 'handicap': 22}
}"""


bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route('/', methods=['GET'])
def get_users():
    db = get_db()
    
    users = db.cursor().execute(
        'SELECT id, name, email, password, handicap FROM user'
    ).fetchall()

    return jsonify([dict(user) for user in users]) 


@bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db = get_db()

    user = db.cursor().execute( 
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()

    if user is None:
        return {"error": "User not found"}, 404

    #pprint(dict(user))

    return jsonify(dict(user))


@bp.route('/create', methods=['POST'])
def create_user():
    if request.is_json:
        json_payload = request.get_json()
        db = get_db()
        error = None

        if error is None:
            try:
                db.execute("INSERT INTO user (name, email, password, handicap) VALUES (?, ?, ?, ?)",
                    (json_payload['name'], json_payload['email'], json_payload['password'], json_payload['handicap'])
                )
                db.commit()
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        else:
            return jsonify({"error": "Request must be JSON"}), 400
    
    return jsonify({"message": "JSON data inserted successfully."}), 201