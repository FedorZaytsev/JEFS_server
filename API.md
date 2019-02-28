# JEFS Server


## API

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
		"breakfast": [
			{
				"name": string,
				"description": string,
				"link": string,
				"picture": string,         #url
			}
		],
		"lunch": [
			...
		],
		"dinner": [
			...
		]
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

