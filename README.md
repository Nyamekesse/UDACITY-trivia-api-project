# Trivia Fun Game WebApp

Trivia fun game webapp is an online game which aims at creating a bond between people. The trivia WebApp allows its users to test their knowledge by answering some general questions. Users can also delete a question,add a category, add questions of their choice and require that they include answer text. Players can also search for a particular question and play or choose to play randomly.
By playing this game users will be able to gain a lot of knowledge in most interesting fields.

The front end is built with Javascript and backend in Python, both languages follow ES6 and PEP8 style guidelines respectively.
Click to read more about [ES6](https://www.w3schools.com/Js/js_es6.asp) or [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/)

---

## Getting Started

### Pre-requisites and Local Development

As a developer using this project, you should already have Python 3, pip and node installed on your local machines.

- #### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file.

_For Mac / Linux users_

To run the application run the following commands:

```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

_For Windows users_

To run the application run the following commands:

```
set FLASK_APP=flaskr
set FLASK_DEBUG=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. `FLASK_DEBUG` is set to development in order to enable a debug feature which helps in development. You can also look for more commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration.

- #### Frontend

Navigate to the folder named `frontend` and run the following commands to start the client:

_If you are using npm as package manager_

```
npm install // only once to install dependencies
npm start
```

_If you are using yarn as package manager_

```
yarn install // only once to install dependencies
yarn start
```

By default, the frontend will run on localhost:3000.

---

### Tests

In order to run tests navigate to the backend folder, open the terminal and run the following commands:

_For Mac/Linux users_

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

_For Windows users_

```
drop database if exists trivia_test;
create database trivia_test
\i <'type the path to the trivia.psql file'>
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.

---

## API Reference

### Getting Started

- Base URL: Currently trivia app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the trivia application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
```

The API will return five(5) error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 405: MethodNot Allowed
- 500: Internal Server Error

---

### Endpoints

#### GET /api/categories

- General:
  - Returns an object of all categories available and success value.
- Request Arguments: None
- Sample: `curl http://127.0.0.1:5000/api/categories`

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

#### GET /api/questions

- General:
  - Returns an object of questions, available categories, total number of questions, the current category and a success value.
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Request Arguments: None
- Sample: `curl http://127.0.0.1:5000/api/questions`

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
  "current_category": "History",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 18
}

```

#### GET /api/categories/{category_id}/questions

- General:
  - Returns an object of all the questions under the category id specified, the current category and a success value.
- Request Argument: category id
- Sample: `curl http://127.0.0.1:5000/api/categories/3/questions`

```
{
  "currentCategory": "History",
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "totalQuestions": 3
}

```

#### POST /api/questions/new-question

- General:
  - Creates a new questions using the submitted question, answer, category and difficulty. Returns the id of the created question, success value and total questions.
- Request Arguments: An object containing the question, answer, category and difficulty
- Sample: `curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/api/questions/new-question -d '{"question":"What shape is the earth", "answer":"Sphere", "category":3, "difficulty":3}'`

```
{
  "created": 24,
  "success": true,
  "total_questions": 19
}

```

#### POST /api/categories/new-category

- General:
  - Creates a new category using the submitted category type. Returns the id of the created category, success value, the total categories and a list of current categories.
- Request Arguments: category type
- Sample: `curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/api/categories/new-category -d '{"category": "Gaming"}'`

```
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    },
    {
      "id": 7,
      "type": "Gaming"
    }
  ],
  "created": 7,
  "success": true,
  "total_categories": 7
}

```

#### POST /api/questions/search

- General:
  - Endpoint to get questions based on a search term or phrase. Returns all questions that matched the searched term, success value, the current category and total questions that matched the searched term.
- Request Arguments: search Term
- Sample: `curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/api/questions/search -d '{"searchTerm": "country"}'`

```
{
  "current_category": "Sports",
  "questions": [
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "Ghana",
      "category": 4,
      "difficulty": 3,
      "id": 25,
      "question": "Which country is known to be a peaceful country"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

#### POST /api/quizzes

- General:
  - Endpoint to get a single random question using the passed quiz category and a list of previous questions.
  - The returned question will not be in the previous questions list.
  - Returns a single random question at a time and the success value.
- Request Arguments: list of previous questions ids and quiz category
- Sample: `curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/api/quizzes -d '{"previous_questions": [15,14], "quiz_category": {"type":"Science","id":3}}'`

```
{
  "question": {
    "answer": "Lake Victoria",
    "category": 3,
    "difficulty": 2,
    "id": 13,
    "question": "What is the largest lake in Africa?"
  },
  "success": true
}

```

#### DELETE /api/questions/{question_id}

- General:
  - Deletes the question of the given ID if it exists. Returns the id of the deleted book, success value, total questions.
- Request Arguments: question id
- Sample: `curl -X DELETE http://127.0.0.1:5000/api/questions/25`

```
{
  "deleted": 25,
  "success": true,
  "total_questions": 19
}

```

## Deployment N/A

## Authors

Nyamekesse Samuel

## Acknowledgements

The awesome team at Udacity.
