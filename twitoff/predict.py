"""prediction for user based on tweets"""
import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet


def predict_user(user0_name, user1_name, hypo_tweet_text):
    """
    Determine and returns which user is more likely to say a given tweet
    Example run: predict_user('elonmusk', 'jackblack', "tesla cars go fast")
    Returns a 0 (user0: 'elonmusk') or a 1 (user1: 'jackblack')
    """

    #Grabbing user from our DB
    #the user must be in our DB
    user0 = User.query.filter(User.name == user0_name).one()
    user1 = User.query.filter(User.name == user1_name).one()

    #grabbing tweet vectors from each tweet for each user
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    #vertically stack tweet_vects to get one np array
    vects = np.vstack([user0_vects, user1_vects])
    labels = np.concatenate(
        [np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))])

    #Fit model with our x's == vects y's == labels
    log_reg = LogisticRegression().fit(vects, labels)

    #vectorize hypothetical tweet to pass into .predict()
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)

    return log_reg.predict(hypo_tweet_vect.reshape(1, -1))

