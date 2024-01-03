MIDDLEWARE = [
    # ... other middleware
    'django.middleware.gzip.GZipMiddleware',
]


GZIP_CONTENT_TYPES = ['application/json']  # Add any content types you want compressed
GZIP_MIN_LENGTH = 500  # Minimum response size to trigger compression

GZIP_COMPRESSOR = 'django.core.compression.GZipCompressor'  # Default compressor
