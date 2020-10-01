from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
        return render_template('home.html')

@app.route('/about', methods=['POST', 'GET'])
def about():
        return render_template('about.html')

@app.route('/boardgames', methods=['POST', 'GET'])
def games():
        return render_template('boardgames.html')

@app.route('/boardgamegenres', methods=['POST', 'GET'])
def genres():
        return render_template('boardgamegenres.html')

@app.route('/boardgamepublishers', methods=['POST', 'GET'])
def publishers():
        return render_template('boardgamepublishers.html')
if __name__ == "__main__":
    app.run(debug=True)