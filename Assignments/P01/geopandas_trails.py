import geopandas as gpd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
#import contextily as ctx

'''
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, flash, url_for, redirect, render_template

app = Flask(__name__)
database_uri = "postgresql://postgres:1234@localhost:5432/Project1?gssencmode=disable"
app.config ['SQLALCHEMY_DATABASE_URI'] = database_uri
'''
from flask import Flask, request, flash, url_for, redirect, render_template
database_uri = "postgresql://postgres:1234@winhost:5433/Project1?gssencmode=disable"
app = Flask(__name__)
def disply():
    engine = create_engine(database_uri)
    sql = "SELECT geom as geom FROM public.ufo"
    ufos = gpd.GeoDataFrame.from_postgis(sql, engine , geom_col="geom")
    ufos.crs = "EPSG:4326"
    #countries = gpd.read_file("countries.geojson")
    fig, ax = plt.subplots(figsize=(14,12))
    ufos.sample(150).to_crs(epsg=3857).plot(ax=ax, color="red", edgecolor="white")
    #ctx.add_basemap(ax, url=ctx.providers.Stamen.TonerLite)
    plt.title("UFO sightings")
    ax.axis("off")
    plt.show()

@app.route("/")
def hello():
    return {"use one of these : ":["findAll", "findOne", "findClosest"]}

@app.route("/findAll")    
def get_all():
    engine = create_engine(database_uri)
    sql = "SELECT * FROM public.ufo"
    ufos = gpd.GeoDataFrame.from_postgis(sql, engine , geom_col="geom")
    ufos.crs = "EPSG:4326"
    return ufos.__geo_interface__

@app.route("/findOne/<string:geo_location>/")
def getOne(geo_location):
    #geo_location = "Bismarck"
    engine = create_engine(database_uri)
    sql = "SELECT * FROM public.ufo where city='%s'" % (geo_location.strip())
    ufos = gpd.GeoDataFrame.from_postgis(sql, engine , geom_col="geom")
    ufos.crs = "EPSG:4326"
    return ufos.__geo_interface__

def extract(obj):
    temp = str(obj)
    temp = temp.split(" ")
    temp = [i for i in temp if i]
    num = temp[1].split("\n")[0].strip()
    return float(num)

@app.route("/findClosest/<string:geo_location>/")
def getClosest(geo_location):
    engine = create_engine(database_uri)
    sql = "SELECT * FROM public.ufo where city='%s'" % (geo_location.strip())
    ufos = gpd.GeoDataFrame.from_postgis(sql, engine , geom_col="geom")
    ufos.crs = "EPSG:4326"
    if len(ufos)>1:
        ufos = ufos[0]
    lat = extract(ufos["lat"])
    lon = extract(ufos["lon"])

    print("============")
    print(lat,lon)

    sql = '''
    SELECT *, ST_Distance(ST_MakePoint(%s,%s ), geom) AS dist
    FROM ufo
    ORDER BY dist LIMIT 3;
    '''%(str(lat), str(lon))
    ufos = gpd.GeoDataFrame.from_postgis(sql, engine , geom_col="geom")
    ufos.crs = "EPSG:4326"

    return ufos.__geo_interface__



if __name__ == "__main__":
    app.run()
    disply()


