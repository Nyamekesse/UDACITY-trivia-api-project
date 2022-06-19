import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from random import randint


from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_display(selected_questions):
    """method to return number of question per page"""
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    return [single_question.format() for single_question in selected_questions[start:end]]


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

    # endpoint to get all categories
    @app.route('/api/categories', methods=['GET'])
    def get_all_categories():
        try:
            # get all categories in a list format
            all_categories = [
                category.format() for category in Category.query.order_by(Category.id).all()]

            return jsonify({
                'success': True,
                # zip a list of category ids and category type
                'categories': dict(zip([i.get('id') for i in all_categories], [i.get('type') for i in all_categories]))
            })
        except:
            abort(404)

   # endpoint to get paginated question
    @app.route('/api/questions', methods=['GET'])
    def get_all_questions():
        try:
            all_categories = [
                category.format() for category in Category.query.order_by(Category.id).all()]
            grab_questions = Question.query.order_by(Question.id).all()
            if len(all_categories) == 0:
                abort(404)
            else:
                questions = paginate_display(
                    grab_questions) if paginate_display(
                    grab_questions) else abort(400)
                return jsonify({
                    'success': True,
                    'questions': questions,
                    'total_questions': len(questions),
                    'categories': dict(zip([i.get('id') for i in all_categories], [i.get('type') for i in all_categories])),
                    'current_category': 'History'
                })
        except:
            abort(400)

    # end point to delete a single question
    @app.route('/api/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
            question = Question.query.filter(Question.id == id).one_or_none()
            if question == None:
                abort(404)
            else:
                question.delete()
                return jsonify({
                    'success': True
                })
        except:
            abort(422)

    # end point to create a new question
    @app.route('/api/questions/new-question', methods=['POST'])
    def create_new_question():
        body = request.get_json()
        if body.get('question') == '' or body.get('answer') == '' or body.get('category') == '' or body.get('difficulty') == '':
            abort(422)
        else:
            try:
                new_question = Question(question=body.get('question'), answer=body.get(
                    'answer'), category=body.get('category'), difficulty=body.get('difficulty')).insert()
                get_all_current_questions = Question.query.order_by(
                    Question.id).all()
                paginated_question = paginate_display(
                    get_all_current_questions)
                return jsonify({
                    'success': True,
                    'question': paginated_question
                })
            except:
                abort(422)

    # end point to search for a question
    @app.route('/api/questions/search', methods=['POST'])
    def get_question_by_search():
        # get search word/phrase
        searchTerm = request.get_json().get('searchTerm', None)
        # if none abort 422
        if searchTerm == None:
            abort(400)
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
            abort(404)

    # end point to a single random question

    @app.route('/api/quizzes', methods=['POST'])
    def get_random_question():
        body = request.get_json()
        previous_questions = body.get('previous_questions')
        quiz_category = body.get('quiz_category')
        print(previous_questions)
        if previous_questions == [] or quiz_category == None:
            abort(422)
        else:
            try:
                if quiz_category.get('id') == 0:
                    questions = [question.format()
                                 for question in Question.query.all()]
                else:
                    questions = [question.format()
                                 for question in Question.query.filter(Question.category == quiz_category).all()]
                # generate a random number within the range of
                # the list returned by getting the size of the list
                random_number = randint(0, len(questions)-1)
                # grab a random question using the generated number
                random_question = questions[random_number]
                while(random_question.get('id') not in previous_questions):
                    return jsonify({
                        'success': True,
                        'question': random_question
                    })
                random_question = None
                return jsonify({"success": False, "question": random_question})

            except:
                abort(404)

    @app.route('/api/categories/new-category', methods=['POST'])
    def create_new_category():
        body = request.get_json()
        if body.get('category') == '':
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
                abort(422)
    # error handlers

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(500)
    def internal_Server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    return app
