
def check_image(file_path):
    if file_path.endswith(".jpeg") or file_path.endswith(".png") or file_path.endswith(".jpg"):
        return True
    return False


def get_name(string):
    return string.split("/")[-1]
