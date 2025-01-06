import pytest
import requests
from requests.exceptions import Timeout
from jsonschema import validate, ValidationError
from unittest.mock import patch
import logging

POST_SCHEMA = {
    "type": "object",
    "properties": {
        "userId": {"type": "integer"},
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": "string"},
    },
    "required": ["userId", "id", "title", "body"],
}

logging.basicConfig(level=logging.INFO)

# pytest fixture to provide base URL
@pytest.fixture(scope="module")
def base_url():
    return "https://jsonplaceholder.typicode.com"

# pytest fixture to provide headers with no authorization
@pytest.fixture(scope="module")
def headers_with_no_auth():
    return {"Content-Type": "application/json; charset=UTF-8"}  

def test_post_posts(base_url, headers_with_no_auth):
    """
    POST request: creates a new post
    """
    # Define the payload (data to be sent in the request)
    payload = {
        "title": "foo",
        "body": "bar",
        "userId": 1
    }

    response = requests.post(f"{base_url}/posts", json=payload, headers=headers_with_no_auth)    
    assert response.status_code == 201, f"Unexpected status code: {response.status_code}"
    response_data = response.json()

    # Assert that the response contains the expected data
    assert response_data["title"] == "foo"
    assert response_data["body"] == "bar"
    assert response_data["userId"] == 1
    assert "id" in response_data 
    
def test_get_post_schema(base_url):
    """
    Validating json schema for posts
    """
    response = requests.get(f"{base_url}/posts/1")
    assert response.status_code == 200
    try:
        validate(instance=response.json(), schema=POST_SCHEMA)
    except ValidationError as e:
        pytest.fail(f"Response schema validation failed: {e}")

