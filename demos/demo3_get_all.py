import requests

# define the end point URL
BASE_URL = "http://127.0.0.1:5000/students"

# send a get request to get student with id
res = requests.get(BASE_URL)

# print response info
print(res.status_code) # the status code number
print(res.reason) # the status code message
print(res.json()) # the response body - the student list

