import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

from dotenv import load_dotenv

load_dotenv()
dbpassword = os.environ['PASSWORD']
database_name = os.environ['DBNAME']

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        self.database_path = f"postgresql://postgres:{dbpassword}@localhost:5432/{database_name}"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertTrue(data["categories"])
        self.assertEqual(data["success"], True)
        self.assertEqual(res.status_code, 200)
    
    def test_get_categories_405(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)
        self.assertEqual(data['message'], 'The specified http method is not allowed')
        self.assertEqual(data["success"], False)
        self.assertEqual(res.status_code, 405)



    def test_get_all_questions_default(self):
        res = self.client().get('/questions') 
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertTrue(data['questions'])
        self.assertLessEqual(len(data['questions']), 10)
        self.assertTrue(data['totalQuestions'])

    def test_get_all_questions_in_page(self):
        res = self.client().get('/questions?page=2') 
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertTrue(data['questions'])
        self.assertLessEqual(len(data['questions']), 10)
        self.assertTrue(data['totalQuestions'])

    def test_get_all_questions_404(self):
        res = self.client().get('/questions?page=9') 
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)
        self.assertTrue(data['message'], 'The resource could not be found')



    def test_add_question(self):
        new_q = {
        'question': 'test question6',
        'answer': 'test answer6',
        'difficulty': 4,
        'category': 5
        }
        res = self.client().post('/questions', json=new_q)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], 'question added')

    def test_add_question_incomplete_request_400(self):
        new_q = {
        'question': 'test question2',
        'answer': 'test answer2',
        'difficulty': 1 
        }
        res = self.client().post('/questions', json=new_q)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], 'Bad request')

    def test_add_question_invalid_request_400(self):
        new_q = [
        'question', 'test question2',
        'answer', 'test answer2',
        'difficulty', 1,
        'category', 3, 
        ]
        res = self.client().post('/questions', json=new_q)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertRaises(TypeError) 
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], 'Bad request')



    def test_search_question(self):
        chars = {
        'searchTerm': 'title'
        }
        res = self.client().post('/questions', json=chars)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        

    def test_search_question_invalid_request_400(self):
        chars = [{
        "searchTerm":'title'
        }]
        res = self.client().post('/questions', json=chars)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 400)
        self.assertRaises(TypeError)
        self.assertEqual(data['message'], 'Bad request')
        
    def test_search_question_404(self):
        chars = {
        "searchTerm": "delsyke" 
        }
        res = self.client().post('/questions', json=chars)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'The resource could not be found')


    def test_delete_question(self):
        res = self.client().delete('/questions/46')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data['message'], 'question deleted')

    def test_delete_question_404(self):
        res = self.client().delete('/questions/10000') 
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], 'The resource could not be found')


    def test_get_questions_by_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])

    def test_get_questions_by_category_404(self):
        res = self.client().get('/categories/125/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], 'The resource could not be found')


    def test_play_trivia(self):
        quiz = {
            'previous_questions': [11],
            'quiz_category': {
            'type': 'Sports',
            'id': '6'
            }
        }
        res = self.client().post('/quizzes', json=quiz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_play_trivia_404(self):
        quiz = {
            'previous_questions': [11],
            'quiz_category': {
            'type': 'Soccer', 
            'id': '100' 
            }
        }
        res = self.client().post('/quizzes', json=quiz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The resource could not be found')

    def test_play_trivia_invalid_request_400(self):
        quiz = [{
            'previous_questions': [11],
            'quiz_category': {
            'type': 'Sports', 
            'id': '6'
            }
        }]
        res = self.client().post('/quizzes', json=quiz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')






# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()