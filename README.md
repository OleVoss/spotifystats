# SpotifyStats

From the Spotify account site, one can request an extended history of a profile. This history includes every track played for at least 30 seconds, and allows for a more thorough analysis of the listening behavior within that time.  

The information provided by the history _as is_, is the following:

- Timestamp
- Track uri
- Milliseconds played
- Reason the track was started/ended
- Was the track skipped?

The rest is either not interesting to me, or requires cleaning/processing to be used in a meaningful manner.
This includes the information about the artists, these are only referenced by name, which bears the risk of mistaking two artists for the same. Also, a song may be produced by multiple aritsts, that also is not reflected in the history.

Through processing and utilising the spotify web api the additional data will be gathred for analysis:

- [x] Every artist per song
- [x] Each artists genres
- [ ] Musik features (Spotify Api):
  - uri
  - acousticness
  - danceability
  - duration_ms
  - energy
  - instrumentalness
  - key
  - liveness
  - loudness
  - mode
  - speechiness
  - tempo
  - time_signature
  - valence

## Metrics

Metric, stats and statistics planned to do:

- [ ] Correlation Matrix
  - [ ] audio features
  - [ ] listening activity
    - [ ] time
    - [ ] weekday
    - [ ] month
    - [ ] season
- [ ] Fun stats
  - [ ] Tracks with most plays
  - [ ] Artists with most plays
  - [ ] Genres with most plays
  - [ ] Most skipped song
- [ ] Listening behavior over time
  - [ ] Playtime
  - [ ] Musik features (bpm, energy, danceability) \
        It might be interesting to look for correlations with months/seasons.
- [ ] Cluster maps
  - [ ] Genres
  - [ ] Artists
- [ ] Sessions
  - [ ] How long
  - [ ] Correlation Session <-> Genre
  - [ ] Correlation Session <-> Musik features
- [ ] Correlation track presence and musik features (bpm)
