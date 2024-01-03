import gzip

# Data to be compressed
data = b"Lorem ipsum dolor sit amet, consectetur adipiscing elit."

with gzip.open('compressed_file.gz', 'wb') as f:
    f.write(data)

print("File compressed successfully.")
