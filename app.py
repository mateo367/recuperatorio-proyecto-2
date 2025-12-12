from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

MAP_PATH = "mapa_guardado.json"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/guardar", methods=["POST"])
def guardar():
    data = request.get_json()
    if not data:
        return jsonify({"ok": False, "error": "No JSON recibido"}), 400
    try:
        with open(MAP_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/cargar", methods=["GET"])
def cargar():
    if not os.path.exists(MAP_PATH):
        # devolver mapa vacío por defecto
        mapa = [[1 for _ in range(40)] for _ in range(20)]
        mapa_arboles = [[0 for _ in range(40)] for _ in range(20)]
        return jsonify({"mapa": mapa, "mapa_arboles": mapa_arboles})
    with open(MAP_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
