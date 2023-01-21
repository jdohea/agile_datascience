import requests

if __name__=='__main__':
    data= {
    "text": "movie_id1,movieid_2,movie_id3",
    }
    response = requests.post("http://104.47.164.128:8088/get_movie",json=data)
    print(response.text)