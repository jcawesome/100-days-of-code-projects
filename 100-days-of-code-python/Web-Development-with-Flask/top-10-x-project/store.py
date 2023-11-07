import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)

# Function to Fetch All Movies
def find_all_movies():
    data = supabase.table("movie").select("*").execute()
    # Equivalent for SQL Query "SELECT * FROM games;"
    return data

movies = find_all_movies()
print(movies)