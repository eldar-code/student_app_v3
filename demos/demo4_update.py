import requests

BASE_URL = "http://127.0.0.1:5000/students"
student = {"id": 1, "name": "Eldar Bakshi", "age": 42}
res = requests.put(BASE_URL, json=student)

print(res.status_code)  # the status code number
print(res.reason)  # the status code message
print(res.json())  # the response body - the student with the id or error message
