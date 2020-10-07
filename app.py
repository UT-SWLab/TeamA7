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
        return render_template('genres.html')

@app.route('/boardgamepublishers', methods=['POST', 'GET'])
def publishers():
        return render_template('publishers.html')




@app.route('/RioGrandeGames', methods=['POST', 'GET'])
def RioGrandeGames():
        return render_template('RioGrandeGames.html')


@app.route('/Mattel', methods=['POST', 'GET'])
def Mattel():
        return render_template('Mattel.html')

@app.route('/Hasbro', methods=['POST', 'GET'])
def Hasbro():
        return render_template('Hasbro.html')




if __name__ == "__main__":
    app.run(debug=True)
