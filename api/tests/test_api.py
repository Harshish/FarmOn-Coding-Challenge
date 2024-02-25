import dotenv
from fastapi.testclient import TestClient
import util
import json

try:
    dotenv.load_dotenv()
except IOError:
    pass


def test_root(client_test: TestClient):
    response = client_test.get("/")
    assert response.status_code == 200
    assert response.json() == {"message":"All Creatures Welcome!"}

def test_add_parcels(client_test: TestClient):
    # Get json value of geodataframe
    util.load_parcels_data()
    df = util.get_in_batch(0,5)
    res = df.to_json()
    jval = json.loads(res)

    # Add centroid and soc value 
    util.add_soc_and_centroid()
    df = util.get_in_batch(0,5)

    # Create array of json body of the POST requests
    req = []
    for i in df.index:
        item = dict(jval['features'][i]['properties'])
        item['soc'] = df.iloc[i]['soc'][0]
        item['centroid']  = { "type": "Point", "coordinates": [df.iloc[i]['centroid'].x,df.iloc[i]['centroid'].y] }
        req.append(item)

    # POST each data in the DB
    for r in req:
        response = client_test.post(
            "/parcels/add_parcels",
            headers={"Accept": "application/json","Content-Type":"application/json"},
            json=r,
        )
        assert response.status_code == 200