#
# (c) 2023 Michael Fitzgerald (mpfitz@ucla.edu)
#
# Some code for querying Vizier for catalog to construct a CMD.
#
import numpy as np

from astroquery.vizier import Vizier
from numpy import dtype

Vizier.ROW_LIMIT = 1000

catalog = Vizier.get_catalogs('J/AJ/133/1658/acssggc')

catalogs = Vizier.get_catalogs(catalog.keys())
print(catalogs)
for table_name in catalog.keys():
    table = catalog[table_name]

v = Vizier(columns=["_RAJ2000", "_DEJ2000", "V-I",
                    "Vmag"])
v.ROW_LIMIT = -1
cluster = v.query_object("NGC 7089", catalog =["J/AJ/133/1658/acssggc"])



#Vizier.ROW_LIMIT = 1000
#Vizier.ROW_LIMIT = -1 # get all sources

#V magnitude vs. V-I color
# parse the result to get the source list

vi =cluster[0]["V-I"]
vmag = cluster[0]["Vmag"]
print(vi, vmag)
#V_I.append(vi)
#Vmag.append(vmag)


# plot the color-magnitude diagram
import matplotlib.pyplot as plt
import pylab
fig = plt.figure(0)
#fig.clear()
ax = fig.add_subplot(111)

ax.scatter(vi, vmag,
           marker='.',
           c='k',
           s=1., # experiment with marker size
           )
# plot title and axes labels
plt.title("Color-Magnitude Diagram for M2")
plt.xlabel("V-I Color (mag)")
plt.ylabel("V magnitude (mag)")
# invert the y axis
ax.invert_yaxis()

plt.draw()
plt.show()
fig.savefig('hw4prob2.pdf', dpi=300)

