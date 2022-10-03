from application import app

if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True, port=5005)