# pylint: disable=redefined-outer-name
"""Tests for microservice"""
import os
import json
from unittest.mock import patch
import pytest
import jsend
from falcon import testing
import service.microservice
from service.resources.case_leaverequest import CaseLeaveRequest

CLIENT_HEADERS = {
    "ACCESS_KEY": "1234567"
}

@pytest.fixture()
def client():
    """ client fixture """
    return testing.TestClient(app=service.microservice.start_service(), headers=CLIENT_HEADERS)

@pytest.fixture
def _mock_env_access_key(monkeypatch):
    """ mock environment access key """
    monkeypatch.setenv("ACCESS_KEY", CLIENT_HEADERS["ACCESS_KEY"])

def test_case_leaverequest(client, _mock_env_access_key):
    """Test case_leaverequest response"""
    with open("tests/mocks/create_case_submission.json", "r") as file_obj:
        mock_submission = bytes(file_obj.read(), 'utf-8')
    assert mock_submission

    with open("tests/mocks/create_case_response.json", "r") as file_obj:
        mock_response = json.load(file_obj)
    assert mock_response

    workspace = os.environ.get("PM_WORKSPACE") if os.environ.get("PM_WORKSPACE") else "test"
    response = client.simulate_post(
        "/cases/leaveRequest?workspace="+workspace,
        headers=CLIENT_HEADERS,
        body=mock_submission)

    response_json = response.json
    assert response_json['status'] == "success"

    assert "data" in response_json
    assert "id" in response_json
    assert "CASE_NUMBER" in response_json["data"]
    assert "APP_UID" in response_json["data"]

    assert response.status_code == 200

def test_case_leaverequest_error(client, _mock_env_access_key):
    """Test case_leaverequest error response"""
    with open("tests/mocks/create_case_submission.json", "r") as file_obj:
        mock_submission = bytes(file_obj.read(), 'utf-8')
    assert mock_submission

    workspace = os.environ.get("PM_WORKSPACE") if os.environ.get("PM_WORKSPACE") else "test"

    # Error caused by ProcessMaker.post
    with patch('service.resources.case_leaverequest.ProcessMaker.post') as mock_post:
        mock_post.side_effect = ValueError("test_case_leaverequest_error")

        response = client.simulate_post(
            "/cases/leaveRequest?workspace="+workspace,
            headers=CLIENT_HEADERS,
            body=mock_submission)

    assert response.status_code == 400
    assert jsend.is_error(response.json)

def test_get_case_json():
    """ Test get_case_json """
    with open("tests/mocks/create_case_submission.json", "r") as file_obj:
        mock_submission = bytes(file_obj.read(), 'utf-8')
    assert mock_submission

    with open("tests/mocks/create_case_data.json", "r") as file_obj:
        mock_case = json.load(file_obj)
    assert mock_case

    assert json.loads(CaseLeaveRequest.get_case_json(mock_submission)) == mock_case
