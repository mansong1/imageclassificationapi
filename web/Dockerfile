FROM python:3.7.11-slim-stretch

# Create a working directory
WORKDIR /app

# Copy source code to working directory
COPY . .
COPY requirements.txt ./

# hadolint ignore=DL3013
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python" ]

# Run app.py at container launch
CMD [ "app.py" ]