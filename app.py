from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

mapa = [[1 for _ in range(40)] for _ in range(20)]
mapa_arboles = [[0 for _ in range(40)] for _ in range(20)]


@app.route("/")
def home():
    return render_template("index2.html")

@app.route("/guardar", methods=["POST"])
def guardar():
    nombre = request.json["nombre"]
    with open(nombre + ".txt", "w") as f:
        for fila in mapa:
            f.write("".join(str(b) for b in fila) + "\n")
        f.write("--ARBOL--\n")
        for fila in mapa_arboles:
            f.write("".join(str(b) for b in fila) + "\n")
    return jsonify({"ok": True})

@app.route("/cargar", methods=["POST"])
def cargar():
    global mapa, mapa_arboles
    nombre = request.json["nombre"]

    mapa_c = [[1 for _ in range(40)] for _ in range(20)]
    mapa_arboles_c = [[0 for _ in range(40)] for _ in range(20)]

    try:
        with open(nombre + ".txt", "r") as f:
            lineas = f.read().splitlines()

        sep = lineas.index("--ARBOL--")

        for y, fila in enumerate(lineas[:sep]):
            for x, val in enumerate(fila):
                mapa_c[y][x] = int(val)

        for y, fila in enumerate(lineas[sep+1:]):
            for x, val in enumerate(fila):
                mapa_arboles_c[y][x] = int(val)

        mapa = mapa_c
        mapa_arboles = mapa_arboles_c
    except:
        return jsonify({"ok": False})

    return jsonify({"ok": True, "mapa": mapa, "arboles": mapa_arboles})

if __name__ == "__main__":
    app.run(debug=True)
