
import json
import requests

def test_find_parcel_by_location():
    data = None
    url = 'http://localhost:8080/parcels/find_parcel_by_location'

    print("Starting Querying...")
    r = requests.get(url, params={'longitude': 3.78, 'latitude': 51})
    assert r.status_code == 200
    jval = json.loads(r.text)
    assert "objectid" in jval
    objid = jval["objectid"]

    r = requests.get(url, params={'longitude': 33.78, 'latitude': 51})
    assert r.status_code == 200
    assert "No feilds found within radius" in r.text

    r = requests.get(url, params={'longitude': 91, 'latitude': 91})
    assert r.status_code == 200
    assert "OperationFailure" in r.text

    r = requests.get(url, params={'longitude': 420787.675, 'latitude': 6621293.722, 'crs':"EPSG:3857"})
    assert r.status_code == 200
    jval = json.loads(r.text)
    assert objid == jval["objectid"]

    print("All Tests successfull")

test_find_parcel_by_location()