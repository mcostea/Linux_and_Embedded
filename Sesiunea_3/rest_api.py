from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for items
items = {}

# Endpoint to create a new item
@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    if not data or 'id' not in data or 'name' not in data:
        return jsonify({'error': 'Bad Request', 'message': 'id and name are required'}), 400
    
    item_id = data['id']
    if item_id in items:
        return jsonify({'error': 'Conflict', 'message': f'Item with id {item_id} already exists'}), 409
    
    items[item_id] = data['name']
    return jsonify({'message': 'Item created', 'item': {item_id: items[item_id]}}), 201

# Endpoint to get an item by id
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    if item_id not in items:
        return jsonify({'error': 'Not Found', 'message': f'Item with id {item_id} not found'}), 404
    
    return jsonify({'item': {item_id: items[item_id]}}), 200

# Endpoint to update an existing item
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    if item_id not in items:
        return jsonify({'error': 'Not Found', 'message': f'Item with id {item_id} not found'}), 404
    
    data = request.json
    if not data or 'name' not in data:
        return jsonify({'error': 'Bad Request', 'message': 'name is required'}), 400
    
    items[item_id] = data['name']
    return jsonify({'message': 'Item updated', 'item': {item_id: items[item_id]}}), 200

# Endpoint to delete an item
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if item_id not in items:
        return jsonify({'error': 'Not Found', 'message': f'Item with id {item_id} not found'}), 404
    
    del items[item_id]
    return jsonify({'message': 'Item deleted'}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
