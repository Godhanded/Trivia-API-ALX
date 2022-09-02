import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://{}:{}@{}/{}'.format('student','student','localhost:5432', self.database_name)
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
    def test_get_questions(self):
        res= self.client().get("/questions?page=1")
        data= json.loads(res.data)
        self.assertEqual(data["status"],200)
        self.assertTrue(data["success"])
        self.assertEqual(len(data["questions"]),10)

    def test_404_if_cant_get_questions(self):
        res= self.client().get("/questions?page=1000")
        data= json.loads(res.data)
        self.assertEqual(data["status"],404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"],"resource not found")

    def test_create_question(self):
        res= self.client().post("/questions", json={"question":"is python oop?","answer":"yes","difficulty":1,"category":1})
        data= json.loads(res.data)
        self.assertEqual(data["status"],200)
        self.assertTrue(data["success"])

    def test_422_if_cant_create_question(self):
        res= self.client().post("/questions", json={"question":"is python oop?","answer":"yes"})
        data= json.loads(res.data)
        self.assertEqual(data["status"],422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"],"Bad Request")

    def test_delete_question_with_id(self):
        res= self.client().delete("/questions/6")
        data= json.loads(res.data)
        self.assertEqual(data["status"],200)
        self.assertEqual(data["question_id"],6)
        self.assertTrue(data["success"])

    def test_404_if_cant_find_delete_item(self):
        res= self.client().delete("/questions/1000")
        data= json.loads(res.data)
        self.assertEqual(data["status"],404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"],"resource not found")

    def test_search_questions(self):
        res=self.client().post("/questions/searchterm", json={"searchTerm":"title"})
        data=json.loads(res.data)
        self.assertEqual(data["status"],200)
        self.assertTrue(data["total_questions"])

    def test_404_if_search_not_found(self):
        res=self.client().post("/questions/searchterm", json={"searchTerm":"<<<<>"})
        data=json.loads(res.data)
        self.assertEqual(data["status"],404)
        self.assertEqual(data["message"], "resource not found")

    def get_categories(self):
        res= self.client().get("/categories")
        data= json.loads(res.data)
        self.assertEqual(data["status"],200)
        self.assertTrue(data["success"])
    
    # def test_500_if_get_category_fails(self):
    #     res= self.client().post("/categories")
    #     data= json.loads(res.data)
    #     self.assertEqual(data["status"],500)
    #     self.assertFalse(data["success"])
    #     self.assertEqual(data["message"],"Internal server error")

    def test_get_category_questions(self):
        res= self.client().get("/categories/3/questions")
        data= json.loads(res.data)
        self.assertEqual(data["status"],200)
        self.assertTrue(data["success"])
        self.assertTrue(data["total_questions"])

    def test_404_if_category_questions_fail(self):
        res= self.client().get("/categories/10000/questions")
        data= json.loads(res.data)
        self.assertEqual(data["status"],404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"],"resource not found")

    def test_run_quiz(self):
        res= self.client().post("/quizzes",json={"previouse_questions":[1,2,3],"quize_category":{"id":3,"type":"title"}})
        data= json.loads(res.data)
        self.assertEqual(data["status"],200)
        self.assertTrue(data["success"])
        self.assertTrue(data["question"])

    def test_400_if_run_quize_fails(self):
        res= self.client().post("/quizzes",json={"previouse_questions":[1000,2000,3000],"quize_category":{"id":3565,"type":"tithvjh jbhvh56576854le"}})
        data= json.loads(res.data)
        self.assertEqual(data["status"],400)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"],"Request unprocessable")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()