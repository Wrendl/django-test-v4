for j, i in enumerate(arr):
    print(j + 1, i[0], i[1])

    b = models.Album(name=str(i[0]), description='1', cover=get_default_cover())
    b.save()

    a = models.Artist.objects.get(name=i[1])
    b.author.add(a)