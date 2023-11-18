import sys
import toml
import random
import pandas as pd
import geopandas as gpd
from pyproj import Transformer
from scripts.helpers.utils import save_coordinates_to_csv as sccsv
from scripts.helpers.helpers import column_descriptions


def calculate_optimal_number_of_points(weight: int, relation: float, budget: float, max_point_count: int) -> int:
    """
    Calculate the optimal number of points for each county based on weight, relation, and budget.

    :param weight: The weight value used for weighting when calculating the number of points.
    :param relation: The relation value which represents relation between weight and certain enterprise. Ex. number of grocery stored per one citizen.
    :param budget: The budget value which represents the budget one want to use when searching for points. Budget is directly related to the percentage of points that will be used. Percentage of weight can be modified in the config.toml file.
    :param max_point_count: The maximum number of establishment that can be scraped for every points selected. It can be altered in config.toml file.

    :return: The calculated optimal number of points.
    """
    establishments = weight * relation
    number_of_points = round(establishments / max_point_count)
    return max(1, round(number_of_points * budget))


def generate_random_points_in_polygon(polygon_list: list, num_points: int) -> gpd.GeoSeries:
    """
    Generate num_points of random points within a polygon.

    :param polygon_list: A list of polygons representing a county.
    :param num_points: The desired number of random points to generate.

    :return: A GeoSeries containing the generated random points.

    """
    points = []
    transformer = Transformer.from_crs('EPSG:3857', 'EPSG:4326')

    for polygon in polygon_list:
        min_x, min_y, max_x, max_y = polygon.bounds
        while len(points) < num_points:
            x = random.uniform(min_x, max_x)
            y = random.uniform(min_y, max_y)
            point = (x, y)
            if polygon.contains(gpd.points_from_xy([x], [y])[0]):
                points.append(point)

    transformed_points = [transformer.transform(p[0], p[1]) for p in points]
    return gpd.GeoSeries(gpd.points_from_xy([point[0] for point in transformed_points], [point[1] for point in transformed_points]))


def reading_file_error(key_error):
    """
        Handle error when reading file columns.

        :param key_error: The KeyError that occurred during file reading.
    """
    missing_columns = [column.strip() for column in
                       key_error.args[0].split('[')[1].split(']')[0].replace("'", "").split(',')]
    for column in missing_columns:
        if column in column_descriptions:
            print(f"Missing column: {column}\nDescription: {column_descriptions[column]}\n")
        else:
            print(f"Missing column: {column}\nDescription: Description not available.\n")


def weight_based(file_name_with_weights: str, output_file: str, shape_file: str, relation: float, budget: float,
                 max_points: int):
    """
        Generate points that will cover all establishment in each county based on parameters.

        :param file_name_with_weights: Location of file which holds weight.
        :param output_file: Location of a file in which point will be saved.
        :param shape_file: Location of a shape file from which polygons will be extracted.
        :param relation: The relation value which represents relation between weight and certain enterprise. Ex. number of grocery stored per one citizen.
        :param budget: The budget value which represents the budget one want to use when searching for points. Budget is directly related to the percentage of points that will be used. Percentage of weight can be modified in the config.toml file.
        :param max_points: The maximum number of establishment that can be scraped for every points selected. It can be altered in config.toml file.

        """
    try:
        weights = pd.read_csv(file_name_with_weights, dtype={'Population': int, 'STATEFP': str, 'COUNTYFP': str}).loc[:, ['STATEFP', 'COUNTYFP', 'WEIGHT', 'LATITUDE', 'LONGITUDE']]
    except KeyError as e:
        reading_file_error(e)
        sys.exit()

    weights['Optimal Number of Points'] = weights.apply(lambda row_points: calculate_optimal_number_of_points(row_points['WEIGHT'], relation, budget, max_points), axis=1)

    county_polygons = gpd.read_file(shape_file)

    generated_points = []

    for index, row in weights.iterrows():
        state_code = row['STATEFP']
        county_code = row['COUNTYFP']
        num_points = row['Optimal Number of Points']

        polygons = county_polygons.loc[(county_polygons['STATEFP'] == state_code) & (
                    county_polygons['COUNTYFP'] == county_code), 'geometry'].values

        random_points = generate_random_points_in_polygon(polygons, num_points)

        generated_points.extend([[point.x, point.y] for point in random_points])

    sccsv(generated_points, output_file)


if __name__ == '__main__':
    weights_file = '../res/US_county_cenpop_2020.csv'
    name_of_output_file = '../res/output.csv'
    shapefile_path = '../res/COUNTY-2020-US-SL050-Coast-Clipped.zip'

    config_file = "../res/config.toml"
    config = toml.load(config_file)

    relation_value = 0.00018928137587254074
    budget_multipliers = config['budget']

    weight_based(weights_file, name_of_output_file, shapefile_path, relation_value, budget_multipliers["high"],
                 config['config']['max_num_per_screen'])
