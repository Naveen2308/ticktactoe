import requests
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_recipe', methods=['POST'])
def get_recipe():
    query = request.json.get('query', '').lower()
    app_id = '5c26525e'  # Replace with your Edamam API ID
    app_key = '5c4549c32c0e7bb2d8fb75f6c2acefc8'  # Replace with your Edamam API key
    base_url = 'https://api.edamam.com/search'
    params = {
        'q': query,
        'app_id': app_id,
        'app_key': app_key,
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['hits']:
            recipe = data['hits'][0]['recipe']
            # Include image URL in the response
            return jsonify({
                'label': recipe['label'],
                'ingredientLines': recipe['ingredientLines'],
                'url': recipe['url'],
                'image': recipe['image'] if 'image' in recipe else None  # Check if image key exists
            })
        else:
            return jsonify({'message': 'Recipe not found.'}), 404
    else:
        return jsonify({'message': 'Error fetching recipe.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
