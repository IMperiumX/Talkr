import uuid


def unique_upload(instance, filename):
    ext = filename.split(".").pop()
    return "{}.{}".format(uuid.uuid4(), ext)


def file_upload(folder_name, instance, filename):
    return "%s/%s" % (folder_name, unique_upload(instance, filename))


def get_unique_string(length=None):
    if not length:
        return uuid.uuid4().hex
    return uuid.uuid4().hex[:length]


import subprocess


def get_thumbnail_from_video(video_path):
    # create thumbnail
    image_path = f"/tmp/{get_unique_string()}.jpg"
    time = "00:00:00.000"

    subprocess.call(
        ["ffmpeg", "-i", video_path, "-ss", time, "-vframes", "1", image_path]
    )
    return image_path
