#
# (c) 2023 Michael Fitzgerald (mpfitz@ucla.edu)
#
# Some code for querying the virtual observatory to make finder charts
#
import logging

import pyvo as vo
import matplotlib as mpl
import numpy as np
from PIL import Image, ImageDraw

import matplotlib.pyplot as plt
import pylab
from astropy.io import fits
from astropy import units as u
import astropy.coordinates as coord
from astropy.coordinates import SkyCoord
from astropy.utils.data import download_file
from IPython.display import Image as ipImage, display
import warnings
import logging as _log
from astroquery.simbad import Simbad


c = SkyCoord(ra=10.625*u.degree, dec=41.2*u.degree, frame='icrs')

#logger/exception for bodies not in SDSS !
warnings.filterwarnings("ignore", module="astropy.io.votable.*")
warnings.filterwarnings("ignore", module="pyvo.utils.xml.*")
# set up VO service for DSS image retrieval
# automatically retrieve the DSS g-band image of the source
target_list = ['M2',
               #'M45',
               #'HD 189733',
               '3C 273',
               'NGC 1068',
               #'AU Mic',
               'TRAPPIST-1'
               ]
coords_arr = []

for target_name in target_list:
    coords = coord.SkyCoord.from_name(target_name)
    #print(coords)
    coords_arr.append(coords)
    services = vo.regsearch(servicetype='image', keywords=['sloan'], waveband='optical')
    services.to_table()[np.where(np.isin(services.to_table()['short_name'], 'SDSSDR7'))]['ivoid', 'short_name']
    jhu_dr7_service = [s for s in services if 'SDSS' in s.short_name and 'jhu' in s.ivoid][0]

    sdss_table_jhu = jhu_dr7_service.search(pos=coords, size=0.2, format=None)
    sdss_table_jhu.to_table().show_in_notebook(display_length=5)
    url = sdss_table_jhu[0].getdataurl()
    print(url)
    img = ipImage(url=sdss_table_jhu[0].getdataurl())
    display(img)

    file_name = download_file(sdss_table_jhu[1].getdataurl(), cache=True, timeout=600)
    hdu_list = fits.open(file_name)

    plt.imshow(hdu_list[0].data, cmap='binary', origin='lower', vmax=1200, vmin=1010)
    #plt.show()

print(coords_arr)
# set up VO service for IRSA 2MASS point-source catalog retrieval
# query for "bright" point sources in the region, adjust cutoff & find J-band mag limit
# for each source show image & overplot the point sources
# loop over sources
def get_point_sources(ra, dec):
    service = vo.dal.TAPService('https://irsa.ipac.caltech.edu/TAP')

    result = service.run_async("""
            SELECT ra,dec,j_m,j_msigcom,h_m,h_msigcom,k_m,k_msigcom,ph_qual,cc_flg
            FROM fp_psc
            WHERE CONTAINS(POINT('ICRS', ra, dec), CIRCLE('ICRS',{},{},0.1))=1 and 
            bmag < 14
            """.format(ra, dec))
    tab = result.to_table()
    coordinates = {}
    ra = tab[0]["RA"]
    print(ra)

    dec = tab[0]["DEC"]
    coordinates[target_name] = (ra, dec)
    # sort dictionary by the "value" (ra,dec)


    target_info = dict(sorted(coordinates.items(), key=lambda x: x[1]))
    return tab, target_info

print(coords_arr)

#Bmag < 14 for "bright" sources


for target_name in target_list:
    _log.debug('querying {}'.format(target_name))
    result_table = Simbad.query_object(target_name)
    print(result_table)

    n_result = len(result_table)
    _log.info('{}: {} objects found'.format(target_name, n_result))
    if n_result == 0:
        _log.warning('skipping....')
        continue
    if n_result > 1:
        _log.warning('using first result')

# compute object coordinates
    #convert ra, dec to pixels for plotting: i unfortunately ran out of time to figure out how to do this step
# retrieve image


# retrieve point sources


# set up figure
fig = pylab.figure(0)
fig.clear()
ax = fig.add_subplot(111)

# display image
ax.imshow(imdata,
    cmap=mpl.cm.gray,
    interpolation='nearest',
    )

# display point sources
ax.scatter()


# annotate
plt.title("")

# save figure
plt.savefig("hw4prob3_image.png")