def test_get_posts(base_url):
    """
    GET request: return a list of all posts
    """
    logging.info("Testing GET /posts endpoint")
    response = requests.get(f"{base_url}/posts")
    logging.info(f"Response status code: {response.status_code}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
@patch("requests.post")
def test_post_posts_mock_success(mock_post, base_url):
    """
    POST request: simulating a 201
    """
    payload = {"title": "foo", "body": "bar", "userId": 1}
    mock_response = {"id": 101, "title": "foo", "body": "bar", "userId": 1}
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = mock_response

    response = requests.post(f"{base_url}/posts", json=payload)
    assert response.status_code == 201
    assert response.json() == mock_response

@patch("requests.post")
def test_post_posts_mock_invalid_data(mock_post, base_url):
    """
    POST request: simulating a 400
    """
    payload = {"title": "", "body": "", "userId": 1}  # Invalid payload
    mock_post.return_value.status_code = 400

    response = requests.post(f"{base_url}/posts", json=payload)
    assert response.status_code == 400 
    
@pytest.mark.parametrize("post_id, expected_user_id", [(1, 1), (2, 1), (3, 1)])
def test_get_post_by_id(base_url, post_id, expected_user_id):
    """
    GET request: return a post based on userId
    """
    response = requests.get(f"{base_url}/posts/{post_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == post_id
    assert response_data["userId"] == expected_user_id
    
@patch("requests.get")
def test_get_posts_mock_success(mock_get, base_url):
    """
    GET request: simulating a 200 OK 
    """
    mock_response = {
        "userId": 1,
        "id": 1,
        "title": "mocked title",
        "body": "mocked body",
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    response = requests.get(f"{base_url}/posts/1")
    assert response.status_code == 200
    assert response.json() == mock_response    
    
@patch("requests.get")
def test_get_post_mock_server_error(mock_get, base_url):
    """
    GET request: simulating a 500 server error 
    """
    mock_get.return_value.status_code = 500

    response = requests.get(f"{base_url}/posts/1")
    assert response.status_code == 500
    
@patch("requests.get")
def test_get_posts_network_error(mock_get, base_url):
    """
    GET request: simulating a network error 
    """
    mock_get.side_effect = requests.exceptions.ConnectionError

    with pytest.raises(requests.exceptions.ConnectionError):
        requests.get(f"{base_url}/posts")
        
@patch("requests.get")
def test_get_posts_timeout(mock_get, base_url):
    """
    GET request: simulating a timeout error 
    """
    mock_get.side_effect = Timeout

    with pytest.raises(Timeout):
        requests.get(f"{base_url}/posts", timeout=1)



def test_filter_posts_by_user_id(base_url):
    """
    Filtering posts: return only posts of user with userID 1
    """
    params = {"userId" : 1}
    response = requests.get(f"{base_url}/posts", params=params)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    posts = response.json()
    
    for post in posts:
        assert post["userId"] == 1, f"Post with ID {post['id']} does not belong to userId 1"  

def test_put_posts(base_url, headers_with_no_auth):
    """
    PUT request: updating existing post with ID 1
    """
    # Define the payload (data to be sent in the request)
    payload = {
        "id": 1,
        "title": "foo2",
        "body": "bar",
        "userId": 1
    }

    response = requests.put(f"{base_url}/posts/1", json=payload, headers=headers_with_no_auth)    
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    response_data = response.json()

    # Assert that the response contains the expected data
    assert response_data["id"] == 1
    assert response_data["title"] == "foo2"
    
@patch("requests.put")
def test_put_post_success(mock_put, base_url):
    """
    PUT request: simulating a 200 OK
    """
    payload = {"id": 1, "title": "Updated Title", "body": "Updated Body", "userId": 1}
    mock_response = {"id": 1, "title": "Updated Title", "body": "Updated Body", "userId": 1}
    mock_put.return_value.status_code = 200
    mock_put.return_value.json.return_value = mock_response

    response = requests.put(f"{base_url}/posts/1", json=payload)
    assert response.status_code == 200
    assert response.json() == mock_response

@patch("requests.put")
def test_put_post_server_error(mock_put, base_url):
    """
    PUT request: simulating a 500 server error 
    """
    payload = {"id": 1, "title": "Error Title", "body": "Error Body", "userId": 1}
    mock_put.return_value.status_code = 500

    response = requests.put(f"{base_url}/posts/1", json=payload)
    assert response.status_code == 500

#Delete = Delete some post
def test_delete_post_id_1(base_url):
    """
    DELETE request: deleting existing post with ID 1
    """
    response = requests.delete(f"{base_url}/posts/1")
    assert response.status_code == 200
    print(f"Resource with ID 1 deleted successfully.")
    
@patch("requests.delete")
def test_delete_post_success(mock_delete, base_url):
    """
    DELETE request: simulating a 200 OK
    """
    mock_delete.return_value.status_code = 200

    response = requests.delete(f"{base_url}/posts/1")
    assert response.status_code == 200

@patch("requests.delete")
def test_delete_post_not_found(mock_delete, base_url):
    """
    DELETE request: simulating 404 Error
    """
    mock_delete.return_value.status_code = 404

    response = requests.delete(f"{base_url}/posts/999")  # Non-existent post
    assert response.status_code == 404

   
def test_get_comments(base_url):
    """
    GET request: get all comments
    """
    response = requests.get(f"{base_url}/comments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Assuming the response is a list of comments
    
def test_filter_comments_by_user_email(base_url):
    """
    Filter comments: return only comments which belong to a user with a specific email
    """
    params = {"email" : "Lew@alysha.tv"}
    response = requests.get(f"{base_url}/posts/1/comments", params=params)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    posts = response.json()
    
    for post in posts:
        assert post["email"] == "Lew@alysha.tv", (
            f"Comment  for Post with ID 1 does not belong to user with email {post['email']}"
            )
        
def test_fetch_some_comment(base_url):
    """
    Fetching all comments under post with id post_id
    """
    post_id = 1
    endpoint = f"{base_url}/posts/{post_id}/comments"    
    
    response = requests.get(endpoint)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    comments = response.json()
    
    required_keys = {"postId", "id", "name", "email", "body"}
    for comment in comments:
        assert required_keys.issubset(comment.keys()), f"Missing keys in comment: {comment}"
        assert comment["postId"] == post_id, f"Comment does not belong to post ID {post_id}"