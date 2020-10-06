import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    CORS(app, resources={r"/*": {"origins": "*"}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE')
        return response

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''

    @app.route('/categories')
    def get_categories():
        try:

            all_categories = Category.query.order_by('id').all()

            formatted_categories={category.id:category.type for category in all_categories}


            return jsonify({
            'success': True,
            'categories': formatted_categories
            })
        except:
            abort(404)

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''

    @app.route('/questions')
    def get_questions():
        try:

            page = request.args.get('page', 1, type=int)
            questions = Question.query.order_by('id').all()

            #page start and stop
            start = (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE
            formatted_questions=[question.format() for question in questions]

            if len(formatted_questions[start:end]) == 0:
                abort(404)

            all_categories = Category.query.order_by('id').all()

            formatted_categories = [category.format()['type'] for category in all_categories]


            return jsonify({
            'success': True,
            'questions': formatted_questions[start:end],
            'total_questions': len(questions),
            'current_category': random.choice(formatted_categories), #return a random category
            'categories': formatted_categories
            })

        except:
            abort(404)

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_questions(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            #delete question from db
            question.delete()

            return jsonify({
            "success": True,
            })

        except:

            abort(422)

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    '''

    @app.route('/questions', methods=['POST'])
    def add_question():
        #get request from the client
        body = request.get_json()

        #get info from the body and if nothing there set it to None
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)
        searchTerm = body.get('searchTerm', None)


        print(searchTerm)

        if searchTerm == None: #no searchTerm just add a new question
            try:

                new_question = Question(question = new_question, answer = new_answer,
                category = new_category, difficulty = new_difficulty)

                new_question.insert()

                return jsonify({
                "success": True
                })

            except:
                abort(400)
        else: #search for term in the questions


            search_results  = search_questions(searchTerm)

            return search_results.data




    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''

    '''PEP8 encourages only having one questions endpoint per HTTP method so I
    turned this to a helper function for the /questions POST endpoint.
    The test still works though'''
    def search_questions(searchTerm):

        try:

            selection = Question.query.filter(Question.question.ilike('%{}%'.format(searchTerm)))

            '''{} are placeholders for python format() in strings.
            Using {} as placeholders lets you insert all arguments in the
            following () w/o having to worry about indexes numbering or naming
            it auto fills each placeholder in the order the args appear
            '''

            formatted_selection=[selected.format() for selected in selection]

            if(len(formatted_selection) != 0):


                return jsonify({
                'success': True,
                'questions': formatted_selection,
                'total_questions':len(formatted_selection), # not sure if it means total all questions or for search results. len(Question.query.all()),
                'current_category': [selected['category'] for selected in formatted_selection]
                })

            else:

                abort(404)



        except:
            abort(404)

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):

        try:

            '''There is no pagination for these questions.
            Would probably need to add that as a secondary
            feature once a question bank grew'''

            questions = Question.query.filter(Question.category == category_id+1).all()

            formatted_questions = [question.format() for question in questions]

            if len(formatted_questions) == 0:
                abort(404)

            return jsonify({
            'success': True,
            'current_category': category_id,
            'total_questions': len(formatted_questions),
            'questions': formatted_questions
            })

        except:
            abort(404)

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''

    @app.route('/quizzes', methods=['POST'])
    def play_quizzes():

        #get request from the client
        body = request.get_json()

        #get info from the body and if nothing there set it to None
        #since getting list from prev_questions instead of object, check for empty list
        prev_questions = body.get('previous_questions', [])
        current_category = body.get('quiz_category', None)

        try:


            if current_category:

                db_questions = Question.query.filter(Question.category == int(current_category['id'])+1).all()

            else:
                #return all questions if category isn't specified
                db_questions = Question.query.all()

            #create a list of questions from db not in previous quesitons
            new_questions = []


            if db_questions:
                #if question isn't in previous_questions then make it an option
                for question in db_questions:
                    if question.id not in prev_questions:
                        new_questions.append(question.format())

                if len(new_questions) != 0:
                    randomQuest = random.choice(new_questions)
                    return jsonify({
                    'success': True,
                    'question': randomQuest
                    })
                else:
                    return jsonify({
                    'success': True,
                    'question': False
                    })
            else:
                abort(422)

        except:
            abort(400)



    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''

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
    def method_not_allowed(error):
        return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
        }), 422


    return app
