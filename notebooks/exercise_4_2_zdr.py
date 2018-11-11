#plotting
fig, axes = plt.subplots(2, 2, subplot_kw=dict(projection=projection), figsize=(16, 16))
display = pyart.graph.RadarMapDisplayCartopy(my_radar)

#Differential Reflectivity
display.plot_ppi_map('DBZH', 0,
                        projection=projection, colorbar_flag=False,
                        min_lon=min_lon, max_lon=max_lon, min_lat=min_lat, max_lat=max_lat,
                        vmin=-8, vmax=70, cmap=pyart.graph.cm_colorblind.HomeyerRainbow,
                        resolution='10m', ax=axes[0][0])
cb = plt.colorbar(display.plots[0], ax=axes[0][0])
cb.set_label('Reflectivity (dBZ)', fontsize=16)

#Differential Reflectivity
display.plot_ppi_map('ZDR', 0,
                        projection=projection, colorbar_flag=False,
                        min_lon=min_lon, max_lon=max_lon, min_lat=min_lat, max_lat=max_lat,
                        vmin=-1, vmax=10, cmap=pyart.graph.cm_colorblind.HomeyerRainbow,
                        resolution='10m', ax=axes[0][1])
cb = plt.colorbar(display.plots[1], ax=axes[0][1])
cb.set_label('Differential Reflectivity (dB)', fontsize=16)

#Differential Reflectivity
display.plot_ppi_map('DBZH', 6,
                        projection=projection, colorbar_flag=False,
                        min_lon=min_lon, max_lon=max_lon, min_lat=min_lat, max_lat=max_lat,
                        vmin=-8, vmax=70, cmap=pyart.graph.cm_colorblind.HomeyerRainbow,
                        resolution='10m', ax=axes[1][0])
cb = plt.colorbar(display.plots[2], ax=axes[1][0])
cb.set_label('Reflectivity (dBZ)', fontsize=16)

#Differential Reflectivity
display.plot_ppi_map('ZDR', 6,
                        projection=projection, colorbar_flag=False,
                        min_lon=min_lon, max_lon=max_lon, min_lat=min_lat, max_lat=max_lat,
                        vmin=-1, vmax=10, cmap=pyart.graph.cm_colorblind.HomeyerRainbow,
                        resolution='10m', ax=axes[1][1])
cb = plt.colorbar(display.plots[3], ax=axes[1][1])
cb.set_label('Differential Reflectivity (dB)', fontsize=16)

plt.show()
