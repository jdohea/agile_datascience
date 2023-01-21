FROM python:3.9-slim

EXPOSE 8501

WORKDIR /streamlit

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/2022ADS-3/streamlit.git .

RUN pip install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=6969", "--server.address=0.0.0.0"]
