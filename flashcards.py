from model import db, save_db
from flask import Flask, render_template, abort, jsonify, request, redirect, url_for


app = Flask(__name__)


@app.route("/")
def welcome():
    return render_template("welcome.html",
                           message="Nice work my friend!")


@app.route("/cards_list")
def cards_list():
    return render_template("cards_list.html", cards=db)


@app.route("/card/<int:index>")
def card(index):
    try:
        c = db[index]
        return render_template("card.html",
                               card=c,
                               index=index,
                               max_idx=len(db)-1)
    except IndexError:
        abort(404)


@app.route("/add_card", methods=["GET", "POST"])
def add_card():
    if request.method == "POST":
        _card = {
            "id": len(db),
            "question": request.form["question"],
            "answer": request.form["answer"]
        }
        db.append(_card)
        save_db()
        return redirect(url_for("card", index=_card['id']))

    return render_template("add_card.html")


@app.route("/remove_card/<int:index>", methods=["POST", "GET"])
def remove_card(index):
    if request.method == "POST":
        db.pop(index)
        save_db()
        return redirect(url_for("cards_list"))
    c = db[index]
    return render_template("remove_card.html", card=c)


@app.route("/edit_card/<int:index>", methods=["GET", "POST"])
def edit_card(index):
    try:
        c = db[index]
        if request.method == "POST":
            qst = request.form["question"]
            ans = request.form["answer"]
            flash_card = db[index]
            flash_card['question'] = qst
            flash_card['answer'] = ans
            save_db()
            return redirect(url_for("cards_list"))
        return render_template("edit_card.html", card=c)
    except IndexError:
        abort(404)


# Return REST Data
@app.route("/api/cards_list")
def api_cards_list():
    return jsonify(db)


@app.route("/api/card/<int:index>")
def api_card(index):
    try:
        return db[index]
    except IndexError:
        abort(404)

