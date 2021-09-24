import json
import os, requests
import logging
import time

import concurrent.futures


def request_file(thread_idx):
    global THREAD_COUNT, FILES, BASE_URL, OUTPUT
    for i in range(THREAD_COUNT):

        try:
            with open(FILES[i * THREAD_COUNT + thread_idx], "rb") as a_file:
                file_dict = {"file": a_file}
                response = requests.post(BASE_URL+"dxf_to_json", files=file_dict)

                a_dict = json.load(response.text)

                file_name = a_dict["name"]
                # file_content = a_dict["geometry_data"]

                with open(OUTPUT+"/"+file_name.replace(".dxf", ".json"), 'w') as a_json:
                    json.dump(a_dict, a_json)

                # with open(OUTPUT+"/"+file_name, 'w') as a_dxf:
                #     a_dxf.write(''.join(
                #         [line.replace('\\n', '\n').replace('\\', '')
                #          for line in a_file.readlines()])[2:-1])

                # print(thread_idx, i)
                # print(response)

        except Exception as e:
            print(e)


def multi_threaded_stress_test(file_dir, output_test_data, url, port):
    start_time = time.time()

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    global FILES, THREAD_COUNT, BASE_URL, OUTPUT
    FILES = []
    THREAD_COUNT = 10
    BASE_URL = "http://"+str(url)+":"+str(port)+"/"
    OUTPUT = output_test_data
    # r=root, d=directories, f = files
    for r, d, f in os.walk(file_dir):
        for file in f:
            if '.dxf' in file:
                FILES.append(os.path.join(r, file))


    with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
        executor.map(request_file, range(THREAD_COUNT))

    return "running {} files through {} threads took {} seconds".format(
        len(FILES), THREAD_COUNT, time.time()-start_time)