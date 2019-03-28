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
          "title" : "Setup",
          "description" : "Setting up Python Dev Environment",
          "content" : "To begin the setup process, please download Python by following the instructions here: <a href='https://www.python.org/downloads/'>https://www.python.org/downloads/</a>. Make sure you add Python to PATH (this should appear as a checkbox during installation). We recommend you get Python 3.6 or newer."
        },
        {
           "title": "Testing",
           "description" : "Making sure the Python installation worked",
           "content" : "Type this into command prompt (or Terminal): <pre class=\"language-python\"><code>python --version</code></pre> If the command is not found, then the installation failed (or you didn't setup the path)."
        },
        {
        "title" : "Writing Hello World",
        "description" : "The most basic Python program.",
        "content" : """
                    Create a file with an extension of \".py\". This will allow you to run the Python script at any time. Paste the code below to create your first program and reopen
                    Command Prompt. There, you must navigate to the directory of the \".py\" file and type \"python {filename}.py\" Note: \"{filename}\" should be replaced with your
                    python script's name. You can also use an IDE such as PyCharm (what I use), or a simple Text Editor like Sublime Text.  
                    <script src=\"https://gist.github.com/harrisbegca/9cb76603192b62d91dea0aad389e7431.js\"></script>
                    Note the lack of semicolons and excessive methods - Python is simple and concise (totally not throwing shade at C++ & Java).
                    """
        },
          {
              "title": "For/While/Foreach Loops",
              "description": "You'll remember this stuff FOREVER",
              "content": "<script src=\"https://gist.github.com/harrisbegca/bd6155e03f19c63b9cd1a77052c9d5cf.js\"></script>"
          },
        {
        "title" : "Writing a Class",
        "description" : "This class will define a class with parameter 'message'. The constructor defines an object of this class with the parameter.",
        "content" : """<script src=\"https://gist.github.com/harrisbegca/c8f5e00308fea54ecdac2f9e1492186a.js\"></script>
                        For the time being, this is the class structure that we will work with. The init method signifies a constructor, which
                        is a type of method. Methods are covered below. If this is confusing, another example is given below:
                        <script src="https://gist.github.com/harrisbegca/f34382868e61ace4af560e654f1ee84b.js"></script>
        """
      },
      {
        "title" : "Writing a Method",
        "description" : "We can do a lot of things with methods - and methods don't have to be defined in a class, like Java.",
        "content" : "<script src=\"https://gist.github.com/harrisbegca/877a6675b580f80bf2f4999afaaaf471.js\"></script>"
      },
      {
        "title" : "Optional: Lambda",
        "description" : "A lambda is essentially a shortened method. Lambdas are useful for quick operations or shorthand writing.",
        "content" : "<script src=\"https://gist.github.com/harrisbegca/5e33b482a0826664d050ea42205ca5b4.js\"></script>"
      },
      {
          "title": "Optional: Intro to Args & Kwargs",
          "description": "Need more parameters but don't want to define them each time? Well, you're in luck since Python doesn't allow overloading anyways.",
          "content": "<script src=\"https://gist.github.com/harrisbegca/bd6155e03f19c63b9cd1a77052c9d5cf.js\"></script>"
      },
      {
        "title" : "Inheritance",
        "description" : "But wait, what's the point of methods or classes if we only use em once? Well, that's where inheritance comes in.",
        "content" : "This is where it gets difficult.<script src=\"https://gist.github.com/harrisbegca/573c2bb56c551b7625ca0772ec798264.js\"></script>"
      }

  ],
  "java": [
      {
        "title" : "Setting up Flask",
        "description" : "Description",
        "content" : "<pre><code class='language-python'>print('Hello World')</code></pre>"
      }
  ],
    "js":[]
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

'''
Generates random gradient from list (gathered from UIGradients)
'''
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
