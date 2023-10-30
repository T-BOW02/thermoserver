from flask import Flask, request, jsonify
from flask_cors import CORS
import  pymongo
from pymongo.errors import ServerSelectionTimeoutError
app = Flask(__name__)
CORS(app)
client = pymongo.MongoClient(
    "mongodb+srv://TbowLeder:Codons9876@cluster0.r5zgyhj.mongodb.net/?retryWrites=true&w=majority"
)

db = client.thermo
responses_collection = db['thermo']

try:
    client.server_info()
    print("Connexion OK!")
except ServerSelectionTimeoutError as err:
    print(f"Impossible de se connecter à MongoDB: {err}")

# Initialisation des comptages des réponses
initial_counts = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
responses = {i: initial_counts.copy() for i in range(1, 11)}

unique_responses = {}


@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    question_number = data['question_number']
    answer = data['answer']
    user_ip = request.remote_addr

    query = {"ip": user_ip, "question_number": question_number}
    update = {"$set": {"answer": answer}}
    responses_collection.update_one(query, update, upsert=True)

    return jsonify({"message": "Answer saved!"})


@app.route('/results', methods=['GET'])
def get_results():
    aggregate_data = []
    for num in range(1, 11):  # Si vous avez 10 questions
        question_data = {"question_number": num}
        for option in ['a', 'b', 'c', 'd']:
            count = responses_collection.count_documents({"question_number": num, "answer": option})
            question_data[option] = count
        aggregate_data.append(question_data)

    return jsonify(aggregate_data)


if __name__ == '__main__':
    app.run(debug=True, host="192.168.0.27")
