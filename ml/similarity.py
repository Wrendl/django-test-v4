import pandas as pd
import numpy as np
from audio_library.views import TrackView

track = TrackView()

print(track.get_queryset())

index = []
title = []
genre = []
album = []

dict = {
    'index': index,
    'title': title,
    'genre': genre,
    'album': album,
    }

df = pd.DataFrame(dict)