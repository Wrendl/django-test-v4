import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from base.services import get_default_avatar, get_default_cover


def get_data(models):
    df = pd.read_csv(r"C:\Users\aishu\Desktop\DB Tracks - Sheet1.csv", encoding="ISO-8859-1")

    arr = []
    for i in range(len(df['Album Name'])):
        arr.append([df['Song name'][i], df['Album Name'][i], df['Genre'][i], df['Play count'][i]])

    for j, i in enumerate(arr):
        print(j + 1, i[0], i[1], i[2], i[3])

        name2 = str(i[1]).strip()
        print(name2)
        a = models.Album.objects.get(name=name2)
        print(a)

        name1 = str(i[0]).strip()
        print(name1)
        play_cnt = int(i[3])
        b = models.Track(title=name1, album_id=a.id, plays_count=play_cnt, file=r"C:\Users\aishu\Desktop\songs\01 Ashè - Moral of the Story.mp3")
        b.save()

        genres = i[2].split(', ')
        print(genres)
        for genre in genres:
            genre = str(genre).strip()
            c = models.Genre.objects.get(name=genre)
            b.genre.add(c)

        name2 = str(i[1]).strip()
        print(name2)
        a = models.Album.objects.get(name=name2)
        print(a)
        # b.album.add(a)

