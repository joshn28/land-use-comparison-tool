import arcpy

# Get feature layers and fields
current_land_use = arcpy.GetParameterAsText(0)
historical_land_use = arcpy.GetParameterAsText(1)
area_field = arcpy.GetParameterAsText(2)
land_use_field = arcpy.GetParameterAsText(3)
urban_growth_boundary = arcpy.GetParameterAsText(4)

# Set output locations
out_changed_areas = arcpy.GetParameterAsText(5)
out_summary_stats = arcpy.GetParameterAsText(6)

# Set the workspace environment
arcpy.env.workspace = "CURRENT"

# To allow overwriting outputs
arcpy.env.overwriteOutput = True

# Identify areas where land use has changed
arcpy.analysis.Erase(current_land_use, historical_land_use, out_changed_areas)

print("Identified areas where land use has changed...")

# Intersect changed areas with urban growth boundaries to see if the changes fall within urban expansion zones
if urban_growth_boundary:
    arcpy.analysis.Intersect(
        [out_changed_areas, urban_growth_boundary], "urban_growth_overlay"
    )

# Calculate statistics for each land use change type and summarize the results.

arcpy.analysis.Statistics(
    out_changed_areas,
    out_summary_stats,
    [
        [area_field, "SUM"],
        [area_field, "MEAN"],
        [area_field, "MAX"],
        [area_field, "MIN"],
        [area_field, "STD"],
    ],
    land_use_field,
)

print("Land Use Comparison Tool Completed!")
