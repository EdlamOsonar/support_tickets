def test_create_read_update_delete_item(client):
    # Create
    resp = client.post('/items/', json={'name': 'Test', 'description': 'Desc'})
    assert resp.status_code == 201
    data = resp.json()
    assert data['name'] == 'Test'
    item_id = data['id']

    # Read
    resp = client.get(f'/items/{item_id}')
    assert resp.status_code == 200
    data = resp.json()
    assert data['description'] == 'Desc'

    # Update
    resp = client.put(f'/items/{item_id}', json={'name': 'Updated', 'description': 'New'})
    assert resp.status_code == 200
    data = resp.json()
    assert data['name'] == 'Updated'

    # Delete
    resp = client.delete(f'/items/{item_id}')
    assert resp.status_code == 204

    # Confirm deleted
    resp = client.get(f'/items/{item_id}')
    assert resp.status_code == 404
