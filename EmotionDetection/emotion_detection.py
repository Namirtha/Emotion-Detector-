"""
Module for detecting emotions in text using the Watson NLP Emotion API.
"""

import json

import requests


def emotion_detector(text_to_analyze):
    """
    Analyze the given text for emotions using the Watson NLP Embed API.

    Args:
        text_to_analyze (str): The text to analyze for emotions.

    Returns:
        dict: A dictionary containing scores for anger, disgust, fear,
              joy, sadness, and the dominant_emotion.
              Returns None values for all keys if input is blank
              or the API returns a 400 status code.
    """
    # Handle blank input before making the API call
    if not text_to_analyze or not text_to_analyze.strip():
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    url = (
        "https://sn-watson-emotion.labs.skills.network/"
        "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )

    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }

    input_json = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    response = requests.post(url, headers=headers, json=input_json, timeout=10)

    # Handle 400 status code (bad request)
    if response.status_code == 400:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    # Parse the JSON response
    formatted_response = json.loads(response.text)

    # Extract emotion scores from the response
    emotions = formatted_response['emotionPredictions'][0]['emotion']

    anger_score = emotions['anger']
    disgust_score = emotions['disgust']
    fear_score = emotions['fear']
    joy_score = emotions['joy']
    sadness_score = emotions['sadness']

    # Determine the dominant emotion (the one with the highest score)
    emotion_scores = {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score
    }

    dominant_emotion = max(emotion_scores, key=emotion_scores.get)

    # Build and return the result dictionary
    result = {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score,
        'dominant_emotion': dominant_emotion
    }

    return result
