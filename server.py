from flask import Flask, request, jsonify, send_from_directory
import os
import pyphen
import re

# Initialize Pyphen with Hungarian patterns
hyphenator = pyphen.Pyphen(lang='hu_HU')

app = Flask(__name__)

# Route to serve the index.html file
@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

# Route to get supported languages from pyphen.LANGUAGES
@app.route('/languages', methods=['GET'])
def get_languages():
    supported_languages = pyphen.LANGUAGES
    # Return the language codes and names
    return jsonify(list([key for key in supported_languages.keys() if len(key) == 2]))

# Route to hyphenate input text based on selected language
@app.route('/hyphenate', methods=['POST'])
def hyphenate_text():
    data = request.json
    text = data.get('text', '')
    language = data.get('language', 'hu_HU')  # Default to Hungarian if no language is selected
    # Initialize the Pyphen object with the selected language
    hyphenator = pyphen.Pyphen(lang=language)

    # Split the text into words
    words = text.split()

    # Hyphenate each word
    hyphenated_words = [hyphenator.inserted(word, hyphen='-') for word in words]

    # Replace hyphens between non-space characters with "- "
    hyphenated_text = " ".join(hyphenated_words).replace("--", "-")

    return jsonify({'result': hyphenated_text})

