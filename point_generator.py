"""
Spatial Data Processing Tool

This script serves as a versatile utility for conducting spatial data processing tasks using a variety of algorithms. It provides a command-line interface to execute different algorithms tailored for specific tasks, such as generating grids, weight-based point generation, distance-based shapefile analysis, and more.

The script takes advantage of various modules and libraries, including 'toml' for configuration management and several custom scripts for different algorithm implementations. It utilizes the argparse module to facilitate command-line argument parsing, enabling users to specify the algorithm and relevant parameters.

Algorithms Available:
- 'grid': Grid Generator - Generate grids using given border points and distance.
- 'weight_w_num_points': Weight-Based Fixed Point Generator - Generate points based on weight with a specified number of points.
- 'weight': Weight-Based Algorithm - Process shapefiles using weight-related parameters.
- 'shapefile_w_distance': Shapefile with Distance - Analyze shapefiles based on distances and a specified budget.
- 'shapefile_w_weight': Shapefile with Weight - Analyze shapefiles considering geographical weight and preference.

Usage:
python script_name.py --alg <algorithm> [additional arguments]

Where:
--alg: Specify the algorithm to execute. Choose from 'grid', 'weight_w_num_points', 'weight', 'shapefile_w_distance', 'shapefile_w_weight'.
[additional arguments]: Provide the necessary parameters based on the chosen algorithm. Use '--help' to view the specific parameters for each algorithm.

Example Usage:
python script_name.py --alg grid --ip border_points.txt --of output_grid.txt --d 100
"""

import os
import sys

import toml
from scripts.grid_generator import generate_grid as gg
from scripts.weight_based_fixed_point_nr import weight_based_generator as wn
from scripts.weight_based import weight_based as w
from scripts.shapefile_with_distance import shapefile_with_distance as sd
from scripts.shapefile_with_weight import shapefile_with_weight as sw
import argparse
import json


HELP_MESSAGE = """
Help for Grid Generator (grid)
--ip: File containing grid border points
--sf: Location of the shape file
--d: Distance between two points
--of: Location of the output file
Weight Based (weight):
--wf: Location of the weighted file
--of: Location of the output file
--sf: Location of the shape file
--r: Number that represents the relation value
 --b: Number that represents the budget
Shapefile with Distance (shapefile_w_distance):
--sf: Location of the shape file
--of: Location of the output file
--b: Number that represents the budget
Shapefile with Weight (shapefile_w_weight):
--sf: Location of the shape file
--gf: Location of the shapefile which represents geography
--of: Location of the output file
--p: Preference for point placement, either larger_weight or smaller_weight
        """


def display_help_for_algorithm(alg):
    help_message = ""

    if args.alg == 'grid':
        help_message = """
Grid Generator (grid)
--ip: File containing grid border points
--sf: Location of the shape file
--of: Location of the output file
--d: Distance between two points
"""
    elif args.alg == 'weight_w_num_points':
        help_message = """
Help for Weight Based with Number of Points (weight_w_num_points):
--wf: Location of the weighted file
--of: Location of the output file
--n: Number of points
        """
    elif args.alg == 'weight':
        help_message = """
Help for Weight Based (weight):
--wf: Location of the weighted file
--of: Location of the output file
--sf: Location of the shape file
--r: Number that represents the relation value
 --b: Number that represents the budget
        """
    elif args.alg == 'shapefile_w_distance':
        help_message = """
Help for Shapefile with Distance (shapefile_w_distance):
--sf: Location of the shape file
--of: Location of the output file
--b: Number that represents the budget
        """
    elif args.alg == 'shapefile_w_weight':
        help_message = """
Help for Shapefile with Weight (shapefile_w_weight):
--sf: Location of the shape file
--gf: Location of the shapefile which represents geography
--of: Location of the output file
--p: Preference for point placement, either larger_weight or smaller_weight
        """

    print(help_message)
    print("\nUsage:")
    print(f"python script_name.py --alg {alg} [additional arguments]\n")


def load_params_from_json(json_file):
    try:
        with open(json_file, 'r') as f:
            params = json.load(f)
            return params
    except json.decoder.JSONDecodeError:
        print("ne valja json")
        sys.exit()
    except Exception as e:
        print(f"Exception Happened: {e}")
        sys.exit()


if __name__ == '__main__':
    print(HELP_MESSAGE)

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--json',
        help='Configuration file'
    )

    parser.add_argument(
        '--alg',
        choices=['grid', 'weight_w_num_points', 'weight', 'shapefile_w_distance', 'shapefile_w_weight'],
        help='Select the algorithm: grid - grid generator, weight_w_num_points - weight based point selection with number of points as an input, weight - weight based point selection, shapefile_w_distance - points selected based on the shapefile and distance between points as input parameters, shapefile_w_weight - points selected based on the shapefile and weight file which are input parameters',
    )

    parser.add_argument('--ip', help='File containing grid border points', type=str)
    parser.add_argument('--d', help='Distance between two points expressed in miles', type=float)
    parser.add_argument('--of', help='Location of the output file', type=str)
    parser.add_argument('--wf', help='Location of the weighted file', type=str)
    parser.add_argument('--n', help='Number of points', type=int)
    parser.add_argument('--sf', help='Location of the shape file', type=str)
    parser.add_argument('--r', help='Number that represents the relation value', type=float)
    parser.add_argument('--b', help='Number that represents the budget', type=str)
    parser.add_argument('--conf', help='Path to the TOML configuration file', type=str, default='res/config.toml')
    parser.add_argument('--gf', help='Location of the shapefile which represents geography', type=str)
    parser.add_argument('--p', help='Preference for point placement, either larger_weight or smaller_weight', type=str)

    args = parser.parse_args()

    if args.json:
        json_params = load_params_from_json(args.json)
        args = argparse.Namespace(**vars(args), **json_params)

    config_path = os.path.abspath('res/config.toml')
    config = toml.load(config_path)
    required_args_count = config['required_args_count']

    if args.alg in required_args_count:
        if len(vars(args)) != required_args_count[args.alg]:
            display_help_for_algorithm(args.alg)
        else:
            if args.alg == 'grid':
                gg(args.ip, args.sf, args.of, args.d)
            elif args.alg == 'weight_w_num_points':
                wn(args.wf, args.of, args.n)
            elif args.alg == 'weight':
                config_file = "res/config.toml"
                config = toml.load(config_file)
                w(args.wf, args.of, args.sf, args.r, args.b, config['config']['max_num_per_screen'])
            elif args.alg == 'shapefile_w_distance':
                sd(args.sf, args.of, args.b)
            elif args.alg == 'shapefile_w_weight':
                sw(args.sf, args.gf, args.of, args.p)
    else:
        print(f"Invalid algorithm choice: {args.alg}")
        parser.print_help()
