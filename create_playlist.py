import requests

CREATE_PLAYLIST_URL = "https://api.spotify.com/v1/users/hillybilly18/playlists"

ACCESS_TOKEN = 'BQAMmQ7qz53SClbwrKxiVxWY4pnQ7xdxmwsuS8qcDudh5axHH9nUja4t5t-hkmdixRn36f-52q5FifLezqNh0-Wgp8qKgj694XpXd_PGvt4RrPJCM3xz'

def create_playlist(name, public):
    response = requests.post(
        CREATE_PLAYLIST_URL, 
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}"
            },
            json = {
                "name": name, 
                "public": public
            }
    )
    json_resp = response.json()
    return json_resp

def main():
    playlist = create_playlist(
        name = "My Private Playlist",
        public = False
    )
    print(f"Playlist: {playlist}")

if __name__ == '__main__':
    main()