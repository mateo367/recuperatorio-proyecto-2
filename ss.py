from flask import Flask, render_template

app = Flask(__name__)

mapa = [[1 for _ in range(40)] for _ in range(20)]
mapa_arboles = [[0 for _ in range(40)] for _ in range(20)]


@app.route("/")
def home():
    return render_template("index2.html")
    
if __name__ == "__main__":
    app.run()