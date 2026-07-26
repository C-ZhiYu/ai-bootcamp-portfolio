from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
)

from src.map_loader import load_map
from src.pathfinder import dijkstra
from src.visualizer import draw_map
from src.auth import check_password

app = Flask(__name__)

app.secret_key = "day8-secret"

@app.route("/", methods=["GET", "POST"])
def index():

    nodes, edges = load_map()

    result = None
    image = None

    if request.method == "POST":

        start = int(request.form["start"])
        end = int(request.form["end"])

        try:

            path, distance = dijkstra(
                nodes,
                edges,
                start,
                end,
            )

            draw_map(
                nodes,
                edges,
                path,
            )

            result = {

                "path": " -> ".join(map(str, path)),
                "distance": distance,

            }

            image = "map.png"

        except Exception as e:

            result = {

                "error": str(e)

            }

    return render_template(

        "index.html",

        nodes=nodes.values(),

        result=result,

        image=image,

    )


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        password = request.form["password"]

        if check_password(password):

            session["editor"] = True

            return redirect("/")

        return render_template(

            "login.html",

            error="Wrong password",

        )

    return render_template("login.html")


@app.route("/edit")
def edit():

    if not session.get("editor"):

        return "Access Denied", 403

    return "<h1>Editor Mode</h1>"


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=60003,

        debug=True,

    )