from run import app
from utils import geo
from utils import lyft

# get ArcGIS API token
arcgis_token = geo.get_token()

# geocode address - get address from frontend
locations = geo.geocode(arcgis_token, "Empire State Building")

# get 2-legged lyft token
lyft_public_token = lyft.get_public_token()

# get cost and ETA
eta = lyft.get_eta(lyft_public_token, locations)

# get 3-legged lyft token

# request lyft

app.run(debug=True)
