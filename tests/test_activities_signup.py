def test_signup_for_activity_adds_participant(client, new_email):
    response = client.post(f"/activities/Chess Club/signup?email={new_email}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {new_email} for Chess Club"}

    activities_response = client.get("/activities")
    assert new_email in activities_response.json()["Chess Club"]["participants"]


def test_signup_for_activity_rejects_duplicate_participant(client, existing_email):
    response = client.post(f"/activities/Chess Club/signup?email={existing_email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_for_activity_returns_404_for_unknown_activity(client, new_email):
    response = client.post(f"/activities/Unknown Club/signup?email={new_email}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_for_activity_requires_email_query_parameter(client):
    response = client.post("/activities/Chess Club/signup")

    assert response.status_code == 422
