import os


def is_video_file(file_path):
    video_extensions = ['avi', 'mp4', 'mkv', 'mov', 'flv', 'wmv', 'webm']
    ext = file_path.split('.')[-1].lower()
    return ext in video_extensions

def add_tags(file_name, tag, extension):

    file_name_parts = file_name.split(".")
    file_name_without_extension = ".".join(file_name_parts[:-1])
    return f"{file_name_without_extension}_{tag}.{extension}"


def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory created at {path}")
    else:
        # print(f"Directory already exists at {path}")
        pass