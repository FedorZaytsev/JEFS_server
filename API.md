# JEFS Server


## API

### Save location
Saves user location on the server

`POST /storage/location`

```
{
	"longitude": float,
	"latitude": float,
}
```

### Save step count
Saves step counter on the server

`POST /storage/stepcount` 

```
{
	"count": int
}
```

### Get recepies
Get recepies recommendations from the server

`GET /recommendations/recepies`

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

`GET /recommendations/workouts`

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

