from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)


score_cards = {
    1: {
        'user_id': 1,
        'course_id': 123,
        'score_card': [4, 5, 3, 4, 4, 5, 3, 4, 4, 5, 4, 3, 4, 4, 0, 0, 0, 0],},
    2: {
        'user_id': 2,
        'course_id': 123,
        'score_card': [5, 6, 4, 5, 5, 6, 4, 5, 5, 6, 5, 4, 5, 5, 0, 0, 0, 0],},
    3: {
        'user_id': 3,
        'course_id': 123,
        'score_card': [3, 4, 2, 3, 3, 4, 2, 3, 3, 4, 3, 2, 3, 3, 0, 0, 0, 0],},
    4: {
        'user_id': 4,
        'course_id': 123,
        'score_card': [6, 7, 5, 6, 6, 7, 5, 6, 6, 7, 6, 5, 6, 6, 0, 0, 0, 0],},
    5: {
        'user_id': 1,
        'course_id': 12,
        'score_card': [6, 7, 5, 6, 6, 7, 5, 6, 6, 7, 6, 5, 6, 6, 7, 5, 6, 6],},
}

bp = Blueprint("score_card", __name__, url_prefix="/score_card")

@bp.route('/', methods=['GET'])
def get_all_score_cards():
    return score_cards

@bp.route('/<int:score_card_id>', methods=['GET'])
def get_score_card(score_card_id):
    score_card = score_cards.get(score_card_id)
    if score_card is None:
        return {"error": "Score card not found"}, 404
    return score_card

def get_score_card_by_user_id(user_id):
    #my_dict = {"apple": 1, "banana": 2, "cherry": 3}
    score_cards_by_user_id = []
    for key, value in score_cards.items():
        print(f"{key}: {value.user_id}")

    score_card = score_cards.get(user_id)
    if score_card is None:
        return {"error": "Score card not found"}, 404
    return score_card