from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# Initialisation des comptages des réponses
initial_counts = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
responses = {i: initial_counts.copy() for i in range(1, 11)}

unique_responses = {}

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    question_number = data['question_number']
    answer = data['answer']
    user_ip = request.remote_addr  # Utilisation de l'adresse IP comme identifiant unique

    # Si l'utilisateur a déjà répondu
    if user_ip in unique_responses:
        previous_answer = unique_responses[user_ip].get(question_number)
        if previous_answer:
            responses[question_number][previous_answer] -= 1  # décrémenter l'ancienne réponse
    else:
        unique_responses[user_ip] = {}

    # Enregistrez la nouvelle réponse et incrémentez le compteur
    unique_responses[user_ip][question_number] = answer
    responses.setdefault(question_number, {'a': 0, 'b': 0, 'c': 0, 'd': 0})[answer] += 1

    return jsonify({"message": "Answer saved!"})


@app.route('/results', methods=['GET'])
def get_results():
    print(responses)
    return jsonify(responses)

if __name__ == '__main__':
    app.run(debug=True, host="192.168.0.27")
