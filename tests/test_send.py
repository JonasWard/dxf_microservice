import requests

API_URL = 'http://localhost:1338/'


def send_local_file(path):

    return requests.post('{}data/import'.format(API_URL), files={'file': open(path, 'r')})


if __name__ == "__main__":
    path = '../test_data/1-100_ModelTest.dxf'

    # with open(path, 'r') as a_dxf:
    #     print(len(a_dxf))

    response = send_local_file(path)

    print(response.content)
