import os


def process(dirs):
    media = os.listdir(dirs)
    for name in media:
        print(name)
        os.rename(os.path.join(dirs, name), os.path.join(dirs, name.replace("-", "_")))


process("medias")
process("interactive_task_image")
