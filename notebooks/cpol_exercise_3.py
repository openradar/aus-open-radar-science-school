for sw in range(radar.nsweeps):
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    ax = ax.ravel()

    display.plot_ppi('velocity', ax=ax[0], sweep=sw, cmap='pyart_NWSVel', gatefilter=gf, vmin=-26, vmax=26)
    display.plot_ppi('corrected_velocity', ax=ax[1], sweep=sw, cmap='pyart_NWSVel', vmin=-26, vmax=26)

    for myax in ax:
        display.plot_range_rings([50, 100, 150], ax=myax)
        myax.set_aspect(1)  # I like my axes square.
        myax.set_xlim(-150, 150)
        myax.set_ylim(-150, 150)

    fig.tight_layout()
plt.show()