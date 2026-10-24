"""
Flask server for the Emotion Detector web application.

Provides a web interface and an API endpoint for detecting
emotions in user-provided text.
"""

from flask import Flask, render_template, request
from EmotionDetection import emotion_detector

app = Flask("Emotion Detector")


@app.route("/emotionDetector")
def emotion_detector_route():
    """
    API endpoint that analyzes the given text for emotions.

    Reads the 'textToAnalyze' query parameter, calls the
    emotion_detector function, and returns a formatted response string.

    Returns:
        str: A formatted string with emotion scores and dominant emotion,
             or an error message if the input is invalid.
    """
    text_to_analyze = request.args.get("textToAnalyze")

    response = emotion_detector(text_to_analyze)

    # Check if the dominant_emotion is None (blank input or API error)
    if response['dominant_emotion'] is None:
        return "Invalid text! Please try again!"

    return (
        f"For the given statement, the system response is "
        f"'anger': {response['anger']}, "
        f"'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, "
        f"'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. "
        f"The dominant emotion is <b>{response['dominant_emotion']}</b>."
    )


@app.route("/")
def render_index_page():
    """
    Render the main index page of the Emotion Detector application.

    Returns:
        str: The rendered index.html template.
    """
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
