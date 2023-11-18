# Grid Generator

`grid_generator.py` is a Python script that generates a grid of points within a given polygon based on a specified distance between points. It takes the border points of the polygon, the desired distance between points, the shapefile and the output file location as inputs and produces a CSV file containing the generated grid points.

## Input CSV File Format

The input CSV file should have the following format:

```csv
lon,lat,description
49.384358,-125.000000,Northwest
49.384358,-66.934570,Northeast
24.396308,-125.000000,Southwest
24.396308,-66.934570,Southeast
```

- The `lon` column represents the longitude of each point.
- The `lat` column represents the latitude of each point.
- The `description` column is optional and can be used to provide additional information about each point.

**Please ensure that the number of points in the CSV file is a multiple of 4 (e.g., 4, 8, 12, 16, and so on) since each polygon requires exactly 4 points to be defined properly.**

## Requirements

- Python 3.x
- pandas library

## Installation

Before running the script, make sure you have Python 3.x installed. If you don't have the pandas library installed, you can install it using pip:

```bash
pip install pandas
```

## Usage

To use the `grid_generator.py` script, follow these steps:

1. Prepare the input CSV file: Create a CSV file following the specified format and ensure that the number of points is a multiple of 4.

2. Modify the script parameters: Open `grid_generator.py` in a text editor and adjust the following variables according to your needs:
   - `border_points_location_file`: Provide the file path of the CSV file containing the border points of the polygons.
   - `distance`: Set the desired distance between each grid point in kilometers.
   - `shapefile_path`: Provide the file path of the shape file which will be used to filter the points. 
   - `output_file_name`: Specify the file path where you want to save the generated grid points.

3. Run the script: Open a terminal or command prompt, navigate to the directory where `grid_generator.py` is located, and execute the following command:

```bash
python grid_generator.py
```

The script will read the border points from the provided CSV file, generate the grid points within each polygon based on the specified distance, and save the resulting grid points to the output CSV file.


# Points Generator - Weight Based

The `weight_based.py` script is a flexible tool that generates points within a geographical area based on certain parameters. It calculates the optimal number of points for each region, generates random points within the polygons, and saves the resulting points to a CSV file.

## Requirements

- Python 3.x
- pandas library
- geopandas library
- pyproj library
- toml library

## Installation

Before running the script, make sure you have Python 3.x installed along with the required libraries. If you don't have them installed, you can install them using pip:

```bash
pip install pandas geopandas pyproj toml
```

## Configuration

The script requires a configuration file named `config.toml`, which allows you to set various parameters affecting point generation. The configuration file should be placed in the `res` directory and have the following format:

```toml
[budget]
high = 0.8
medium = 0.5
low = 0.2

[config]
max_num_per_screen = 500
```

The `budget` section defines multipliers for different budget scenarios, affecting the number of points generated. The `config` section defines the maximum number of establishments that can be scraped for every selected point.

## Input Data

### Weights File

The script expects a CSV file containing data for geographical regions. The file should have the following columns:

- `STATEFP`: State FIPS code.
- `COUNTYFP`: County FIPS code.
- `geometry`: The geometry column representing the polygons of each region.
- `population`: The population count of each region.

Ensure that the data in the CSV file is relevant to the geographical area for which you want to generate points.

### Region Shapefile

The script requires a shapefile containing polygons that represent the boundaries of the geographical regions. The polygons will be used to generate random points within each region.

## Usage

To use the `weight_based.py` script, follow these steps:

1. Prepare the input files: Ensure you have the weights file and the region shapefile in the `res` directory. The weights file should contain the necessary columns, including the `STATEFP`, `COUNTYFP`, `geometry` and `population` columns.

2. Configure the budget multipliers: Modify the `budget` section in `config.toml` to set different budget scenarios with corresponding multipliers.

3. Run the script: Open a terminal or command prompt, navigate to the directory where `weight_based.py` is located, and execute the following command:

```bash
python weight_based.py
```

The script will read the weights file, calculate the optimal number of points for each region, generate random points within each region's polygon, and save the resulting points to the `output.csv` file in the `res` directory.

Sure! Here is the README.md file for your Python script:

# Weight-Based Points Generator

This Python script generates points based on the weight of each point in the input file. The points are moved randomly within a certain range to create new data points.

## Prerequisites

Before running the script, make sure you have the following installed:

- Python 3.x
- pandas library
- randi=om library


Install the required packages using pip:
```bash
pip install pandas random
```

## Overview

### `move_point_by_rand(latitude: float, longitude: float) -> Tuple[float, float]:`

This function moves a point's latitude and longitude randomly within a certain range.

Parameters:
- `latitude` (float): The latitude of the point.
- `longitude` (float): The longitude of the point.

Returns: tuple - The updated latitude and longitude after random movement.

