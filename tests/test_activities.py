def test_get_activities(client):
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_duplicate(client):
    activity = "Chess Club"
    email = "teststudent@mergington.edu"

    # ensure not already in participants
    res = client.get("/activities")
    assert email not in res.json()[activity]["participants"]

    # sign up
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200
    assert f"Signed up {email}" in res.json()["message"]

    # duplicate signup should fail
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 400


def test_unregister(client):
    activity = "Programming Class"
    email = "temp@mergington.edu"

    # sign up first
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200

    # now unregister
    res = client.delete(f"/activities/{activity}/participants?email={email}")
    assert res.status_code == 200
    assert f"Unregistered {email}" in res.json()["message"]


def test_unregister_not_found(client):
    activity = "Programming Class"
    email = "noone@mergington.edu"

    res = client.delete(f"/activities/{activity}/participants?email={email}")
    assert res.status_code == 404
