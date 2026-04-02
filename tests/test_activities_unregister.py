def test_unregister_participant_removes_participant(client, existing_email):
    response = client.delete(
        f"/activities/Chess Club/participants?email={existing_email}"
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {existing_email} from Chess Club"
    }

    activities_response = client.get("/activities")
    assert existing_email not in activities_response.json()["Chess Club"]["participants"]


def test_unregister_participant_returns_404_when_participant_missing(client, new_email):
    response = client.delete(f"/activities/Chess Club/participants?email={new_email}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"


def test_unregister_participant_returns_404_for_unknown_activity(client, new_email):
    response = client.delete(f"/activities/Unknown Club/participants?email={new_email}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_requires_email_query_parameter(client):
    response = client.delete("/activities/Chess Club/participants")

    assert response.status_code == 422
