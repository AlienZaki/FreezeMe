import requests
from io import BytesIO, BufferedReader
from urllib.parse import urlparse

file_url = 'https://nyc3.digitaloceanspaces.com/freeze-me-space/media/uploads/Driver/driver_546970825.pdf?sdfsdf'
file_name = file_url.split('/')[-1].split('?')[0]
print(file_name)