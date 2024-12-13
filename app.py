from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'


# static data for the individual quizzes
quiz_data = {
    "lineups": {
        "question": "Name the Real Madrid team who played against Atletico Madrid in the 2014 Champions League Final",
        "answers": [
            "Casillas", "Carvajal", "Varane", "Ramos", "Coentrao", 
            "Modric", "Khedira", "Di Maria", "Bale", "Benzema", "Ronaldo"
        ]
    },
    "top10": {
        "question": "Name the top 10 scorers in the Premier League for Manchester United",
        "answers": [
            "Shearer", "Kane", "Rooney", "Cole", "Aguero", 
            "Lampard", "Henry", "Salah", "Fowler", "Defoe"
        ]
    }
}

# list of premier league players
prem_players = {"Haaland", "Foden", "Rashford", "De Bruyne", "Hojlund", "Antony", "Zirkzee", "De Ligt", "Onana", "Salah", "Nunez"}

# home/index page 
@app.route('/')
def home():
    return render_template('index.html')
    
# accessibility 
@app.route('/accessibility')
def accessibility():
    return render_template('accessibility.html')

# Lineups 
@app.route('/lineups', methods=['GET', 'POST'])
def lineups():
    if request.method == 'POST':
        user_answer = request.form.get('answer').strip()
        correct_answers = quiz_data['lineups']['answers'] 

        answer_index = next((i for i, answer in enumerate(correct_answers) if answer.lower() == user_answer.lower()), -1)
        
        if answer_index != -1:
            return jsonify({"result": "Correct!", "index": answer_index, "player": correct_answers[answer_index]}) # response when right
       
        return jsonify({"result": "Incorrect. Try again!"}) # response when wrong

    return render_template('lineups.html', question=quiz_data['lineups']['question'])


# top 10
@app.route('/top10', methods=['GET', 'POST'])
def top10():
    # Handles the Top 10 Quiz
    if request.method == 'POST':
        user_answer = request.form.get('answer').strip()  # users answer from the website
        correct_answers = quiz_data['top10']['answers']  # retrieves the list of correct answers from above

        
        answer_index = next((i for i, answer in enumerate(correct_answers) if answer.lower() == user_answer.lower()), -1) # checks lower case list of answers against the users answer also made lower case
        
        if answer_index != -1:
            return jsonify({"result": "Correct!", "index": answer_index, "player": correct_answers[answer_index]}) # response when right
        
        return jsonify({"result": "Incorrect. Try again!"}) # response when wrong

    return render_template('top10.html', question=quiz_data['top10']['question'])

 # multiplayer
@app.route('/multiplayer', methods=['GET', 'POST'])
def multiplayer():
   
    if request.method == 'POST':
        guessed_player = request.form.get('player').strip()  # Retrieve user input
        guessed_players = session.get('guessed_players', [])  # Retrieve the current guessed players list from the session

        if guessed_player.lower() in [p.lower() for p in guessed_players]:
            return jsonify({"result": "You have guessed them already!", "guessed_players": guessed_players})

        # Check if the guessed player is in the predefined list of players
        if guessed_player.lower() in [p.lower() for p in prem_players]:
            guessed_players.append(guessed_player)  # adds the player the user just guessed to the list
            session['guessed_players'] = guessed_players  # updates the list of guessed players
            return jsonify({"result": "Correct!", "guessed_players": guessed_players}) # response when right

        
        return jsonify({"result": "Incorrect!", "guessed_players": guessed_players}) # response when wrong

    session['guessed_players'] = []
    return render_template('multiplayer.html')

if __name__ == '__main__':
    app.run(debug=True)
