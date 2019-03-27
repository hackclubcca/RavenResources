from flask import Flask, render_template, request, redirect, url_for
from wtforms import Form, StringField, validators, TextAreaField
#from flask_wtf import RecaptchaField
from flask_mail import Mail, Message
from typing import Type
import os
import json
import random
gradients = {}
try:
    with open("app/gradients.json") as f:
        gradients = json.load(f)
except Exception:
    print()

RECAPTCHA_PRIVATE_KEY=""
tutorials = {
 "python": [
            {
                "title" : "Setting up Flask",
                "description" : "Description",
                "content" : """
                <pre><code>from Flask import flask, render_template, redirect</code></pre>
                """
            }
        ],
  "java": [
      {
                "title" : "Setting up Flask",
                "description" : "Description",
                "content" : """
                <pre><code>from Flask import flask, render_template, redirect</code></pre>
                """
      }
  ]
}


class ContactForm(Form):
    sender = StringField('Your Email', [validators.Length(min=20, max=1000), validators.Email(), validators.DataRequired()])
    title = StringField('Title', [validators.Length(min=3, max=25)])
    message = TextAreaField('Message', [validators.Length(min=20, max=1000), validators.DataRequired()])
    #captcha = RecaptchaField()


app = Flask(__name__)
app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='appdevelopmentcca@gmail.com',
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD")
))
mail = Mail(app)


def gradient():
    gradient = gradients[random.randint(0, 200)]['colors']
    return [gradient[0], gradient[1]]

@app.route('/')
def home():
    return render_template("index.html", name="Home", gradient=gradient())


@app.route('/about')
def about():
    return render_template("about.html", members = [
        {
            "image" : "https://media.licdn.com/dms/image/C5603AQGU_OYB_qsooQ/profile-displayphoto-shrink_200_200/0?e=1558569600&v=beta&t=elLp6fQn6IJbiywv3LM9zKPrY3IZah5dvl3VPGzhlLY",
            "name" : "Harris",
            "role" : "Owner",
            "grade" : 11,
            "bio" : "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
        },
        {
            "name" : "Doge",
            "role" : "Moral Support",
            "grade" : 13,
            "bio" : "Much doge. Much wow. Okay but really, why did I do this."
        }
    ], name="About", gradient=gradient())


@app.route('/contact', methods=['GET', 'POST'])
def contact():  # Theoretically we'll add post and get requests
    email = ContactForm(request.form)
    if request.method == 'POST' and email.validate():
        msg = Message(email.message.data, sender=email.sender.data, recipients=["appdevelopmentcca@gmail.com"])
        mail.send(msg)
        return redirect(url_for('contact'))
    return render_template("contact.html", form=email, name="Contact", gradient=gradient())


@app.route('/learn/<language>')
def learn(language):
    #if language.upper() == "PYTHON":
    #    return render_template("resources/python.html", name="Learn: Python", gradient=gradient(), sections = tutorials["python"])
    return render_template("resources/python.html", name="Learn: " + language, gradient=gradient(), sections=tutorials[language.lower()])


if __name__ == '__main__':
    app.run()
