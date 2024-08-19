import asyncio
import weatherbug_spark
import json

async def fetch_and_update_data():
    # Fetch lightning strike data
    data = await weatherbug_spark.get_data(42.3601, -71.0589)

    # Extract global lightning strike locations
    lightning_strikes = [
        {
            "latitude": strike.latitude,
            "longitude": strike.longitude,
            "dateTimeUtcStr": strike.dateTimeUtcStr
        }
        for strike in data.pulseListGlobal
    ]

    # Convert to GeoJSON format
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    for strike in lightning_strikes:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [strike["longitude"], strike["latitude"]]
            },
            "properties": {
                "dateTimeUtcStr": strike["dateTimeUtcStr"]
            }
        }
        geojson["features"].append(feature)

    # Save to a GeoJSON file
    with open("lightning_strikes.geojson", "w") as f:
        json.dump(geojson, f)

    print("GeoJSON file updated successfully.")

# Run the asynchronous function
asyncio.run(fetch_and_update_data())
