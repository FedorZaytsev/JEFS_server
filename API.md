# JEFS Server


## API

### Create User
Creates user. No pass for now

`PUT /user/<user_id>`

```
{
	"name": string,
	"weight": float,
	"height": float,
	"bmigoal": float,
	"gender": string,
	"age": int,
	"ethnicity": string,
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
	"weight": float,
	"height": float,
	"bmigoal": float,
	"gender": string,
	"age": int,
	"ethnicity": string,
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

`GET /user/<user_id>/recommendations/recepies`

Answer format:

```
{
	"monday": {
		"breakfast":
			{	#recipe object
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
				  "vegetarian" : false
			}
		,
		"lunch": {
			...
		},
		"dinner": {
			...
		}
	},
	"tuesday": {
		...
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

