import os, requests
import logging
import threading
import time
import concurrent.futures

global file_dir
file_dir = "../test_data"


def request_file(thread_idx):
    global THREAD_COUNT, files
    for i in range(THREAD_COUNT):
        with open(files[i * THREAD_COUNT + thread_idx], "rb") as a_file:
            file_dict = {"file": a_file}
            response = requests.post("http://localhost:1338/data/import", files=file_dict)
            print(thread_idx, i)
            print(response)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    global files
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(file_dir):
        for file in f:
            if '.dxf' in file:
                files.append(os.path.join(r, file))

    print(files)

    THREAD_COUNT = 10

    with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
        executor.map(request_file, range(THREAD_COUNT))