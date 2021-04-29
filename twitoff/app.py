"""This is what brings the application together"""
from os import getenv
from flask import Flask, render_template, request
# from .predict import predict_user
from .models import DB, User
from .twitter import add_or_update_user


def create_app():
    """
    The main app function for twitoff.
    Brings everything together.
    """
    # __name__ is the name of the current path module

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)
   
    @app.route('/')
    def root():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title="Home", users=User.query.all())
   
    @app.route('/update')
    def update():
        add_or_update_user('elonmusk')
        return "successful"
   
    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return "Database reset!"
   
    @app.route('/compare', methods=["POST"])
    def compare():
        user0, user1 = sorted(
            [request.values['user0'], request.values["user1"]])
        if user0 == user1:
            message = "Cannot compare users to themselves!"
        else:
            prediction = predict_user(
                user0, user1, request.values["tweet_text"])
            message = "{} is more likely to be said by {} than {}!".format(
                request.values["tweet_text"],
                user1 if prediction else user0,
                user0 if prediction else user1
            )
        return render_template('prediction.html', title="Prediction", message=message)
 
    return app