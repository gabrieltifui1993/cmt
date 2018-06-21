from flask import Flask, render_template, request

web = Flask(__name__)

@web.route("/board")
def get_board():
    coin_code = request.args.get('coin')
    return render_template("coin_board.html")

@web.route("/socket")
def get_socket():
    return render_template("socket_test.html")

def sentiment_live():
    pass

if __name__ == "__main__":
    web.run(port='5003')