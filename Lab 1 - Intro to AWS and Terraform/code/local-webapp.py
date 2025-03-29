from flask import Flask, request, jsonify
import urllib.request
import urllib.error
import json

app = Flask(__name__)

HTML_FORM = """
<html>
    <body>
        <form method="post">
            Pokémon Name: <input type="text" name="pokemon_name">
            <input type="submit" value="Search">
        </form>
    </body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return HTML_FORM

    elif request.method == "POST":
        pokemon_name = request.form.get("pokemon_name", "").strip().lower()

        if not pokemon_name:
            return jsonify({"error": "No Pokémon name provided"}), 400

        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())

            return jsonify(data)

        except urllib.error.HTTPError as e:
            return jsonify({
                "error": f"Pokémon \"{pokemon_name}\" not found",
                "status": e.code
            }), e.code

    return jsonify({"error": "Method Not Allowed"}), 405

if __name__ == "__main__":
    app.run(debug=True)
