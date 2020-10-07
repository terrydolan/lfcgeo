# lfcgeo
lfcgeo is a web app that maps each LFC squad player's shortest journey from their birthplace to Anfield, for a selected season.

The app illustrates the changing nature of top flight football in England. You can see that most of the players from Liverpool's first squad in 1892-93 came from Scotland. Indeed that team was known as the '*team of macs*'. Liverpool's 2020-21 squad is truly global, with players from 19 different countries who have travelled over 42,000 miles to reach Anfield.

The app has knowledge of every player that has been included in an LFC squad; that is 100+ seasons and 800+ players.

## Try the app
The lfcgeo app is deployed at [lfcgeo.herokuapp.com](https://lfcgeo.herokuapp.com). It is also available from [lfcgeo.lfcsorted.com](http://lfcgeo.lfcsorted.com).

## App user interface
The app maps each LFC season squad player's journey from their birthplace to Anfield using a 'great-circle' line of shortest distance. You can select the season to map using a slider. Any LFC season can be selected, from 1892-1893 to the current season. The default selection is 1900-01, Liverpool's first title winning season.

The generated line from a player's birthplace to Anfield is interactive, if you 'hover' over the line then that player's journey details are displayed. You can also zoom in and out of the map. For example you can zoom in to Anfield to see the player's from Liverpool in a given season; or you can zoom out to the world view. The selected season's dataframe is also available to view below the map.

## Animation
The 'painting the world red' animation - available from the navbar - gives an alternative view of the data. Each animation 'frame' is a season, from 1892-93 to 2020-21. A country is painted red on the map in a season when a player born in that country appears in the LFC squad for the first time.

## Primary data source
The LFC squad and player data is sourced from the excellent [www.lfchistory.net](http://www.lfchistory.net). 

## Data preparation and app prototyping
The data was cleansed, enriched and mapped using jupyter, python, pandas, geopy and pydeck with mapbox. The geo-location of each player's bithplace is determined using geopy's geocode with openstreetmap's Nominatim API.

If more than one player in a squad in a given season share the same geo-location origin then the location is transformed, placing each transformed point around a circle with radius 0.5 km from the origin. This ensures that each player's line is distict on the map, though you may need to zoom in!

## App components and deployment
The app uses python, pandas, ast, logging, pydeck (with mapbox) and streamlit and is deployed on the heroku cloud application platform.

## App source code
See lfcgeo_app.py on the [lfcgeo repository on github](https://github.com/terrydolan/lfcgeo).

## Licence
MIT. 

## Acknowledgements
Thanks to the providers of the tools and data.

## Feedback
Your feedback and improvement suggestions are welcome.

  
Terry Dolan, @lfcsorted  
blog: [www.lfcsorted.com](http://www.lfcsorted.com)
