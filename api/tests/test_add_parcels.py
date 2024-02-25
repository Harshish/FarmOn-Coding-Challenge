import json
import requests

def test_add_parcels():
    data = None
    url = 'http://localhost:8080/parcels/add_parcels'
    with open('request_dict.json','r') as f:
        data = json.load(f)
    
    print("Starting requests")
    for r in data:
        print(r)
        response = requests.post(
            url,
            headers={"Accept": "application/json","Content-Type":"application/json"},
            data=json.dumps(r),
        )
        assert response.status_code == 200

test_add_parcels()