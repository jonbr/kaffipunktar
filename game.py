from pprint import pprint
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,jsonify
)

from .db import get_db
from . import user
#from . import score_card

games = {
    1: {
        'id': 101, 
        'team_a': {
            'user_one': 1, 'score_card_id': 1,
            'user_two': 2, 'score_card_id': 2,
        }, 
        'team_b': {
            'user_one': 3, 'score_card_id': 3,
            'user_two': 4, 'score_card_id': 4,
        }
    },
    2: {
        'id': 102, 
        'team_a': {
            'user_one': 1, 
            'user_two': 3
        }, 
        'team_b': {
            'user_one': 3, 
            'user_two': 4
        }
    },
}


bp = Blueprint("game", __name__, url_prefix="/game")


@bp.route('/', methods=['GET'])
def get_all_games():
    return games


@bp.route('/<int:game_id>', methods=['GET'])
def get_game(game_id):
    game = games.get(game_id)
    if game is None:
        return {"error": "Game not found"}, 404
    return game


@bp.route('/', methods=['POST'])
def create_game():

    if request.is_json:
        json_payload = request.get_json()
        db = get_db()
        error = None

        if error is None:
            try:
                # Insert game into database
                db.cursor().execute("INSERT INTO game (team_a_user_one, team_a_user_two, team_b_user_one, team_b_user_two) VALUES (?, ?, ?, ?)",
                    (json_payload['team_a']['user_one'], json_payload['team_a']['user_two'],
                     json_payload['team_b']['user_one'], json_payload['team_b']['user_two'])
                )
                db.commit()
            except db.IntegrityError:
                error = f"Database error occurred."
        else:
            return jsonify({"error": error}), 400
    else:
        return jsonify({"error": "Request must be JSON"}), 400
    
    return jsonify({"message": "Game created successfully"}), 201


@bp.route('/types', methods=['POST'])
def create_game_type():
    if request.is_json:
        json_payload = request.get_json()
        db = get_db()
        error = None

        pprint(json_payload)

        if error is None:
            try:
                # Insert game type into database
                db.cursor().execute("INSERT INTO game_type (name, description) VALUES (?, ?)",
                    (json_payload['name'], json_payload['description'])
                )
                db.commit()
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        else:
            return jsonify({"error": error}), 400
    else:
        return jsonify({"error": "Request must be JSON"}), 400
    
    return jsonify({"message": "Game type created successfully"}), 201


@bp.route('/types', methods=['GET'])
def get_game_types():
    db = get_db()
    game_types = db.cursor().execute("SELECT id, name, description FROM game_type").fetchall()
    result = [{"id": gt[0], "name": gt[1], "description": gt[2]} for gt in game_types]
    return jsonify(result)


@bp.route('/types/<int:type_id>', methods=['GET'])
def get_game_type(type_id):
    db = get_db()
    game_type = db.cursor().execute("SELECT id, name, description FROM game_type WHERE id = ?", (type_id,)).fetchone()
    if game_type is None:
        return jsonify({"error": "Game type not found"}), 404
    result = {"id": game_type[0], "name": game_type[1], "description": game_type[2]}
    return jsonify(result)


def team_constructor(team, green_regulation):
    """
    Constructs a team object and adds key 'handicap_sum' and value
    """
    return {"name_one": team[0],
            "handicap_one": team[1], 
            "name_two": team[2], 
            "handicap_two": team[3],
            "regulation_point": 0, 
            "handicap_sum": team[1] + team[3],
            "green_regulation": green_regulation
            }