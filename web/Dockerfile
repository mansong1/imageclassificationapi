FROM python:3.7.7-slim-stretch

# Create a working directory
WORKDIR /app

# Copy source code to working directory
COPY app.py /app/
COPY classify_image.py /app/
COPY requirements.txt /app/
COPY model_data/boston_housing_prediction.joblib /app/model_data/

# hadolint ignore=DL3013
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose port 80
EXPOSE 80

ENTRYPOINT [ "python" ]

# Run app.py at container launch
CMD [ "app.py" ]