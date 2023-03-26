import folium as folium
from datetime import date
import io
from PIL import Image
import selenium



def createMap(username, df):
    

    m = folium.Map(location=[40,-4],zoom_start=2,width=700,height=500,control_scale=True, tiles='CartoDB Positron')
    folium.TileLayer('stamenterrain').add_to(m)
    folium.LayerControl().add_to(m)

    circles = []

    dfMap = df.loc[df['lugar'] != '']
    if not dfMap.empty:
        dfMap.apply(lambda row: folium.Circle(location=[row.loc['lugar'][1][1], row.loc['lugar'][1][0]],
                                                radius=1000,
                                                popup=row.loc['lugar'][0],
                                                fill=True, 
                                                tooltip=row.loc['Fecha_creación'], opacity=0.5)
                                                    .add_to(m), axis=1)

        mapName = 'funcionalities//Maps//' + username + str(date.today())
        img_data = m._to_png(5)
        img = Image.open(io.BytesIO(img_data))
        img.save(mapName + '.png')