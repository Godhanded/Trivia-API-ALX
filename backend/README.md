# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt

```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:
```bash
export FLASK_APP=flaskr
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

## **TRIVIA API-ENDPOINT DOCUMENTATION**
---
<br>
<br>

### **Base Uri**
----
----
The project has not been deployed hence we will make use of on our local server or machine
- **Base Uri:** `localhost:5000` or `localhost:<prefered port>` or `http://127.0.0.1/5000`
the default port is 5000 and has been set as a proxy in the front-end configuration
<br>

### **Error Handling**
----
----
Errors are returned as JSON objects in the following format

```python
{
  "status": 404,
  "success": False,
  "message": "resource not found"
}
```
The API will return 4 error types when requests fail
- 400: Request unprocessable
- 404: resource not found"
- 422: Bad Request
- 500: Internal server error
<br>

### **EndPoints**
----
----
<br>

> `GET '/categories'`

- Fetches a list of dictionaries of all available categories with key of id and value is the string of the corresponding category
- Request Arguements: None
- Returns json object with keys; `success`, `status`, `categories`. where categories is an object

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "status": 200
}
```

---
<br>

> `GET '/questions?page=${integer}'`

- Fetches paginated trivia questions, their categories and total number of questions available
- Request Arguements: `page`-integer
- Returns: a JSON object containing 10 `questions` per page, `total_questions`, all `categories` and `current_category`

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 2
    },
  ],
  "total_questions": 100,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": {"2":"Art"},
  "status": 200,
  "successs": true
}
```

---
<br>

> `DELETE '/questions/${id}'`
- Deletes the record of a question based on the id provided if it exists
- Request Arguements: `id`- integer
-Returns: JSON object containing `status`,`question_id` and `success`

```json
{
  "status": "success",
  "question_id": 5,
  "success": true
}
```

---
<br>

> `POST '/questions'`
- Creates a new Record of a trivia question based on arguements provided from JSON data, all arguements must be provided
- Request Arguements: JSON object containing 
```json
{
  question: "your question",
  answer: "your answer",
  difficulty: 5,
  category: 8
} 
```
*note:* category takes an id-integer and difficulty  an integer always between 1-5
- Returns: `status` and `success`
```json
{
  "status": 200,
  "success": true
}
```

---
<br>

> `POST '/questions/searchterm'`

- Performs a partial search of all quesions based on searchterm provided
- Request Arguements: a JSON object containing
```json
{
  searchTerm: "your search"
}
```
- Returns: Json object containing array of `questions`,`status`,`success`, `total_questions` and `current_category`
```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 5
    }
  ],
  "total_questions": 100,
  "current_category": {"7":"Entertainment"},
  "status": 200,
  "success": true
}
```

---
<br>

> `GET '/categories/${id}/questions'`

- Fetches all questions with category as the categr0y id provided
- Request Arguements: `id`- integer 
- Returns: `success`, `status`, array of `questions`, `total_questions`, `current_category` object
```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 4
    }
  ],
  "totalQuestions": 100,
  "currentCategory": {"3":"History",},
  "status": 200,
  "succes": true
}
```
---
<br>

> `POST '/quizzes'`
- Fetches one random questions that has not been repeated before and based on category provided
- Request Arguements: Json object containg
```json
{
  "previous_questions": [1,3,5],
  "quize_category": "current category id"
}
```
- Returns: one `question` object, `status`and `success`
```json
{
  "question": {
    "id": 1,
    "question": "This is a question",
    "answer": "This is an answer",
    "difficulty": 5,
    "category": 4
  },
  "status": 200,
  "success": true
}
```
---
<br>
<br>


## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
