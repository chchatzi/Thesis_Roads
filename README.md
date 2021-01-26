# Thesis_Roads
Road width estimation with areal and linear vector data

# General Implementation
0) Input: two shapefiles, i) sample of areal representations of roads in a specific area in Toronto (toronto_sample_polygons.shp), ii) Centerlines of roads for the same area in Toronto (toronto_sample_lines.shp)

1) First step: Merge small centerlines that correspond to the same road. We use LFN_ID attribute for that. merge_lines_lfnid_toronto.py takes the file with the unmerged centerlines and return/creates a file with a big centerline for each road (the new file = merged_lines_toronto.shp).

2) Next step is storing the geometry of polygons that can be found in the polygon shapefile into a list. Before doing that we check each polygon for validity, and if it is not valid we try to validate it, only valid polygons of the shapefile is stored in the list. 

3) Same operation for lines. We store the geometry of each "big" centerline as created to the first step at a list. We assign a unique id to each line. shapefile_manipulation.py takes 2 shapefiles (one with merged lines and one with polygons), reads the geometry and stores it into lists (returns 2 lists: one with geometry of all the big centerlines + an id for each and one with the valid polygons)

4) Traverse the list with the lines, for each line find the polygons that intersects and cut the line to smaller lines in order to fit each polygon. Estimate widths for each pair of polygon and line based on our current methodology. Each one of those widhts is assigned a weigth based on the length of the line piece that is used (in comparison with the total length of the initial  centerline). Use the widths of each pair (with different weights) and estimate a final width for each centerline.

5) During the width estimation process for each pair of polygon and centerline we identify if there is a cross or a T intersection. If so, we assign width to 0 for that pair of polygon-line and we exclude from the final width calculation. For steps 4 and 5 test_road_width.py and intersection_identify.py are used

6) Final step is to write a new lines shapefile which contains the "big" initial centerlines with 3 new attributes. Their width estimation, the number of T intersections and the number of Cross intersections. The new file that is created called lines_with_width.shp. write_the_file.py
