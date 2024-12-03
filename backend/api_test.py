# import requests
#
# url = "https://api.themoviedb.org/3/authentication"
#
# headers = {
#     "accept": "application/json",
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzYzkxMWYxYzZhYTBkYmQxZGMwMGE5MmE4NTg5ZDNmMyIsIm5iZiI6MTczMzE2NjA3Mi40OTEwMDAyLCJzdWIiOiI2NzRlMDNmOGQ4YWM0NTY3M2QxM2Y3N2MiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.LpLe6g8Dajwsk15oqX5pia5OxyfE2EDYo-fOZy72dXQ"
# }
#
# response = requests.get(url, headers=headers)
#
# print(response.text)


import requests

url = "https://api.themoviedb.org/3/search/movie?query=star%20wars&include_adult=false&language=en-US&page=1"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzYzkxMWYxYzZhYTBkYmQxZGMwMGE5MmE4NTg5ZDNmMyIsIm5iZiI6MTczMzE2NjA3Mi40OTEwMDAyLCJzdWIiOiI2NzRlMDNmOGQ4YWM0NTY3M2QxM2Y3N2MiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.LpLe6g8Dajwsk15oqX5pia5OxyfE2EDYo-fOZy72dXQ"
}

response = requests.get(url, headers=headers)

print(response.text)

