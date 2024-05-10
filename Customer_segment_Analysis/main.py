from flask import Flask, render_template, request, g
from textblob import TextBlob
import sqlite3
import datetime

app = Flask(__name__)
DATABASE = "feedback.db"
# # SQLite database setup
conn = sqlite3.connect("feedback.db")
cursor = conn.cursor()
cursor.execute(
    """CREATE TABLE IF NOT EXISTS feedback
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,FName TEXT,
                 Email TEXT,
                 feedback TEXT,
                 sentiment TEXT,
                 timestamp TIMESTAMP)"""
)
conn.commit()


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    FName = request.form["FName"]
    Email = request.form["Email"]
    feedback_text = request.form["feedback"]
    sentiment = analyze_sentiment(feedback_text)
    timestamp = datetime.datetime.now().isoformat()
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """INSERT INTO feedback (FName, Email, feedback, sentiment, timestamp)
                      VALUES ( ?,?, ?, ?, ?)""",
        (FName,Email,feedback_text, sentiment, timestamp),
    )
    db.commit()
    return "Feedback submitted successfully!"


def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"


if __name__ == "__main__":
    app.run(debug=True)
