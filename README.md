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
 - `sample_data/` - ML models and some test data for the models
 - `server225/`
   - `settings.py` - settings for the server
   - `urls.py` - file with API intro points
   - `wsgi.py` - pregenerated wsgi file
 - `storage/` - storage subproject
   - `migrations/` - automatically generated information for DB migration
   - `admin.py` - code for admin model
   - `apps.py` - empty file
   - `create_toy_data.py` - This file extracts some toy data from the Recipes API so to test our methods without
getting charged for sending requests in the API.
   - `main.py` - main file for testing ML models
   - `places.py` - Google Places & Weather API implementation
   - `recipes.py` - This file collects and parses recipes. It accesses several endpoints from the Spoonacular Recipes API to retrieve meal plans by calories, random recipes to show to the user and detailed information about recipes like ingredients, nutrition, cuisines etc.
   - `recommend_helper.py` - This file implements our main recommendation algorithm. It calculates the user BMR based on user manual input (age, height, weight etc), it creates the feature vocabulary for our Vector Space Model (VSM), it builds the VSMs for recipes and the user, it computes cosine similarity between vectors and it finds the k most similar recipe VSMs to the user VSM.
   - `recommendations.py` - This file just runs the whole recommendations pipeline by calling methods
from the recommend_helper.py file.
   - `urls.py` - table with API entries
   - `views.py` - view for the DB

  - `.gitignore` - file to ignore for git
  - `API.md` - description of API
  - `README.md` - this file
  - `db.sqlite3` - database template
  - `manage.py` - pregenerated file for managing server by Django

