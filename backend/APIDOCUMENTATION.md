# TRIVIA APP API Development and Documentation Final Project

<h2>Endpoints and Methods</h2>

# GET "/categories"

- The endpoint has no arguments.
- Category item is described by ID(Key) and TYPE(Value).
- Returns object of all categories for questions.
- Response is as shown below

  ⚡ "categories": { "1": "Science", "2": "Art", "3": "Geography", "4": "History", "5": "Entertainment", "6": "Sports" }

# GET "/questions"

- The first 10 questions ordered by their id are returned as page 1.
- Questions are paginated with each page containing a maximum of 10 question.
- Returns an object containing a dictionary of all categories by their ID (Key) and TYPE (Value), a list of question dictionaries from the database ordered by their id, and the total number of questions in the records.
- Optional page query parameter can be passed to display the questions for that page.

⚡ "/questions?page=2"

Sample response is as shown below

{ "categories": { "1": "Science", "2": "Art", "3": "Geography", "4": "History", "5": "Entertainment", "6": "Sports" }, "questions": [{ "answer": "One", "category": 2, "difficulty": 4, "id": 18, "question": "How many paintings did Van Gogh sell in his lifetime?" }], "totalQuestions": 27 }

# GET "/categories/int:category_id/questions"

- Returns a JSON object containing the selected category (specified by the id), all questions from that category and the total number in that category.
- Response for category 6 is as shown below
  ⚡ { "currentCategory": "Sports", "questions": [ { "answer": "Brazil", "category": 6, "difficulty": 3, "id": 10, "question": "Which is the only team to play in every soccer World Cup tournament?" }, { "answer": "Uruguay", "category": 6, "difficulty": 4, "id": 11, "question": "Which country won the first ever soccer World Cup in 1930?" }, "totalQuestions": 7 }

Http 404 error is raised if the id is not associated with any category in the database or if the specified category has no question associated with it.

/_ Adding new question _/

# POST "/questions"

- For a "POST" request, a new question can be created and stored in the database with a new ID.
  The request body has to be a dictionary object with all the keys in the sample below.

new question = { "answer": "test question", "category": 1, "difficulty": 4, "question": "test answer" }

-If any of the keys is missing, the user will get the http error 400, bad request.
-The request body MUST be in the exact format of the above sample in order to add a question.
-The response does not return new data to the frontend.

# DELETE "/questions/int:question_id"

- Deletes the question with the specified ID from the database
- No information is returned to the frontend
- 404 error is raised if the id is not associated with any question

/_Searching for questions_/

# POST '/questions' searching for question/s

- A 'POST' request to this endpoint can also be used to search for questions containing a specified character combination
- For a successful search, the request body MUST be the single key dictionary shown below
  search = { "searchTerm" : "title" #replace the value with your search characters }

- The response returns a JSON object of all questions containing the searched characters as shown below and the total number of questions matching the search
  ⚡ { "questions": [ { "answer": "Maya Angelou", "category": 4, "difficulty": 2, "id": 5, "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?" }, { "answer": "Edward Scissorhands", "category": 5, "difficulty": 3, "id": 6, "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?" } ], "totalQuestions": 2 }

# POST "/quizzes"

- Posts a request containing a dictionary of information for questions and category of previous questions from the trivia.

- The response is a JSON object containing information of the next question to be displayed in the game determined by the category specified in the request body, and that is not in the list of the previous questions specified by the request.

- Sample request body and format MUST be as shown below with the keys specified by the exampple. Otherwise, Bad request error is raised

⚡ quiz = { 'previous_questions': [11], 'quiz_category': { 'type': 'Sports', 'id': '6' } }

If the category is non-existent, 404 error is raised.
