# backend.py (WSL)
from flask import Flask, request, jsonify
from virtual_cat_companion import ask_virtual_cat_companion

app = Flask(__name__)
print('started2')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('input')
    response = ask_virtual_cat_companion(user_input)
    return jsonify(response=response)

print('started1')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)