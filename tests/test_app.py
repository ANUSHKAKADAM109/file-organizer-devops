import pytest
from app import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    app.config["TESTING"] = True

    # Keep test history separate from real application history.
    monkeypatch.setattr(
        "app.CSV_LOG",
        str(tmp_path / "test_organizer_log.csv")
    )

    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_homepage_loads(client):
    response = client.get("/")

    assert response.status_code == 200


def test_organize_rejects_missing_folder_path(client):
    response = client.post("/organize", json={})

    assert response.status_code == 200
    assert response.get_json()["success"] is False
    assert response.get_json()["error"] == "No folder path provided."


def test_organize_rejects_invalid_folder(client, tmp_path):
    invalid_path = str(tmp_path / "does_not_exist")

    response = client.post(
        "/organize",
        json={"folder_path": invalid_path}
    )

    assert response.status_code == 200
    assert response.get_json()["success"] is False
    assert response.get_json()["error"] == "Invalid folder path."


def test_organize_moves_files_into_categories(client, tmp_path):
    # Create disposable test files.
    image_file = tmp_path / "photo.jpg"
    document_file = tmp_path / "notes.txt"
    unknown_file = tmp_path / "data.xyz"

    image_file.write_text("image test data")
    document_file.write_text("document test data")
    unknown_file.write_text("unknown test data")

    response = client.post(
        "/organize",
        json={"folder_path": str(tmp_path)}
    )

    result = response.get_json()

    assert response.status_code == 200
    assert result["success"] is True
    assert result["total"] == 3

    assert (tmp_path / "Images" / "photo.jpg").exists()
    assert (tmp_path / "Documents" / "notes.txt").exists()
    assert (tmp_path / "Others" / "data.xyz").exists()


def test_history_returns_logged_files(client, tmp_path):
    (tmp_path / "report.pdf").write_text("test document")

    client.post(
        "/organize",
        json={"folder_path": str(tmp_path)}
    )

    response = client.get("/history")
    result = response.get_json()

    assert response.status_code == 200
    assert len(result["logs"]) == 1
    assert result["logs"][0]["File"] == "report.pdf"
    assert result["logs"][0]["Destination"] == "Documents"


def test_clear_history_removes_log(client, tmp_path):
    (tmp_path / "song.mp3").write_text("test audio")

    client.post(
        "/organize",
        json={"folder_path": str(tmp_path)}
    )

    response = client.post("/clear-history")

    assert response.status_code == 200
    assert response.get_json()["success"] is True

    history_response = client.get("/history")
    assert history_response.get_json()["logs"] == []