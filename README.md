
SWEN 230: Final Project - Param Dhaliwal 
================================================================

## Music Recommender

1. **Input**: Users provide the names of three artists they enjoy listening to.
2. **Processing**: The application returns songs by similar artist using the Spotify API.
3. **Output**: Users receive a curated list of recommended songs, complete with artist names and track titles, that can be previewed.

#### Step 1: Install all requirements
```
make install
```
#### Step 2: Load flask 
```
make flask
```
#### Step 3: Type in 3 artist of your choosing and press Get Songs

Note: Adjust volume, it could be too loud.

#### Step 4: Wait for songs to load, You might be interested in some of these songs.

Note: Some songs cannot be previewed due to spotify api not having previews for them.



#### For API, get Client ID and Client Secret from Spotify API [https://developer.spotify.com/] and define them as such in a .env file.
```
CLIENT_ID="put client id here"
CLIENT_SECRET="put client secret here"
```