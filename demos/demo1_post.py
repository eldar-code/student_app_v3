import requests

# define the end point URL
BASE_URL = "http://127.0.0.1:5000/students"

# define the payload - what we in the HTTP request body
student = {"name": "Mark Zukerberg", "age": 32}

# send a post request to the server and get a response
res = requests.post(BASE_URL, json=student)

# print response info
print(res.status_code) # the status code number
print(res.reason) # the status code message
print(res.json()) # the response body - the student with the id or error message

