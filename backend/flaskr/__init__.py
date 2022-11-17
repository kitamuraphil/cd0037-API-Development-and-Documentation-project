import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate(question_list):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  page_questions = question_list[start:end]
  return page_questions

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
    @app.route("/categories", methods=["GET"])
    def get_all_categories():
      cats = Category.query.all()
      cats = {cat.id : cat.type for cat in cats}
      return jsonify ({
        "success" : True,
        "categories": cats
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
    @app.route('/questions', methods=['GET'])
    def get_all_questions():
      page = request.args.get('page', 1, type=int)
      start = (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE

      questions = Question.query.order_by(Question.id).all()
      questions = [q.format() for q in questions]

      page_questions = paginate(questions)

      cats = Category.query.all()
      cats = {cat.id : cat.type for cat in cats}


      if len(page_questions) == 0:
        abort(404)
      else:
       return jsonify({
        "success" : True,
        "questions": page_questions,
        "totalQuestions": len(questions),
        "categories" : cats,
       
      })
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def get_question_by_id(question_id):
      question = Question.query.get(question_id)
      if question:
        question.delete()
        return jsonify ({
          "success": True,
          "message" : "question deleted"
           })
      else:
       abort(404)
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
    @app.route('/questions', methods=['POST'])
    def add_and_search_question():
     try:
      body = request.get_json()
      search = body.get('searchTerm', None)
      q = body.get('question', None)
      ans = body.get('answer', None)
      diff = body.get('difficulty', None)
      cat = body.get('category', None)
     except:
      body = None

     if body:
      if search:
        questions = Question.query.filter(Question.question.ilike(f'%{search}%')).all()
        result = [qn.format() for qn in questions]
        if len(result) == 0:
          abort(404)
        else:
          return jsonify ({
            "success" : True,
            "questions" : result,
            "totalQuestions" : len(questions),
            # "currentCategory" : None
            })
      else:
        info = [q, ans, diff, cat]
        if None in info:
            abort(400)
        else:
          new_q = Question(question=q, answer=ans, category=cat, difficulty=diff)

          try:
            new_q.insert()
            return jsonify({
              "success" : True,
              "message" : "question added"
              })
          except:
            db.session.rollback()
            traceback.print_exc()
            abort(500)
     else:
      abort(400)
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
      questions = Question.query.filter_by(category=category_id).all()
      result = [q.format() for q in questions]

      if result:
       cat = Category.query.filter_by(id=category_id).first().type
       return jsonify({
        "success" : True,
        "questions" : result,
        "totalQuestions" : len(questions),
        "currentCategory" : cat
        })
      else:
       abort(404)
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
    @app.route('/play', methods=['POST'])
    def play_trivia():
     try:
      body = request.get_json()
      previous_questions = body.get('previous_questions')
      quiz_category = body.get('quiz_category')
      cat_id = quiz_category['id']
     except:
      body = None
    
     if body:
      if cat_id == 0:
        quizz = Question.query.all()
      elif cat_id in ['1','2','3','4','5','6']:
        quizz = Question.query.filter_by(category=cat_id).all()
      else:
        quizz = None
      
      if quizz:
        quizz_ids = [q.id for q in quizz]

        coming = [q_id for q_id in quizz_ids if q_id not in previous_questions]

        next_id = random.choice(coming)
        next_q = Question.query.filter_by(id=next_id).first()

        return jsonify({
          "success" : True,
          "question" : next_q.format()
          })
      else:
        abort(404)

     else:
      abort(400)

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
