import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginated_questions(questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * (QUESTIONS_PER_PAGE)
    end = start + (QUESTIONS_PER_PAGE)
    paginated = questions[start:end]
    return paginated


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={'/': {'origins': '*'}})
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.get("/categories")
    def get_categories_all():
            categories = Category.query.order_by(Category.id).all()
            my_cat = {}

            for cat in categories:
                my_cat[cat.id] = cat.type

            if len(my_cat) == 0:
                abort(404)

            return jsonify({
                'categories': my_cat,
                'success': True
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
    @app.get('/questions')
    def get_all_questions():
            questions = Question.query.all()
            formatted_questions = [quest.format() for quest in questions]
            paginated_quest = paginated_questions(formatted_questions)

            if len(paginated_quest) == 0:
                abort(404)

            categories = Category.query.all()
            my_cat = {}

            for cat in categories:
                my_cat[cat.id] = cat.type

            return jsonify({
                'success': True,
                'total_questions': len(questions),
                'categories': my_cat,
                'questions': paginated_quest
            })
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.delete('/questions/<int:id>')
    def delete_question(id):
            q = Question.query.filter_by(id=id).one_or_none()
            if q is None:
                abort(404)

            q.delete()
            return jsonify({
                'deleted': id,
                'success': True,
                'total_questions': len(Question.query.all())
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

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.post('/questions')
    def create_a_question():
            body = request.get_json()
            question = body.get('question', None)
            answer = body.get('answer', None)
            difficulty = body.get('difficulty', None)
            category = body.get('category',  None)

            searchTerm = body.get('searchTerm', None)
            try:
                if searchTerm:
                    questions = Question.query.filter(
                        Question.question.ilike(f"%{searchTerm}%")).all()
                    formatted_questions = [quest.format() for quest in questions]
                    paginated_quest = paginated_questions(formatted_questions)

                    return jsonify({
                        'success': True,
                        'questions': paginated_quest,
                        'total_questions': len(paginated_quest)
                    })

                else:
                    q = Question(question=question, answer=answer,
                                 difficulty=difficulty, category=category)
                    q.insert()

                    return jsonify({
                        'success': True,
                        'question_created': q.question,
                        'created': q.id,
                        'total_questions': len(Question.query.all())
                    })
            except:
                abort(422)
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.get('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
            category = Category.query.filter_by(id=category_id).one_or_none()
            if category is None:
                abort(404)
            try:
                questions = Question.query.filter_by(
                    category=category.id).all()
                formatted_questions = [quest.format() for quest in questions]
                paginated_quest = paginated_questions(formatted_questions)

                return jsonify({
                    'success': True,
                    'total_questions': len(Question.query.all()),
                    'current_category': category.type,
                    'questions': paginated_quest
                })

            except:
                abort(400)
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
    @app.post('/play')
    def gamingMethod():
        try:
            body = request.get_json()
            previousQuestions = body.get('previous_questions', None)
            category = body.get('quiz_category', None)

            cat_id = category['id']
            nextQuest = None

            if cat_id != 0:
                game_questions = Question.query.filter_by(category=cat_id).filter(
                    Question.id.notin_((previousQuestions))).all()
            else:
                game_questions = Question.query.filter(
                    Question.id.notin_((previousQuestions))).all()

            if len(game_questions) > 0:
                nextQuest = random.choice(game_questions).format()

            return jsonify({
                'question': nextQuest,
                'success': True,
                })
        except:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 422

    return app
