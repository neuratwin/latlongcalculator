from flask import Flask, request
from pyproj import Proj, transform
import sys

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    data = ""
    github_url = "github.com"
    if request.method == 'POST':
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        response = changeCoordinate(
            "The Converted Northing and Easting are -->  ", latitude,
            longitude)
        data = response

    return "<h1>Coordinate Conversion App <br/> Convert Coordinates from lat long to California coordinate System 'espg:3498'</h1>\
            <form action='/' method='post'>\
                <label for='latitude'> Enter Latitude </label>\
                    <input type='number' step='0.00001' name='latitude' placeholder='34.000'/>\
                        <lablefor='longitude'> Enter Longitude </label>\
                            <input type='number' step='0.00001' name='longitude' placeholder='-118.000'/>\
                             <input type='submit' value='submit'>  \
            </form>\
            </br></br> %s<br/> <h2> Complete Code :- <br/>  %s" % (data, github_url)


def changeCoordinates(northingfile, latlongfile):
    #California Coordinate System is 'espg:3498' refer to https://spatialreference.org/ref/?search=california
    inProj = Proj(init='epsg:3498', preserve_units=True)

    #Google uses 'espg:4326' , refer to https://spatialreference.org/ref/epsg/4326/
    outProj = Proj(init='epsg:4326')

    with open(northingfile, 'r') as file:
        content = file.read()
    content = [item for item in content.split("\n")]

    with open(latlongfile, 'w') as file:
        for items in content:
            try:
                sensorName, x1, y1 = items.split(",")
                # initialize coordinates , please note that coordinates needs to be reversed, Easting first and then Northing
                y2, x2 = transform(inProj, outProj, y1, x1)
                print(sensorName, x2, y2)
                file.write("{},{},{}\n".format(sensorName, x2, y2))
            except Exception as E:
                print(E)


def changeCoordinate(Instrument, Northing, Easting):
    #California Coordinate System is 'espg:3498' refer to https://spatialreference.org/ref/?search=california
    outProj = Proj(init='epsg:3498', preserve_units=True)

    #Google uses 'espg:4326' , refer to https://spatialreference.org/ref/epsg/4326/
    inProj = Proj(init='epsg:4326')

    x1, y1 = Northing, Easting
    # initialize coordinates , please note that coordinates needs to be reversed, Easting first and then Northing
    y2, x2 = transform(inProj, outProj, y1, x1)
    return (r"{}  {},  {}".format(Instrument, x2, y2))


#Coordinates for northing and easting are saved in file name coordinates.csv
#Transformed coordinates will be saved in file name transform.csv
# changeCoordinate(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == "__main__":
    app.run('0.0.0.0', port=8080, threaded=True)