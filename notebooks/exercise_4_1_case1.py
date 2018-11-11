#Specific the radar and date we want to download
radar_id     = 2 
date         = '2009/02/07'
start_str    = '2009/02/07 07:00' #time in UTC
end_str      = '2009/02/07 08:00' #time in UTC
tilt         = 1 #second tilt!
field        = 'DBZH' #reflectivity

#parse inputs
radar_id_str = str(radar_id).zfill(2)
date_dt      = datetime.strptime(date,'%Y/%m/%d')
#build request filename url
tar_fn       = radar_id_str + '_' + date_dt.strftime('%Y%m%d') + '.pvol.tar'
request_url  = '/'.join([base_url, radar_id_str, date_dt.strftime('%Y'), 'vol', tar_fn])
#download the tar file
if not os.path.isfile(tar_fn):
    urllib.request.urlretrieve(request_url, tar_fn)
#extract the tar file to a temporary directory
temp_dir = tempfile.mkdtemp()
tar = tarfile.open(tar_fn)
tar.extractall(path = temp_dir)
tar.close()
#list all the volumes extracted from the tar file
file_list = sorted(glob(temp_dir + '/*'))
#print('\n'.join(file_list)) #print with newline between each list item


#first convert the start/end time strings into datetime numbers
start_dt  = datetime.strptime(start_str, '%Y/%m/%d %H:%M')
end_dt    = datetime.strptime(end_str, '%Y/%m/%d %H:%M')
#now let's read the datetime numbers of all the volumes for comparision
file_dt_list = []
for i, fname in enumerate(file_list):
    file_dt_list.append(datetime.strptime(os.path.basename(fname)[3:18],'%Y%m%d_%H%M%S'))
#find the index of volumes within our start and end times
file_dt_array = np.array(file_dt_list)
index_array = np.where(np.logical_and(file_dt_array >= start_dt, file_dt_array<=end_dt))[0]

#build list of radar objects to plot
radar_list = []
for index in index_array:
    #get file name of index
    file_name = file_list[index]
    #open volume using pyart
    my_radar = pyart.aux_io.read_odim_h5(file_name, file_field_names=True)
    #clean up field metadata
    my_radar.fields['DBZH']['standard_name'] = 'Reflectivity'
    my_radar.fields['DBZH']['units'] = 'dBZ'
    my_radar.fields['DBZH']['long_name'] = 'Radar Reflectivity Factor'
    #append to radar list for animation later
    radar_list += [my_radar]

#determine plot domains
radar_lat = my_radar.latitude['data'][0]
radar_lon = my_radar.longitude['data'][0]
min_lat   = radar_lat - 1.0
max_lat   = radar_lat + 1.0
min_lon   = radar_lon - 1.5
max_lon   = radar_lon + 1.5

# Set up the GIS projection
projection = ccrs.Mercator(
                central_longitude=radar_lon,
                min_latitude=min_lat, max_latitude=max_lat)

#Generate animation
fig = plt.figure(figsize=(16, 12))
anim = animation.FuncAnimation(fig, animate_reflectivity, frames=len(radar_list))
#Save animation to gif
anim_name = '_'.join(['dbzh_animation', radar_id_str, datetime.now().strftime('%H%M%S')]) +'.gif'
anim.save(anim_name, writer='imagemagick', fps=2)
plt.close()
#show gif in notebook
HTML('<img src="' + anim_name + '">')
