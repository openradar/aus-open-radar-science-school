zdr = radar.fields['differential_reflectivity']['data']
phidp = radar.fields['corrected_differential_phase']['data']
nzdr = 0.016 * phidp + zdr  # ;-)
radar.add_field_like('differential_reflectivity', 'corrected_differential_reflectivity', nzdr)