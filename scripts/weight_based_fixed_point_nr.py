import pandas as pd
import random
from typing import Tuple
from scripts.helpers.utils import save_coordinates_to_csv as sccsv


def move_point_by_rand(latitude: float, longitude: float) -> Tuple[float, float]:
    """
        Move a point's latitude and longitude randomly within a certain range.

        :param latitude: The latitude of the point.
        :param longitude: The longitude of the point.
        :return: The updated latitude and longitude after random movement.
        """
    max_change = 0.09
    lat_change = random.uniform(-max_change, max_change)
    lon_change = random.uniform(-max_change, max_change)
    latitude += lat_change
    longitude += lon_change
    return latitude, longitude


def weight_based_generator(file_name: str, output_file: str, number_of_points: int):
    """
    Generate points based on the weight of each point in the input file.

    :param file_name: Location of the input file containing point data and weight.
    :param output_file: Location of the output file to save the generated points.
    :param number_of_points: The desired number of points to generate.
    """

    column_names = ['POPULATION', 'LATITUDE', 'LONGITUDE']
    sorted_points_df = pd.read_csv(file_name, skiprows=1, usecols=[6, 7, 8], names=column_names).sort_values(by='POPULATION', ascending=False)

    sorted_points_df_length = len(sorted_points_df)

    if number_of_points <= sorted_points_df_length:
        selected_points = sorted_points_df.head(number_of_points)
    else:
        selected_points = sorted_points_df.head(sorted_points_df_length)
        total_population = sorted_points_df['POPULATION'].sum()

        sorted_points_df['Population Percentage'] = round((sorted_points_df['POPULATION'] / total_population) * 100)
        sorted_points_df['Allocated Points'] = round((sorted_points_df['Population Percentage'] / 100) * (number_of_points - sorted_points_df_length))

        for index, row in sorted_points_df.iterrows():
            for i in range(int(round(row['Allocated Points']))):
                latitude, longitude = move_point_by_rand(row['LATITUDE'], row['LONGITUDE'])
                altered_row = pd.Series([latitude, longitude], index=['LATITUDE', 'LONGITUDE'])
                selected_points = selected_points._append(altered_row, ignore_index=True)

        points_used = sorted_points_df['Allocated Points'].sum() + sorted_points_df_length
        points_left = number_of_points - points_used

        if points_left > 0:
            for index, row in sorted_points_df.iterrows():
                latitude, longitude = move_point_by_rand(row['LATITUDE'], row['LONGITUDE'])
                altered_row = pd.Series([latitude, longitude], index=['LATITUDE', 'LONGITUDE'])
                selected_points = selected_points._append(altered_row, ignore_index=True)

                points_left -= 1
                if points_left == 0:
                    break

    sccsv(selected_points, output_file)


if __name__ == '__main__':
    resource_file = '../res/US_county_cenpop_2020.csv'
    name_of_output_file = '../res/output.csv'
    inputted_number_of_points = 3500
    weight_based_generator(resource_file, name_of_output_file, inputted_number_of_points)
