dphi = cpol_helper.texture(radar.fields['differential_phase']['data'])
radar.add_field_like('differential_phase', 'differential_phase_texture', dphi)

display.plot_ppi('differential_phase_texture', vmin=0, vmax=150, cmap='jet')
plt.axes().set_aspect(1)
plt.show()

plt.hist(radar.fields['differential_phase_texture']['data'].flatten(), range=[0, 40], bins=40)
plt.xlabel('$\phi_{dp}$ texture')
plt.ylabel('PDF')
plt.show()

gf.exclude_above('differential_phase_texture', 20)