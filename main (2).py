
from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session

@app.route('/', methods=['GET', 'POST'])
def game():
    if 'computer_score' not in session:
        session['computer_score'] = 0
    if 'user_score' not in session:
        session['user_score'] = 0
    
    result = None
    user_choice = None
    computer_choice = None
    
    if request.method == 'POST':
        user_input = request.form.get('choice')
        if user_input:
            words = ("Rock", "Paper", "Scissors")
            computer_choice = random.choice(words)
            user_choice = {"R": "Rock", "P": "Paper", "S": "Scissors"}[user_input]
            
            result = determine_winner(user_choice, computer_choice)
            if result == "You won":
                session['user_score'] += 1
            elif result == "Computer won":
                session['computer_score'] += 1
                
    return render_template('index.html', 
                         result=result,
                         user_choice=user_choice,
                         computer_choice=computer_choice,
                         user_score=session['user_score'],
                         computer_score=session['computer_score'])

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "Draw"
    if (user_choice == "Rock" and computer_choice == "Scissors") or \
       (user_choice == "Paper" and computer_choice == "Rock") or \
       (user_choice == "Scissors" and computer_choice == "Paper"):
        return "You won"
    return "Computer won"

@app.route('/reset')
def reset():
    session['computer_score'] = 0
    session['user_score'] = 0
    return redirect(url_for('game'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
