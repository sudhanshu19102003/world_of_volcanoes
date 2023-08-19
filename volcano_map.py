import folium, pandas
from folium import plugins

basemaps = {
    'Google Maps': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Maps',
        overlay = True,
        control = True
    ),
    'Google Satellite Hybrid': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Satellite',
        overlay = True,
        control = True
    ),
    'Esri Satellite': folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = 'Esri',
        name = 'Esri Satellite',
        overlay = True,
        control = True
    )
}

data = pandas.read_csv("volcano.csv")
Latitude =list(data["Latitude"])
Longitude=  list(data["Longitude"])
Id = list(data["VolcanoID"])
Names = list(data["V_Name"])
Country = list(data["Country"])
Region = list(data["Region"])
Subregion = list(data["Subregion"])
Hazard = list(data["hazard"])
Vclass = list(data["class"])
Risk = list(data["risk"])

html="""
ID : %s<br>
I'am :<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
%s, %s, %s <br>
Hazard : %s <br>
Class : %s,<br>
Risk : %s <br>
"""

map = folium.Map(location=[18.0116917836677, 37.99229868774134],
                 zoom_start = 2,
                 tiles=""
                )

basemaps['Google Maps'].add_to(map)
basemaps['Google Satellite Hybrid'].add_to(map)
basemaps['Esri Satellite'].add_to(map)

def colors(color):
        if color == 1.0:
            return "#800080"
        elif color == 2.0:
            return "#ffd700"
        elif color == 3.0:
            return "#ff0000"
        else:
            return "#00FF00"

featur_groups = folium.FeatureGroup(name="Volcano Map")

for latitude, longitude, id, name, country, region, subregion, hazard, clas, risk in zip(Latitude, Longitude, Id, Names, Country, Region, Subregion, Hazard, Vclass, Risk):
    iframe = folium.IFrame(html=html % (id, name, name, country, region, subregion, hazard, clas, risk),
                            width=200,
                            height=100
                            )

    featur_groups.add_child(folium.Circle(radius=1000,
                                          location = [latitude, longitude],
                                           popup = folium.Popup(iframe),
                                           color=colors(risk),
                                           fill = True,
                                           fill_opacity = 0.4
                                         )
                            )

map.add_child(featur_groups)
map.add_child(folium.LayerControl())
plugins.Fullscreen().add_to(map)
map.save("World_of_Volcanos.html")
