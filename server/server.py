import flask
from main import Main

class Server:
    def __init__(self, main: Main):
        self.app = flask.Flask(__name__, template_folder="templates", static_folder="static")
        self.main = main

        @self.app.route("/")
        def start():
            return self.app.send_static_file("html/index.html")
        
        @self.app.route("/points")
        def points():
            return flask.jsonify({'score1' : self.main.score1, 'score2' : self.main.score2})
            
    def run(self):
        self.app.run(debug=True)

if __name__ == "__main__":
    Server().run()