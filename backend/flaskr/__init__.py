import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from random import randint


from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {'origins': '*'}})

    # CORS Headers

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,True')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,PATCH')
        return response

    # method to paginate display
    def paginate_display(request, selected_questions):
        """displays the number of questions per page

        Keyword arguments:
        request -- method to get the page number
        selected_questions -- a list of questions from the database
        Return: returns a specific number of items per page
        """

        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        return [single_question.format() for single_question in selected_questions[start:end]]
    # endpoint to get all categories

    @app.route('/api/categories', methods=['GET'])
    def get_all_categories():
        """get all the categories in the database

        Keyword arguments:
        Return: returns a list of categories in a JSON bdy upon successful request
        """

        try:
            # get all categories in a list format
            all_categories = [
                category.format() for category in Category.query.order_by(Category.id).all()]

            return jsonify({
                'success': True,
                # zip a list of category ids and category type
                'categories': dict(zip([values.get('id') for values in all_categories], [values.get('type') for values in all_categories]))
            })
        except:
            abort(405)

   # endpoint to get paginated question
    @app.route('/api/questions', methods=['GET'])
    def get_all_questions():
        """returns all questions in the database, and paginate them

        Keyword arguments:

        Return: a list of questions and categories in the database in a JSON body
        """
        try:
            all_categories = [
                category.format() for category in Category.query.order_by(Category.id).all()]
            grab_questions = Question.query.order_by(Question.id).all()
            if len(all_categories) == 0:
                abort(404)
            else:
                questions = paginate_display(request, grab_questions) if paginate_display(
                    request, grab_questions) else abort(400)
                return jsonify({
                    'success': True,
                    'questions': questions,
                    'total_questions': len(Question.query.all()),
                    'categories': dict(zip([i.get('id') for i in all_categories], [i.get('type') for i in all_categories])),
                    'current_category': 'History'
                })
        except:
            abort(422)

    # end point to delete a single question
    @app.route('/api/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        """delete a single question from a database

        Keyword arguments:
        id -- the id of the question to be deleted
        Return: 200 upon successful request
        """

        try:
            question = Question.query.filter(Question.id == id).one_or_none()
            if question == None:
                abort(404)
            else:
                question.delete()
                return jsonify({
                    'success': True,
                    'deleted': id
                })
        except:
            abort(422)

    # end point to create a new question
    @app.route('/api/questions/new-question', methods=['POST'])
    def create_new_question():
        """add new question record to database

        Keyword arguments:
        json -- contains the question, answer, category and difficulty to be added
        Return: returns 200 upon successful request and a list of paginated questions
        """

        body = request.get_json()
        if body == None:
            abort(422)
        else:
            try:
                new_question = Question(question=body.get('question'), answer=body.get(
                    'answer'), category=body.get('category'), difficulty=body.get('difficulty')).insert()
                get_all_current_questions = Question.query.order_by(
                    Question.id).all()
                paginated_question = paginate_display(request,
                                                      get_all_current_questions)
                return jsonify({
                    'success': True,
                    'question': paginated_question
                })
            except:
                abort(405)

    # end point to search for a question
    @app.route('/api/questions/search', methods=['POST'])
    def get_question_by_search():
        """searches any question matching the search term

        Keyword arguments:
        searchTerm -- the word or phrase to be searched
        Return: returns a list of question or questions upon successful request
        """

        # get search word/phrase
        searchTerm = request.get_json().get('searchTerm')
        # if none abort 422
        if searchTerm == '':
            abort(404)
        else:
            try:
                # query database to get all that match the searched word or phrase
                get_questions = Question.query.order_by(Question.id).filter(
                    Question.question.ilike(f'%{searchTerm}%')).all()
                # return 404 if result is 0
                if len(get_questions) == 0:
                    abort(404)
                else:
                    return jsonify({
                        'success': True,
                        'questions': [question.format() for question in get_questions],
                        'total_questions': len(get_questions),
                        'current_category': 'Sports'
                    })
            except:
                abort(404)

    # end point to get questions per category selected
    @app.route('/api/categories/<int:id>/questions', methods=['GET'])
    def get_questions_per_category(id):
        """returns all questions based on a category

        Keyword arguments:
        id -- id of the category
        Return: category questions
        """

        try:
            questions = Question.query.order_by(
                Question.id).filter(Question.category == id).all()
            if len(questions) == 0:
                abort(404)
            else:
                return jsonify({
                    'success': True,
                    'questions': [question.format() for question in questions],
                    'totalQuestions': len(questions),
                    'currentCategory': 'History'
                })
        except:
            abort(405)

    # end point to a single random question
    @app.route('/api/quizzes', methods=['POST'])
    def get_random_question():
        """displays a single random question, which is not part of a list of previous questions

        Keyword arguments:
        previous_questions -- a list of previous questions ids
        quiz_category -- an object containing type and category id
        Return: returns a single random question
        """

        body = request.get_json()
        previous_questions = body.get('previous_questions')
        quiz_category = body.get('quiz_category')

        if quiz_category.get('id') == '':
            abort(422)
        else:
            try:
                if (quiz_category.get('id') == 0) and (len(previous_questions) >= 0):
                    questions = [question.format()
                                 for question in Question.query.all()]
                elif(quiz_category.get('id') != 0 and (len(previous_questions) >= 0)):
                    questions = [question.format()
                                 for question in Question.query.filter(Question.category == int(quiz_category.get('id'))).all()]
                # generate a random number within the range of
                # the list returned by getting the size of the list
                random_number = randint(0, len(questions)-1)
                # grab a random question using the generated number
                random_question = questions[random_number]
                go_ahead = True     # setting a condition
                # indicates that there are no more questions as soon as the length
                # of questions fetched is equal to the length of the previous question
                # hence should return the score
                if len(previous_questions) == len(questions):
                    go_ahead = False
                    return jsonify({"success": False, "question": False})
                else:
                    while(go_ahead):
                        if(random_question.get('id') in previous_questions):
                            random_number = randint(0, len(questions)-1)
                            random_question = questions[random_number]
                            pass
                        elif(random_question.get('id') not in previous_questions):
                            return jsonify({
                                'success': True,
                                'question': random_question
                            })

                        else:
                            go_ahead = False
                            previous_questions.clear()
                            return jsonify({"success": False, "question": False})

            except:
                abort(404)

    # end point to create a new category
    @ app.route('/api/categories/new-category', methods=['POST'])
    def create_new_category():
        """add new category to the categories

        Keyword arguments:
        json -- contains the category name to be added
        Return: status code 200 if created successfully
        """

        body = request.get_json()
        if body == None:
            abort(422)
        else:
            try:
                new_category = Category(type=body.get('category')).insert()
                get_all_current_categories = [category.format() for category in Category.query.order_by(
                    Category.id).all()]
                return jsonify({
                    'success': True,
                    'categories': get_all_current_categories
                })
            except:
                abort(405)
    # error handlers

    @ app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @ app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @ app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @ app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @ app.errorhandler(500)
    def internal_Server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    return app
