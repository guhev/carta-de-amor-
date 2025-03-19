from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__, static_folder='static')

love_letter = [
    "Querida Vivian,",
    "Desde o momento em que nos beijamos",
    "naquela noite mágica de 06/04/2024 às 22:46,",
    "meu coração tem batido mais forte por você.",
    "Cada momento ao seu lado é um presente,",
    "e eu não consigo imaginar minha vida sem você.",
    "Você é minha inspiração, minha alegria,",
    "e a razão pela qual eu sorrio todos os dias.",
    "Prometo te amar e te cuidar para sempre.",
    "Com todo meu amor, Gustavo."
]

second_love_letter = [
    "Querida Vivian,",
    "Você é a luz que ilumina meus dias,",
    "a estrela que guia meu caminho.",
    "Cada segundo ao seu lado é uma bênção,",
    "e eu sou eternamente grato por ter você em minha vida.",
    "Seu sorriso é a razão do meu sorriso,",
    "e seu amor é o que me mantém forte.",
    "Prometo te amar incondicionalmente,",
    "e fazer de cada dia uma nova declaração de amor.",
    "Com todo meu amor, Gustavo."
]

stage = 0
lives = 5
level = 1

def get_random_operation():
    operations = ['add', 'subtract', 'multiply', 'divide']
    return random.choice(operations)

def get_question():
    operation = get_random_operation()
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    if operation == 'add':
        question = f"{num1} + {num2}"
        answer = num1 + num2
    elif operation == 'subtract':
        question = f"{num1} - {num2}"
        answer = num1 - num2
    elif operation == 'multiply':
        question = f"{num1} * {num2}"
        answer = num1 * num2
    elif operation == 'divide':
        num1 = num1 * num2  # Ensure num1 is divisible by num2
        question = f"{num1} / {num2}"
        answer = num1 / num2
    return question, answer

@app.route('/')
def index():
    global stage, lives, level
    if level == 2:
        return render_template('level2_menu.html', love_letter=love_letter)
    if stage >= 10:
        return render_template('complete.html', love_letter=love_letter)
    question, answer = get_question()
    return render_template('index.html', stage=stage, question=question, answer=answer, love_letter=love_letter[:stage], lives=lives)

@app.route('/answer', methods=['POST'])
def answer():
    global stage, lives, level
    user_answer = request.form.get('answer')
    correct_answer = request.form.get('correct_answer')
    
    try:
        user_answer = float(user_answer)
        correct_answer = float(correct_answer)
    except ValueError:
        return redirect(url_for('index'))
    
    if user_answer == correct_answer:
        stage += 1
        if stage >= 10:
            level = 2
    else:
        lives -= 1
        if lives == 0:
            stage = 0
            lives = 5
    
    return redirect(url_for('index'))

@app.route('/level2', methods=['POST'])
def level2():
    global stage, lives, level
    hearts_clicked = int(request.form.get('hearts_clicked', 0))
    alliances_collected = int(request.form.get('alliances_collected', 0))
    if hearts_clicked < 0:
        stage = 0
        lives = 5
        level = 1
        return redirect(url_for('index'))
    if hearts_clicked >= 50 or alliances_collected >= 2:
        return render_template('final.html', love_letter=love_letter, second_love_letter=second_love_letter)
    return redirect(url_for('index'))

@app.route('/start_level2', methods=['POST'])
def start_level2():
    return render_template('level2.html')

if __name__ == '__main__':
    app.run(debug=True)
