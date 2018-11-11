#define out grid
grid_shape  = (41, 141, 141)
grid_limits = ((0, 20000), (-70000.0, 70000.0), (-70000.0, 70000.0))  #500m vertical, 1000m horz
grid_roi    = 1500

#define the height of the 0C and -20C level for the Maximum Estimated Size of Hail (MESH) algorthim.
fz_altitude      = 3982 #m
minus20_altitude = 7215 #m

# Function which generates a plot for each sweep
def animate_mesh(nframe):
    plt.clf()
    
    #grid reflectivity field from volume
    grid = pyart.map.grid_from_radars(
        radar_list[nframe],
        grid_shape = grid_shape,
        grid_limits = grid_limits,
        roi_func='constant', constant_roi = grid_roi,
        fields=['DBZH'],
        control_scale=True)

    #calculate mesh
    mesh_fields = calc_mesh.main(grid, [fz_altitude, minus20_altitude], 'DBZH')
    
    #setup plot
    lon_grid  = mesh_fields['longitude']['data'][0,:,:]
    lat_grid  = mesh_fields['latitude']['data'][0,:,:]
    mesh_grid = mesh_fields['MESH']['data']
    
    #mask values below 10mm of MESH
    mesh_grid[mesh_grid==0] = np.NaN
    
    #calculate the maximum mesh value
    max_mesh = round(np.nanmax(mesh_grid))
    
    #annotate plot
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=0))
    ax.coastlines('10m')
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=2, color='gray', alpha=0.5, linestyle='--')
    #set plot limits
    ax.set_extent([lon_grid.min(), lon_grid.max(), lat_grid.min(), lat_grid.max()])
    #plot mesh
    im = ax.pcolormesh(lon_grid, lat_grid, mesh_grid, vmin=0, vmax=50)  
    #plot label of maximum mesh in upper left (using lat/lon)
    plt.text(152, -27.15, 'Hail Size: '+ str(max_mesh) + 'mm',
             horizontalalignment='left',
             transform=ccrs.PlateCarree(central_longitude=0))
    #plot colorbar
    cb = plt.colorbar(im)
    cb.set_label('Maximum Estimated Size of Hail')
    
    
#Generate animation
fig = plt.figure(figsize=(10, 8))
anim = animation.FuncAnimation(fig, animate_mesh, frames=len(radar_list))
#Save animation to gif
anim_name = 'mesh_animation_' + datetime.now().strftime('%H%M%S') +'.gif'
anim.save(anim_name, writer='imagemagick', fps=2)
plt.close()
#show gif in notebook
HTML('<img src="' + anim_name + '">')   
