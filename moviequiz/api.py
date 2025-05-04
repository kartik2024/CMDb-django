from flask import Flask, request, jsonify

app = Flask(__name__)


QUIZ_QUESTIONS = [
    {
        'id': 1,
        'question': "What does Andy Dufresne carve on the wall of his prison cell in *The Shawshank Redemption*?",
        'options': ['A chessboard', 'A Bible verse', 'A tunnel', 'A poster of Rita Hayworth'],
        'answer': 'A tunnel'
    },
    {
        'id': 2,
        'question': "In *Interstellar*, what is the name of the planet covered in shallow water and time dilation?",
        'options': ['Miller’s Planet', 'Edmunds’ Planet', 'Mann’s Planet', 'Murph’s Planet'],
        'answer': 'Miller’s Planet'
    },
    {
        'id': 3,
        'question': "In *Oppenheimer*, which equation plays a key symbolic role in the development of the bomb?",
        'options': ['E=mc^2', 'Schrödinger’s Equation', 'Heisenberg’s Uncertainty Principle', 'The Manhattan Equation'],
        'answer': 'E=mc^2'
    },
    {
        'id': 4,
        'question': "Which film has the quote: “I’m gonna make him an offer he can’t refuse”?",
        'options': ['Scarface', 'The Godfather', 'Goodfellas', 'Casino'],
        'answer': 'The Godfather'
    },
    {
        'id': 5,
        'question': "In *The Dark Knight*, who played Harvey Dent / Two-Face?",
        'options': ['Aaron Eckhart', 'Cillian Murphy', 'Tom Hardy', 'Joseph Gordon-Levitt'],
        'answer': 'Aaron Eckhart'
    },
    {
        'id': 6,
        'question': "Which movie ends with the line: “After all, tomorrow is another day”?",
        'options': ['Gone with the Wind', 'Casablanca', 'Citizen Kane', 'The Sound of Music'],
        'answer': 'Gone with the Wind'
    },
    {
        'id': 7,
        'question': "In *Fight Club*, what is the first rule of Fight Club?",
        'options': ['Don’t talk about Fight Club', 'No shirts', 'First rule is obey the second rule', 'No shoes allowed'],
        'answer': 'Don’t talk about Fight Club'
    },
    {
        'id': 8,
        'question': "In *Inception*, what object does Cobb use to check if he’s dreaming?",
        'options': ['A ring', 'A spinning top', 'A photo', 'A coin'],
        'answer': 'A spinning top'
    },
    {
        'id': 9,
        'question': "In *Forrest Gump*, what company does Forrest invest in?",
        'options': ['Apple', 'IBM', 'Microsoft', 'Nike'],
        'answer': 'Apple'
    },
    {
        'id': 10,
        'question': "Which character says “Why so serious?” in *The Dark Knight*?",
        'options': ['Batman', 'Alfred', 'Harvey Dent', 'The Joker'],
        'answer': 'The Joker'
    },
]

@app.route('/get_quiz_questions', methods=['GET'])
def get_quiz_questions():
    questions = QUIZ_QUESTIONS
    
    public_questions = [
        {k: v for k, v in q.items() if k != 'answer'} for q in questions
    ]
    
    return jsonify(public_questions)


@app.route('/evaluate_quiz', methods=['POST'])
def evaluate_quiz():
    submitted_answers = request.json.get('answers', {})


    score = 0
    for q in QUIZ_QUESTIONS:
        qid = str(q["id"])
        correct = q["answer"].strip()
        submitted = submitted_answers.get(qid, "").strip()
        if submitted == correct:
            score += 1

    return jsonify({"score": score, "total": len(QUIZ_QUESTIONS)})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
