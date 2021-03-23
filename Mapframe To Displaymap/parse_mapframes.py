import json
from pathlib import Path

"""
Params from the <mapframe>-tag, can be used like this inside the {{display_map}}:
{{display_map:
...
|width=300
|height=400
|zoom=12
|center=56.162060,10.196270
}}
"""


def main(jsonfile):
    points = []
    polygons = []
    lines = []
    colors = {"0050d0": "_blue", "FF0000": "_red"}
    sizes = {"small": "_small"}
    symbols = {"building": "Building"}

    with open(Path(jsonfile)) as f:
        featurecollection = json.load(f)

        for feature in featurecollection.get("features"):
            if feature["geometry"].get("type") == "Point":
                out = str()
                longitude = str(feature["geometry"]["coordinates"][0])
                latitude = str(feature["geometry"]["coordinates"][1])
                title = feature["properties"].get("title", "")
                description = feature["properties"].get("description", "")
                out += latitude + "," + longitude
                if title:
                    out += "~" + title
                if description:
                    out += "~" + description
                # marker_symbol = feature["properties"].get("marker-symbol")
                # marker_size = feature["properties"].get("marker-size")
                # marker_color = feature["properties"].get("marker-color")
                # if marker_color:
                #     marker_color = colors.get(marker_color, "")
                # if marker_size:
                #     marker_size = sizes.get(marker_size, "_small")
                # if marker_symbol:
                #     marker_symbol = symbols.get(marker_symbol, "")
                points.append(out)
            elif feature["geometry"].get("type") == "Polygon":
                for polygon in feature["geometry"].get("coordinates"):
                    output = []
                    for point in polygon:
                        output.append(str(point[1]) + "," + str(point[0]))
                    polygons.append(":".join(output))

    print("{{#display_map:")
    for point in points:
        print(point + ";")
    if polygons:
        print("|polygons=")
        for polygon in polygons:
            print(polygon + ";")
    print("}}")


if __name__ == "__main__":
    main("broer.json")
