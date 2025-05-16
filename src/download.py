import requests

# Define a download function that downloads a file when there is a 200 status code
def download(url, file_Path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_Path, 'wb') as file:
            file.write(response.content)
        print(f'File downloaded successfully from {url} as {file_Path}')
    else:
        print(f'Failed to download file from {url} as {file_Path}')