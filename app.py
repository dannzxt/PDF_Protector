from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import os
from pdf_modifier import modify_pdf

app = Flask(__name__)
app.config["SECRET_KEY"] = "0123456789"
app.config["UPLOAD_FOLDER"] = "./uploads/"


class IDInputForm(FlaskForm):
    id = StringField("ID", validators=[DataRequired()])
    position = SelectField(
        "Position",
        choices=[
            ("top-left", "Top Left"),
            ("top-right", "Top Right"),
            ("bottom-left", "Bottom Left"),
            ("bottom-right", "Bottom Right"),
        ],
    )
    submit = SubmitField("Submit")
    color = StringField("Color", validators=[DataRequired()])


@app.route("/", methods=["GET", "POST"])
def upload_file():
    form = IDInputForm()
    if form.validate_on_submit():
        if "file" not in request.files:
            flash("File not attached!")
            return redirect(request.url)
        file = request.files["file"]

        if file.filename == "":
            flash("File not selected!")
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            id = form.id.data
            position = form.position.data
            color = form.color.data

            try:
                modify_pdf(filename, id, position, color, app.config["UPLOAD_FOLDER"])
                return send_file(
                    os.path.join(app.config["UPLOAD_FOLDER"], filename),
                    as_attachment=False,
                )

            except Exception as e:
                flash(f"Error sending the file: {str(e)}")
                return redirect(request.url)

    return render_template("index.html", form=form)
