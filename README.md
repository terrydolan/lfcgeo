# lfcgeo
lfcgeo is a web app that maps each LFC squad player's shortest journey from their birthplace to Anfield, for a selected season.

The app illustrates the changing nature of top flight football in England. You can see that most of the players from Liverpool's first squad in 1892-1893 came from Scotland. Indeed that team was known as the '*team of macs*'! Liverpool's 2020-2021 squad is truly global, with players from 19 different countries who have travelled over 42,000 miles to reach Anfield.

The app has knowledge of 800+ Liverpool players over 100+ seasons.

## Try the app
The lfcgeo app is deployed at [lfcgeo.herokuapp.com](https://lfcgeo.herokuapp.com). It is also available from [lfcgeo.lfcsorted.com](http://lfcgeo.lfcsorted.com).

## App user experience
The app maps each LFC season squad player's shortest journey from their birthplace to Anfield using a 'great-circle' line of shortest distance. You can select the season to map using a slider. Any LFC season can be selected, from 1892-1892 to the current season. The default selection is 1962-1963, teh season Shankly's Liverpool team returned to the top flight.

The generated line from a player's birthplace to Anfield is interactive, if you 'hover' over the line then that player's journey details are displayed. You can also zoom in and out of the map. For example you can zoom in to Anfield to see the player's from Liverpool in a given season; or you can zoom out to the world view. The selected season's dataframe is also available to view below the map.

## Data source
The LFC squad and player data is sourced from the excellent[www.lfchistory.net](http://www.lfchistory.net).

## Data analysis and app prototyping
The data was cleansed, enriched and mapped using jupyter, python, pandas, geopy and pydeck with mapbox. The geo-location of each player's bithplace is determined using pydeck's geocode with openstreetmap's Nominitum API.

If more than one player in a squad in a given season share the same geo-location origin then the location is transformed, placing each transformed point around a circle with radius 0.5 km from the origin. This ensures that each player's line is distict on the map.

## App construction and deployment
The app uses python, pandas, ast, pydeck (with mapbox) and streamlit and is deployed on the heroku cloud application platform. 

## App source code
See lfcgeo_app.py on the [lfcgeo repository on github](https://github.com/terrydolan/lfcgeo).

## Licence
MIT. 

## Acknowledgements
Thanks to the providers of the tools and data.

## Feedback
Your feedback and improvement suggestions are welcome.

  
Terry Dolan, @lfcsorted  
blog: www.lfcsorted.com
