from os import path, rename, walk

if __name__ == '__main__':

    missing_cases = []
    file_path = []

    with open('missing.txt') as files:
        missing_cases = files.read().split()

    BASE_PATH = path.join(
        path.dirname(path.abspath(path.dirname(__file__))),
        "archived_responses"
    )

    for dirpath, subdirs, files in walk(BASE_PATH):
        for x in files:
            file_path.append(path.join(dirpath, x))

    new_path = path.join(
        path.dirname(path.abspath(path.dirname(__file__))), "responses"
    )

    common = []

    for i in file_path:
        file_name = i.split('/')[-1].partition('.')[0]
        if file_name in missing_cases:
            new_file_path = path.join(new_path, file_name + ".html")
            rename(i, new_file_path)
