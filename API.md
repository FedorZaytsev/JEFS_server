# JEFS Server


## API

### Create User
Creates user. No pass for now

`PUT /user/<user_id>`

```
{
	"name": string,
	"weight": float, # kg
	"height": float, # cm
	"bmigoal": float,
	"targetWeight": float, # kg
	"gender": "male" | "female" | "other" | "n/a",
	"age": int,
	"cuisine": string[],
}
```

Example:

```
PUT /user/fedorzaytsev228
{
	"name": "Fedor Zaytsev"
}
```

### Set user params
Set user params, like BMI, weight, height ...

`POST /user/<user_id>`

```
{
	"name": string,
	"weight": float, # kg
	"height": float, # cm
	"bmigoal": float,
	"targetWeight": float, # kg
	"gender": "male" | "female" | "other" | "n/a",
	"age": int,
	"cuisine": string[],
}
```


### Get User
Get information about user

`GET /user/<user_id>`


### Save location
Saves user location on the server

`PUT /user/<user_id>/storage/location`

```
{
	"longitude": float,
	"latitude": float,
}
```

### Save step count
Saves step counter on the server

`PUT /user/<user_id>/storage/stepcount` 

```
{
	"count": int
}
```

### Get recepies
Get recepies recommendations from the server

`GET /user/<user_id>/recommendations/recipes`

Answer format:

```
{ "result": {
	{
		"monday": {
			"breakfast":{	#recipe object
				"glutenFree" : false,
				"ingredients" : [
				       "arugula",
				       "baguette",
				       "basil",
				       "butter",
				       "canned tomatoes",
				       "crushed red pepper",
				       "eggs",
				       "garlic cloves",
				       "olive oil",
				       "onion",
				       "parmesan cheese",
				       "parmesan cheese",
				       "rosemary",
				       "salt and pepper",
				       "salt and pepper",
				       "thyme"
				    ],
				"id" : 640636, #id as returned from the Recipes API.
				"title" : "Creamy Egg Marinara Breakfast Dip",
				"cuisines" : [],
				"vegan" : false,
				"image" : "https://spoonacular.com/recipeImages/640636-556x370.jpg",
				"vegetarian" : false,
				"nutrition" : {
					"Carbohydrates" : 5.91,
					"Sodium" : 1054.11,
					"Protein" : 21.76,
					"Sugar" : 3.41,
					"Saturated Fat" : 24.04,
					"Calories" : 557.84,
					"Cholesterol" : 132.39,
					"Fat" : 49.89
				}
			},
			"lunch": {
				...
			},
			"dinner": {
				...
			}
		},
		"tuesday": {
			...
		},
	}
}
``` 

### Get workouts
Get workout recommendations from the server

`GET /user/<user_id>/recommendations/workouts`

Answer format:

```
{
	"monday": [
		{                               #workout object
			"name": string,
			"description": string,
			"picture": string,          #url
		},
		{
			....
		}
	],
	"tuesday": [
		...
	]
}
```


### Get cuisines:
Method to get available recepies to show to user and get their preferences

`GET /user/<user_id>/storage/recipes`

Answer format:


### Mark recipe as liked:

`POST /user/<user_id>/recipe/<recipe_id>/like`


### Save user history

`POST /user/<user_id>/profile?date=yyyy-mm-dd`

Body:
```
{
	"weigth": float,
	"height": float
}
```

### Get consumed calories:

`GET /user/<userId>/calories?from=yyyy-mm-dd&to=yyyy-mm-dd`


### Get consumed nutrients:

`GET /user/<userId>/nutrients?from=yyyy-mm-dd&to=yyyy-mm-dd`

