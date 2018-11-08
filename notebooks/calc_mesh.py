"""
MESH sub-module of pyhail

Contains the single pol MESH retrieval for gridded radar data.
Required reflectivity and temperature data

Joshua Soderholm - 15 June 2018
Modified 5 November for 2018 radar workshop (removed common libs and sounding functions)
"""

import pyart
import netCDF4
import numpy as np
import warnings

warnings.filterwarnings("ignore")

def _get_latlon(radgrid, ref_name):
    """
    Generates lattitude and longitude arrays.
    Parameters:
    ===========
    radgrid: struct
        Py-ART grid object.
    Returns:
    ========
    longitude: ndarray
        Array of coordinates for all points.
    latitude: ndarray
        Array of coordinates for all points.
	
	From cpol_processing: https://github.com/vlouf/cpol_processing
    """
    # Declare array, filled 0 in order to not have a masked array.
    lontot = np.zeros_like(radgrid.fields[ref_name]['data'].filled(0))
    lattot = np.zeros_like(radgrid.fields[ref_name]['data'].filled(0))

    for lvl in range(radgrid.nz):
        lontot[lvl, :, :], lattot[lvl, :, :] = radgrid.get_point_longitude_latitude(lvl)

    longitude = pyart.config.get_metadata('longitude')
    latitude  = pyart.config.get_metadata('latitude')

    longitude['data'] = lontot
    latitude['data']  = lattot

    return longitude, latitude

def main(grid, temph_data, ref_name):

    """
 	Hail grids adapted fromWitt et al. 1998 and Cintineo et al. 2012.
    Exapnded to grids (adapted from wdss-ii)

	Gridding set to 1x1x1km on a 20,145x145km domain

    Parameters:
    ===========
    radgrid: struct
        Py-ART grid object.
	out_ffn: string
		output full filename (inc path)
	snd_input: string
		sounding full filename (inc path)
	temph_data: list
		contains 0C and -20C altitude (m) in first and second element position, only used if snd_input is empty
    ref_name: string
        name of reflectivity field in radar object
    save_flag: logical
        if True, then save grid to file
    Returns:
    ========
    None, write to file
	
    """

    #MESH constants
    z_lower_bound = 40
    z_upper_bound = 50
    

    snd_t_0C       = temph_data[0]
    snd_t_minus20C = temph_data[1]
        
    # Latitude Longitude field for each point.
    longitude, latitude = _get_latlon(grid, ref_name)
    
    # extract grids
    refl_grid = grid.fields[ref_name]['data']
    grid_sz   = np.shape(refl_grid)
    alt_vec   = grid.z['data']
    alt_grid  = np.tile(alt_vec,(grid_sz[1], grid_sz[2], 1))
    alt_grid  = np.swapaxes(alt_grid, 0, 2) #m
    
    #calc reflectivity weighting function
    weight_ref                             = (refl_grid - z_lower_bound)/(z_upper_bound - z_lower_bound)
    weight_ref[refl_grid <= z_lower_bound] = 0
    weight_ref[refl_grid >= z_upper_bound] = 1
    
    #calc hail kenitic energy
    hail_KE = (5 * 10**-6) * 10**(0.084 * refl_grid) * weight_ref
    
    #calc temperature based weighting function
    weight_height = (alt_grid - snd_t_0C) / (snd_t_minus20C - snd_t_0C)
    weight_height[alt_grid <= snd_t_0C]       = 0
    weight_height[alt_grid >= snd_t_minus20C] = 1

    #calc severe hail index
    grid_sz_m = alt_vec[1] - alt_vec[0]
    SHI = 0.1 * np.sum(weight_height * hail_KE, axis=0) * grid_sz_m

    #calc maximum estimated severe hail (mm)
    MESH = 2.54 * SHI**0.5

    #calc warning threshold (J/m/s) NOTE: freezing height must be in meters
    WT   = 57.5 * snd_t_0C - 121

    #calc probability of severe hail (POSH) (%)
    POSH           = 29 * np.log(SHI/WT) + 50
    POSH           = np.real(POSH)
    POSH[POSH<0]   = 0
    POSH[POSH>100] = 100
    
    #add grids to grid object
    hail_KE_field   = {'data': hail_KE, 'units': 'Jm-2s-1', 'long_name': 'Hail Kinetic Energy',
                  'standard_name': 'hail_KE', 'comments': 'Witt et al. 1998'}
    
    SHI_field        = {'data': SHI, 'units': 'J-1s-1', 'long_name': 'Severe Hail Index',
                        'standard_name': 'SHI', 'comments': 'Witt et al. 1998, only valid in the first level'}
 
    MESH_field       = {'data': MESH, 'units': 'mm', 'long_name': 'Maximum Expected Size of Hail',
                        'standard_name': 'MESH', 'comments': 'Witt et al. 1998, only valid in the first level'}
 
    POSH_field       = {'data': POSH, 'units': '%', 'long_name': 'Probability of Severe Hail',
                        'standard_name': 'POSH', 'comments': 'Witt et al. 1998, only valid in the first level'}
    
    #return dictionary
    out_dict = {'hail_KE':hail_KE_field, 'SHI':SHI_field, 'MESH':MESH_field, 'POSH':POSH_field,
               'longitude':longitude,'latitude':latitude}
    return out_dict
