import os
import requests
import pytest
import logging
log = logging.getLogger(__name__)

# Set the API base URL
BASE_URL = os.environ["GATEWAY_URL"]

# Positive Test Case 1: Testing "/" endpoint
def test_hello_world_endpoint():
  response = requests.get(BASE_URL + "/",verify=False) 
  assert response.status_code == 200
  assert response.text == '{"Hello":"World"}'
  log.info(response.status_code)

# Positive Test Case 2: Testing "/predict" endpoint with a valid image
def test_predict_no_image():
    response = requests.post(BASE_URL + "/predict", verify=False)
    assert response.status_code == 422  # Check if the status code is 422, as it's the expected status code for this test case

# Negative Test Case 1: Testing "/predict" endpoint with no image
def test_predict_no_image():
    response = requests.post(BASE_URL + "/predict", verify=False)
    assert response.status_code == 422  # Check if the status code is 422, as it's the expected status code for this test case
  
# Negative Test Case 2: Testing an invalid endpoint
def test_invalid_endpoint():
    response = requests.get(BASE_URL + "/invalid_endpoint", verify=False)
    assert response.status_code == 404

if __name__ == "__main__":
    pytest.main()
