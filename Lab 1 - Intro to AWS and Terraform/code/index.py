import json
import urllib.request
import urllib.error

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

def handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method", "")

    if method == "GET":
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": HTML_FORM,
        }

    elif method == "POST":
        body = event.get("body", "")
        if event.get("isBase64Encoded"):
            import base64
            body = base64.b64decode(body).decode()

        # Parse form-encoded body (e.g., "pokemon_name=ditto")
        params = dict(x.split('=') for x in body.split('&') if '=' in x)
        pokemon_name = params.get("pokemon_name", "").strip().lower()

        if not pokemon_name:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No Pokémon name provided"})
            }

        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())

            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(data)
            }

        except urllib.error.HTTPError as e:
            return {
                "statusCode": e.code,
                "body": json.dumps({"error": f"Pokémon \"{pokemon_name}\" not found", "status": e.code})
            }

    return {
        "statusCode": 405,
        "body": json.dumps({"error": "Method Not Allowed"})
    }
