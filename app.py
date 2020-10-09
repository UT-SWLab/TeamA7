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
        return render_template('Board_Games_List.html')

@app.route('/boardgamegenres', methods=['POST', 'GET'])
def genres():
        return render_template('genres.html')

@app.route('/boardgamepublishers', methods=['POST', 'GET'])
def publishers():
        return render_template('Publishers_List.html')


############ ROUTES TO PUBLISHERS ############

@app.route('/RioGrandeGames', methods=['POST', 'GET'])
def RioGrandeGames():
        return render_template('RioGrandeGames.html')

@app.route('/Mattel', methods=['POST', 'GET'])
def Mattel():
        return render_template('Mattel.html')

@app.route('/Hasbro', methods=['POST', 'GET'])
def Hasbro():
        return render_template('Hasbro.html')


############ ROUTES TO GAMES ############

@app.route('/ApplestoApples', methods=['POST', 'GET'])
def ApplestoApples():
        return render_template('Apples_to_Apples.html')


@app.route('/Dominion', methods=['POST', 'GET'])
def Dominion():
        return render_template('Dominion.html')

@app.route('/Scrabble', methods=['POST', 'GET'])
def Scrabble():
        return render_template('Scrabble.html')


############ ROUTES TO GENRES ############

@app.route('/DeckBuilders', methods=['POST', 'GET'])
def DeckBuilders():
        return render_template('DeckBuilders.html')


@app.route('/PartyGames', methods=['POST', 'GET'])
def PartyGames():
        return render_template('PartyGames.html')

@app.route('/WordGames', methods=['POST', 'GET'])
def WordGames():
        return render_template('WordGames.html')


if __name__ == "__main__":
    app.run(debug=True)
