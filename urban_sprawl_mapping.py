import os
from pathlib import Path

import geopandas as gp
import pandas as pd
import pandas_bokeh # noqa
from bokeh import palettes

census_file = Path('data/census/US_tract_2010.shx')
sprawl_file = Path('data/sprawl/sprawl indices2010_censustract - Jacksonville.csv')
joined_file = Path('data/joined/joined.geojson')

joined_cols = ['fips', 'geometry', 'compositeindex2010']


if joined_file.exists() and not os.environ.get('FORCE_RECOMPUTE'):
  joined = gp.read_file(joined_file)

else:
  census_tracts = gp.read_file(census_file)
  sprawl_info = pd.read_csv(sprawl_file, dtype={'fips': str})

  joined = census_tracts.merge(
    sprawl_info,
    how='inner',
    left_on='GEOID10',
    right_on='fips',
  )
  joined.to_file(joined_file, driver='GeoJSON')


pandas_bokeh.output_file('index.html')

joined.plot_bokeh(
  dropdown=joined_cols[-1:],
  tile_provider='STAMEN_TONER',
  line_alpha=0.25,
  fill_alpha=0.25,
  colormap=palettes.magma(4),
  colormap_range=(0, 150),
)
