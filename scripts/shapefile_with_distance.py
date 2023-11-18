import geopandas as gpd
from scripts.helpers.utils import save_coordinates_to_csv as sccsv
from scripts.helpers.utils import filter_shapefile_by_parameters as filter_shapefile


def points_on_line_with_distance(lines: gpd.GeoDataFrame, distance: float) -> list:
    """
    Generate points along each line based on the specified distance.

    Parameters:
        lines (GeoDataFrame): A GeoDataFrame containing lines represented by their geometries.
                              It should have a 'geometry' column containing line geometries in Well-Known Text (WKT) format.
        distance (float): The distance between each interpolated point along the lines.

    Returns:
        list: A list of tuples containing (latitude, longitude) pairs representing the generated points.
    """
    points_on_line = []

    for _, line in lines.iterrows():
        total_distance = line['geometry'].length

        if total_distance < distance:
            continue

        num_interpolated_points = int(total_distance // distance)

        interpolated_points = [line['geometry'].interpolate(i * distance) for i in range(1, num_interpolated_points + 1)]

        for point in interpolated_points:
            points_on_line.append((point.y, point.x))

    return points_on_line


def shapefile_with_distance(input_file, output_file, distance):
    """
    Process a shapefile, filter specific highway codes, generate points along the lines, and save them to a CSV file.

    Parameters:
        input_file (str): Path to the input shapefile containing highway data.
        output_file (str): Path to the output CSV file where the points will be saved.
        distance (float): The distance between each interpolated point along the lines.

    Returns:
        None
    """
    lines = gpd.read_file(input_file)
    points = points_on_line_with_distance(lines, distance)
    sccsv(points, output_file)


if __name__ == '__main__':
    lines_location_file = '../res/roads-shapefile.zip'
    output_location_file = '../res/output.csv'

    filtering_parameters = ('RTTYP', ['I', 'U', 'S'])
    filter_shapefile(lines_location_file, filtering_parameters, "filtered_shapefile.zip")

    length = 0.001
    shapefile_with_distance('../scripts/filtered_shapefile.zip', output_location_file, length)
