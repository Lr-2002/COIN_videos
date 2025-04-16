import os

media = os.listdir("./medias/")
for name in media:
    print(name)
    os.rename("./medias/" + name, "./medias/" + name.replace("-", "_"))
