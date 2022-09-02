from crypt import methods
import json
from logging import error
import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)

    def paginate(request, selection):
        page = request.args.get("page", 1, type=int)
        start = (page - 1)*10
        end = start+10
        questions = [question.format() for question in selection]

        items = questions[start:end]
        return items
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,POST,PATCH,DELETE,OPTIONS"
        )
        response.headers.add(
            "Access-Control-Allow-Origin", "*"
        )
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories", methods=["GET"])
    def get_categories():
        selections = Category.query.order_by(Category.id).all()
        if selections is None:
            abort(500)
        return jsonify({
            "success": True,
            "status": 200,
            "categories": {cat.id: cat.type for cat in selections}
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions", methods=["Get"])
    def get_questions():
        selection = Question.query.all()
        category = Category.query.all()
        items = paginate(request, selection)
        if len(items) == 0:
            abort(404)
        res = dict()
        # new_items=[item.get["question"] for item in items]
        # print (new_items)
        return jsonify({
            "status": 200,
            "success": True,
            "total_questions": len(selection),
            "questions": items,
            "categories": {cat.id: cat.type for cat in category},
            "current_category": None,
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):

        question = Question.query.filter_by(id=question_id).one_or_none()
        if question is None:
            abort(404)
        question.delete()
        return jsonify({
            "status": 200,
            "question_id": question_id,
            "success": True,
        })

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def create_question():
        try:
            question = request.get_json()
            if "question" and "answer" and "difficulty" and "category" in question:
                ask = str(question.get("question"))
                answer = str(question.get("answer"))
                difficulty = int(question.get("difficulty"))
                category = int(question.get("category"))
                question = Question(question=ask, answer=answer,
                                    difficulty=difficulty, category=category)
                question.insert()
                return jsonify({
                    "status": 200,
                    "success": True,
                })
            else:
                abort(422)
        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/questions/searchterm", methods=["POST"])
    def search_questions():
        search_term = request.get_json()
        search_term = search_term.get("searchTerm")
        questions = Question.query.filter(
            Question.question.ilike('%'+search_term+'%')).all()
        if questions == []:
            abort(404)
        print(questions)
        return jsonify({
            "status": 200,
            "success": True,
            "questions": [question.format() for question in questions],
            "total_questions": len(questions),
            "current_category": None
        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:id>/questions", methods=["GET"])
    def get_category_questions(id):
        questions = Question.query.filter(Question.category == id).all()
        if questions is None:
            abort(404)
        formated = [question.format() for question in questions]
        category = Category.query.get(id)
        if category is None:
            abort(404)
        format_cat = category.format()
        print(formated)
        return jsonify({
            "status": 200,
            "success": True,
            "questions": formated,
            "total_questions": len(formated),
            "current_category": format_cat
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=["POST"])
    def run_quiz():
        data = request.get_json()
        prev = data.get("previouse_questions")
        quize_category = data.get("quize_category").get("id")
        # question=Question.query.filter(Question.id.not_in(prev)).join(Category).filter(Category.type.ilike(quize_category)).first()
        categories = Category.query.filter_by(id=quize_category).first()
        if categories is None:
            abort(400)
        print(categories)
        question = Question.query.filter(Question.id.not_in(prev)).filter(
            Question.category == categories.id).first()

        return jsonify({
            "status": 200,
            "success": True,
            "question": question.format(),
        })

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "status": 404,
            "success": False,
            "message": "resource not found"
        })

    @app.errorhandler(400)
    def cant_process(error):
        return jsonify({
            "status": 400,
            "success": False,
            "message": "Request unprocessable"
        })

    @app.errorhandler(422)
    def bad_request(error):
        return jsonify({
            "status": 422,
            "success": False,
            "message": "Bad Request"
        })

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "status": 500,
            "success": False,
            "message": "Internal server error"
        })

    return app
