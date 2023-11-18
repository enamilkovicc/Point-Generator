import geopandas as gpd
import pandas as pd
import pyproj
from scripts.helpers.utils import save_coordinates_to_csv as sccsv
from scripts.helpers.utils import filter_shapefile_by_parameters as filter_shapefile


def generate_points_on_line(lines: gpd.GeoDataFrame) -> list:
    """
    Generate points along each line based on the calculated distance between points.

    Parameters:
        lines (GeoDataFrame): A GeoDataFrame containing lines represented by their geometries.
                                It should have columns 'geometry', 'line_length', and 'num_points'.

    Returns:
        list: A list of tuples containing (latitude, longitude) pairs representing the generated points.
    """
    points_on_line = []

    for _, line in lines.iterrows():
        line_string = line['geometry']
        total_distance = line['line_length']
        distance = line['line_length'] / line['num_points']

        if total_distance < distance:
            continue

        num_interpolated_points = line['num_points']

        interpolated_points = [line_string.interpolate(i * distance) for i in range(1, num_interpolated_points + 1)]

        for point in interpolated_points:
            points_on_line.append((point.y, point.x))

    return points_on_line


def define_weight_preference(preference: str, line: pd.Series) -> float:
    """
    Calculate the weight preference for a given line based on user's choice.

    Parameters:
        preference (str): User's choice of 'larger_population' or 'smaller_population'.
        line (pd.Series): A pandas Series representing a specific line in the geography.
                          It should have a 'weight' column representing the ratio of line length to county area.

    Returns:
        float: The calculated weight preference for the given line.
    """
    if 'weight' not in line:
        raise ValueError(
            "Input 'line' must have a 'weight' column representing the ratio of line length to county area.")

    if preference == 'larger_population':
        max_weight = line['weight'].max()
        weight_preference = max_weight - line['weight']
    elif preference == 'smaller_population':
        weight_preference = line['weight']
    else:
        raise ValueError("Invalid preference choice. Please choose 'larger_population' or 'smaller_population'.")

    return weight_preference


def shapefile_with_weight(input_file: str, shape_file: str, output_file: str, preference: str):
    """
    Process shapefiles, calculate weights, generate points, and export to a CSV file.

    Parameters:
        input_file (str): Path to the input shapefile containing highway data.
        shape_file (str): Path to the shapefile representing the geographic boundaries.
        output_file (str): Path to the output CSV file where the points will be saved.
        preference (str): User's preference for point placement, either 'larger_weight' or 'smaller_weight'.

    Returns:
        None
    """
    lines = gpd.read_file(input_file)

    geography = gpd.read_file(shape_file)

    lines = lines.to_crs('EPSG:32633')
    geography = geography.to_crs(crs=lines.crs)

    geography['county_area'] = geography.geometry.area
    lines['line_length'] = lines.geometry.length

    lines_in_geography = gpd.sjoin(lines, geography, how='inner', predicate='intersects')

    lines_in_geography['weight'] = lines_in_geography['line_length'] / lines_in_geography['county_area']

    weight_preference = define_weight_preference(preference, lines_in_geography)

    min_weight = weight_preference.min()
    max_weight = weight_preference.max()

    lines_in_geography['num_points'] = (
        (1 - (weight_preference - min_weight) / (max_weight - min_weight))).astype(int)

    lines_in_geography.loc[lines_in_geography['num_points'] == 0, 'num_points'] = 1

    points = generate_points_on_line(lines_in_geography)

    transformer = pyproj.Transformer.from_crs('EPSG:32633', 'EPSG:4326', always_xy=True)

    transformed_points = []
    for point in points:
        lon, lat = transformer.transform(point[1], point[0])
        transformed_points.append((lat, lon))

    sccsv(transformed_points, output_file)


if __name__ == '__main__':
    lines_location_file = '../res/roads-shapefile.zip'
    geography_location_file = '../res/COUNTY-2020-US-SL050-Coast-Clipped.zip'
    output_location_file = '../res/output.csv'

    position_preference = "smaller_weight"

    filtering_parameters = ('RTTYP', ['I', 'U', 'S'])
    filtered_shapefile = filter_shapefile(lines_location_file, filtering_parameters, "filtered_shapefile.zip")

    shapefile_with_weight('../scripts/filtered_shapefile.zip', geography_location_file, output_location_file, position_preference)
