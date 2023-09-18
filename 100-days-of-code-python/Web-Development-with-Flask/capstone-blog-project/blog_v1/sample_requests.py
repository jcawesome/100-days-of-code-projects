import requests

blog_url = 'https://www.npoint.io/docs/c790b4d5cab58020d391'
response = requests.get(blog_url)
# all_posts = response.json()

print(response)