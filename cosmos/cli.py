import os
import json
import click

from cosmos import Data


def validate_filename(ctx, param, value):
    if os.path.dirname(value) and not os.path.isdir(os.path.dirname(value)):
        print('No such directory: {}'.format(value))
        ctx.exit()

    ext = os.path.splitext(value)[1]
    if ext not in ['.json', '.geojson']:
        raise click.BadParameter(
            'Only .json and .geojson filenames are accepted.')

    return value


@click.command()
@click.option('-l', '--location', type=str,
              help='input location name(city, country)', prompt=True)
@click.option('-f', '--filename', type=str, callback=validate_filename,
              help='output file name', prompt=True)
@click.option('-d', '--dtype', type=click.Choice(['roads', 'cities', 'buildings']),
              default='roads', help='data type')
@click.option('-b', '--bbox', type=(float, float, float, float),
              default=(None, None, None, None),
              help='bbox in form (west_lat, north_lon, east_lat, south_lon)')
def main(location, filename, dtype, bbox):
    data = Data(location)

    if None in bbox:
        bbox = None

    output = data.get(dtype, format='geojson', bbox=bbox)

    with open(os.path.expanduser(filename), 'w') as f:
        json.dump(output, f)
