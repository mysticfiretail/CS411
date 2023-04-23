@app.route('/get_category_playlists')
def get_category_playlists():
    with open('access_token.txt', 'r') as f:
        access_token = f.read()

    category_id = 'dinner'  #replace with weather 
    limit = 10  #will get 10 songs 

    playlists_data = get_category_playlists_data(access_token, category_id, limit)
    return json.dumps(playlists_data, indent=2)

def get_category_playlists_data(access_token, category_id, limit):
    url = f'https://api.spotify.com/v1/browse/categories/{category_id}/playlists?limit={limit}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    return data