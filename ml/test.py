import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def to_dataframe(tracks, model, albums):
    index = []
    title = []
    genre = []
    album = []
    artist = []

    for track in tracks:
        index.append(str(track['id']))
        title.append(str(track['title']))

        genre_track = model.filter(id=track['id'])[0].genre.values()
        genre_str = ''
        for i in genre_track:
            genre_str += i['name']
            genre_str += ' '
        genre.append(str(genre_str))

        album_track = model.filter(id=track['id'])[0].album
        album.append(str(album_track))

        artist_track = albums.filter(id=album_track.id)[0]
        author = artist_track.author.values()[0]['name']
        artist.append(str(author))

    dict = {
        'index': index,
        'title': title,
        'genre': genre,
        'album': album,
        'artist': artist,
        }

    df = pd.DataFrame(dict)
    # df = pd.read_csv(r"top10s.csv", encoding="ISO-8859-1")
    return df


def combined_features(row):
    return row['genre']
    # return row['title']+" "+row['artist']+" "+row['genre']+" "+row['album']


def get_count_matrix(df):
    features = ['title', 'artist', 'genre', 'album']
    # for feature in features:
    #     df[feature] = df[feature].fillna('')

    df["combined_features"] = df.apply(combined_features, axis=1)

    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df["combined_features"])

    return count_matrix


def get_index_from_title(title, df):
    return df[df.title == title]["index"].values[0]


def get_title_from_index(index, df):
    dict = {
        "id": df[df.index == index]["index"].values[0],
        "title": df[df.index == index]["title"].values[0],
        "artist": df[df.index == index]["artist"].values[0],
        "genre": df[df.index == index]["genre"].values[0],
        "album": df[df.index == index]["album"].values[0]
    }
    return dict


def get_reccomendation(tracks, model, albums, liked_tracks):
    df = to_dataframe(tracks, model, albums)
    count_matrix = get_count_matrix(df)

    cosine_sim = cosine_similarity(count_matrix)

    tracks_user_likes = []
    if len(liked_tracks) > 5:
        length = len(liked_tracks)-5
        divider = 5
    else:
        length = 0
        divider = len(liked_tracks)
    for l_t in liked_tracks[length:]:
        print(l_t['title'])
        tracks_user_likes.append(l_t['title'])

    global_arr_track = []
    print(tracks_user_likes)
    for track_user_likes in tracks_user_likes:
        track_index = get_index_from_title(track_user_likes, df)
        track_index = int(track_index)-95
        print(track_index)
        similar_tracks = list(enumerate(cosine_sim[track_index-1]))
        sorted_similar_tracks = sorted(similar_tracks, key=lambda x:x[1], reverse=True)

        i = 0
        for track in sorted_similar_tracks:
            # print(get_title_from_index(track[0], df))
            global_arr_track.append(get_title_from_index(track[0], df))
            i=i+1
            if i>int(15/divider):
                break

    wanted_items = set()
    for item in global_arr_track:
        wanted_items.add(item['id'])

    # return model.filter(pk__in=wanted_items).values()
    return wanted_items
