# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code.

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

## API Endpoints

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.



#### 1. POST '/questions'
- Description: Adds a question to the database
- Request Arguments: <string> question, <string> answer, <string> difficulty, <string> category
- Returns: An object with a single key, success.

    - **success**: boolean value

##### Sample Request
```
curl -X POST -H "Content-Type: application/json" -d '{"question": "Did this question do what it should?","answer": "I hope so","category": 5,"difficulty": 2}' http://127.0.0.1:5000/questions

```

##### Sample Response
```
{
  "success": true
}

```

#### 2. POST '/questions'
- Description: Searches questions that include the search term
- Request Arguments: <string> searchTerm
- Returns: An object with four key:value pairs.

    - **current_category**: list of categories of questions with search term in them
    - **questions**: list of Question objects
    - **success**: boolean value
    - **total_questions**: integer number of returned questions

##### Sample Request
```
curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "title"}' http://127.0.0.1:5000/questions

```

##### Sample Response
```
{
  "current_category": [
    4,
    5
  ],
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 2
}

```

#### 3. GET '/questions?page=<int:pageNum>'
- Description: Request pagination
- Request Arguments: <int> pageNum
- Returns: An object with four key:value pairs.

    - **current_category**: random category choosen from page list
    - **questions**: list of Question objects for requested page
    - **success**: boolean value
    - **total_questions**: integer number of all questions

##### Sample Request
```
curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "title"}' http://127.0.0.1:5000/questions

```

##### Sample Response
```
{
  "current_category": [
    4,
    5
  ],
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 2
}

```

#### 4. GET '/categories'
- Description: Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.

  - **categories**: dict of category ids and types formatted for the frontend
  - **success**: boolean value


##### Sample Request
```
curl http://127.0.0.1:5000/categories
```

##### Sample Response
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}

```

#### 5. GET '/categories/\<int:category_id>/questions'
- Description: Fetches questions based on category.
- Request Arguments: <int> category_id  
- Returns: A list of question objects, success status, and total number of category questions.

    - **current_category**: id of the current category
    - **questions**: list of all question objects of a specific category
    - **success**: boolean value
    - **total_questions**: number of questions in the category

##### Sample Request
```
curl http://127.0.0.1:5000/categories/2/questions
```

##### Sample Response
```
"current_category": 2,
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    ....
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 3
}

```

#### 6. DELETE '/questions/\<int:question_id>/'
- Description: Deletes a question based on its question id.
- Request Arguments: <int> question_id
- Returns: A list of question objects, success status, and total number of category questions.

    - **success**: boolean value

##### Sample Request
```
curl http://127.0.0.1:5000/questions/8
```

##### Sample Response
```
{
  "success": true
}

```

#### 7. POST '/quizzes'
- Description: Gets quizzes Deletes a question based on its question id.
- Request Arguments: <list> previous_questions, <int,string> quiz_category  
- Returns: A list of question objects, success status, and total number of category questions.

    - **questions**: list of all question objects of a specific category
    - **success**: boolean value


##### Sample Request
```
curl -X POST -H "Content-Type: application/json" -d '{"previous_questions":[], "quiz_category": {"type": "Geography", "id": "3"}}' http://127.0.0.1:5000/quizzes
```

##### Sample Response
```
{
  "question": {
    "answer": "Maya Angelou",
    "category": 4,
    "difficulty": 2,
    "id": 5,
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  },
  "success": true
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
