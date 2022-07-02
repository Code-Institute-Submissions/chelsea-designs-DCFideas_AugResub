from flask import render_template, request, redirect, url_for
from dcfideas import app, db
from dcfideas.models import Strand, Idea 


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register",methods=["GET","POST"])
def register():
    return render_template("register.html")



@app.route("/strands")
def strands():
    strands = list(Strand.query.order_by(Strand.strand_name).all())
    categories = set()
    for x in strands:
        categories.add(x.strand_name)
    return render_template("strands.html", strands=strands, categories=categories)

@app.route("/ideas")
def ideas():
    ideas = list(Idea.query.order_by(Idea.idea_name).all())
    return render_template("ideas.html", ideas=ideas)

@app.route("/add_idea", methods=["GET", "POST"])
def add_idea():
    strands = list(Strand.query.order_by(Strand.strand_name).all())
    if request.method == "POST":
        idea = Idea(
            idea_name=request.form.get("idea_name"),
            idea_description=request.form.get("idea_description"),
            strand_id=request.form.get("strand_id"),
            idea_teacher =request.form.get("idea_teacher"),
        )
        db.session.add(idea)
        db.session.commit()
        return redirect(url_for('ideas'))
    return render_template("add_idea.html", strands=strands)


@app.route("/update_idea/<int:idea_id>", methods=["GET", "POST"])
def update_idea(idea_id):
    idea = Idea.query.get_or_404(idea_id)
    strands = list(Strand.query.order_by(Strand.strand_name).all())
    if request.method == "POST":
        idea.idea_name=request.form.get("idea_name")
        idea.idea_description=request.form.get("idea_description")
        idea.strand_id=request.form.get("strand_id")
        idea.idea_teacher=request.form.get("idea_teacher")
        db.session.commit()
        return redirect(url_for('ideas'))
    return render_template("update_idea.html", idea=idea, strands=strands)

@app.route("/delete_idea/<int:idea_id>")
def delete_idea(idea_id):
    idea = Idea.query.get_or_404(idea_id)
    db.session.delete(idea)
    db.session.commit()
    return redirect(url_for("ideas"))


# ---------- Error Handling Functionality ---------- #

# --- 404 Handler --- #
@app.errorhandler(404)
def page_not_found(e):
    """
    Renders a custom 404 error page with a button
    that takes the user back to the home page.
    """
    return render_template("errors/404.html", page_title="404"), 404


# --- 500 Handler --- #
@app.errorhandler(500)
def internal_server_error(e):
    """
    Renders a custom 500 error page with a button
    that takes the user back to the home page.
    """
    return render_template("errors/500.html", page_title="500"), 500
