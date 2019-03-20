# JEFS server

## How to start

1. Install django, googlemaps and pyowm: `pip install Django googlemaps pyowm`
2. Clone repo:
`git clone https://github.com/FedorZaytsev/JEFS_server.git && cd JEFS_server`
3. Start server: `python manage.py runserver`
4. Server is ready

Try to run something like:

Create user:
`curl -XPUT 127.0.0.1:8000/user/kekes/ -d '{"name":"Fedor Zaytsev", "weight": 70, "height": 180, "bmigoal": 2, "gender":"male", "age": 23, "ethnicity": "retard"}'`

Show recommendations:
`curl -v 127.0.0.1:8000/user/kekes/recommendations/workouts`

## Files description
 - sample_data - ML models and some test data for the models
 - server225/
   - 