### `weight_based_generator(file_name: str, output_file: str, number_of_points: int) -> None:`

This function generates points based on the weight of each point in the input file. If the desired number of points is greater than the available points, additional points are generated based on population percentage.

Parameters:
- `file_name` (str): Location of the input file containing point data and weight.
- `output_file` (str): Location of the output file to save the generated points.
- `number_of_points` (int): The desired number of points to generate.

Returns: None

## Usage

1. Ensure you have installed the required packages mentioned in the Prerequisites section.

2. Modify the `resource_file`, `name_of_output_file`, and `inputted_number_of_points` variables in the main section according to your data and preferences.

3. Run the script:

```bash
python your_script_name.py
```

4. The script will read the input file, generate points based on the weight of each point, and save the generated points in the CSV file specified by `name_of_output_file`.

## Input File Format

The input file should be a CSV file with the following columns:
- 'POPULATION': Population weight of each county centroid.
- 'LATITUDE': Latitude of each county centroid.
- 'LONGITUDE': Longitude of each county centroid.


# Point Generator - Shapefile with Distance

This Python script processes geospatial data from a shapefile to generate points along the lines with a specified distance.

## Prerequisites

Before running the script, make sure you have the following installed:


- Python 3.x
- geopandas library

Install the required package using pip:
```bash
pip install geopandas
```

## Overview

### `points_on_line_with_distance(lines: gpd.GeoDataFrame, distance: float) -> list:`

This function generates points along each line in a GeoDataFrame based on the specified distance.

Parameters:
- `lines` (GeoDataFrame): A GeoDataFrame containing lines represented by their geometries.
  It should have a 'geometry' column containing line geometries in Shapely format.
- `distance` (float): The distance between each interpolated point along the lines.

Returns: list - A list of tuples containing (latitude, longitude) pairs representing the generated points.

### `shapefile_with_distance(input_file: str, output_file: str, distance: float) -> None:`

This function processes a shapefile, filters specific highway codes, generates points along the lines, and saves them to a CSV file.

Parameters:
- `input_file` (str): Path to the input shapefile containing highway data.
- `output_file` (str): Path to the output CSV file where the points will be saved.
- `distance` (float): The distance between each interpolated point along the lines.

Returns: None

## Usage

1. Ensure you have installed the required packages mentioned in the Prerequisites section.

2. Modify the `lines_location_file` and `output_location_file` variables in the main section according to your data and preferences.

3. Optionally, adjust the `length` variable to change the distance between the generated points along the lines.

4. Run the script:

```bash
python your_script_name.py
```

5. The script will process the geospatial data, generate points along the lines with the specified distance, and save the output points in the CSV file specified by `output_location_file`.


# Point Generator - Shapefile with Weight

This Python script processes geospatial data to generate weighted points along the given lines.

## Prerequisites

Before running the script, make sure you have the following installed:

- Python 3.x
- pandas library
- geopandas library
- pyproj library

Install the required packages using pip:
```bash
pip install pandas geopandas pyproj
```

## Overview

The script contains the following functions:

1. `shapefile_with_weight(input_file: str, shape_file: str, output_file: str, preference: str) -> None:`

   Process shapefiles, calculate weights, generate points, and export to a CSV file.

   Parameters:
   - `input_file` (str): Path to the input shapefile containing highway data.
   - `shape_file` (str): Path to the shapefile representing the geographic boundaries.
   - `output_file` (str): Path to the output CSV file where the points will be saved.
   - `preference` (str): User's preference for point placement, either 'larger_population' or 'smaller_population'.

   Returns: None

2. `define_weight_preference(preference: str, line: pd.Series) -> float:`

   Calculate the weight preference for a given line based on the user's choice of 'larger_population' or 'smaller_population'.

   Parameters:
   - `preference` (str): User's preference for point placement, either 'larger_population' or 'smaller_population'.
   - `line` (pd.Series): A pandas Series representing a specific line in the geography with a 'weight' column.

   Returns: float - The calculated weight preference for the given line.

3. `generate_points_on_line(lines) -> list:`

   Generate points along each line based on the calculated distance between points and the number of points.

   Parameters:
   - `lines` (GeoDataFrame): A GeoDataFrame containing lines represented by their geometries.
     It should have columns 'geometry', 'line_length', and 'num_points'.

   Returns: list - A list of tuples containing (latitude, longitude) pairs representing the generated points.

## Usage

1. Ensure you have installed the required packages mentioned in the Prerequisites section.

2. Modify the `roads_location_file`, `geography_location_file`, `output_location_file`, and `position_preference` variables in the main section according to your data and preferences.

3. Run the script:

```bash
python your_script_name.py
```

4. The script will process the geospatial data, generate points along the lines based on the specified preference, and save the output points in the CSV file specified by `output_location_file`.

