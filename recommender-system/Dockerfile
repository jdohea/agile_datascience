FROM python:3.9
COPY . /recommender-system/
WORKDIR /recommender-system
EXPOSE 8080
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY constants.json .
COPY start.sh .
CMD ./start.sh
# below command runs the container 
# docker run -p 80:80 repo-only
