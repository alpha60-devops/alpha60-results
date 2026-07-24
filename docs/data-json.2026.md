# alpha60 data documentation

*Last 2026-07-24*

## definitions
- "media object" : an instance of a film, series, book, etc.
- "collection" : a set of media objects, all instances found
- "btih" : the Bittorrent Info Hash associated with a media object
- "btiha" : an array of all btiha in a collection, including duplicates
- "unique btiha" : an array of unique info hashes, with duplicates merged

## shared data fields JSON

- collection_key : "andor-201", unique human readable tag that works
  as a filesystem-level identifier for media collection. All
  lowercase, full seasons are 2 digits (01 is first season), and
  episodes are three digits (102 is Season 1 Episode 02). For multiple
  episodes, use the first episode sampled.
- data_version : "2026-06-18", date of data API
- geolocation_version : "6:1777968300", geolocation library major : db version,
						library major is 0:none, 1:maxmind, 2-6:ipinfo geo, privacy, mobile, satellite
						version is vendor-defined.
- udownloaders_total: number of unique ip addresses downloading the media
- uuploaders_total: number of unique ip addresses uploading the media to others

- sample_duration: ISO 8601 formatted begin date "-to-" end date.

## duration JSON files

### "*-cumulative*".json
- filename: (collection_key)-cumulative.json
  - collection_cumulative : total results
	- btiha
	- unique-btiha
  - data_transfer : cost of bandwidth
  - media_codecs_resolution
	- [0] 1080p downloaders
	- [1] 720p downloaders
	- [2] sd downloaders
	- [3] 2160, aka 4k downloaders
  - geo_slices_4_cahill_keyes_quadrant_udownloaders: global "quadrant" breakdown
  - geo_slices_continental_udownloaders : continental breakdown of traffic
  - geo_country_top_10_downloaders : top countries by download swarm size
  - geo_country_top_10_uploaders : top countries by upload swarm size
  - geo_country_region_city_top_30_downloaders : top country-region

- filename: (collection_key)-cumulative-ip-swarm.json
  - swarm-analysis
	- anomalies_and_tor_exit_nodes
	  - global
	  - by_country
	- carrier_and_mobile_wireless
	  - global
	  - by_country
	- satellite
	  - global
	  - by_country
	- privacy
	  - global
	  - by_country

- filename: (collection_key)-cumulative-btiha-media-objects.json
  - collection_btiha_duplicates
	- [0] array of torrent file names that share btih number 1
	- [n] array of torrent file names that share btih number n
  - collection_btiha_metadata
	- [0] name of 1st torrent file, total file size, names of files contained
	- [n] name of last torrent file, total file size, names of files contained
  - collection_cumulative_by_btiha
	- [0] cumulative udownloaders first btih in btiha
	- [n] cumulative udownloaders last btih in btiha

### "*-week".json
- filename: (collection_key)-week.json
  - collection_week
	- [0] week 1 udownloaders_total, uuploaders_total
	- [n] week n + 1 udownloaders_total, uuploaders_total
  - collection_week_by_btiha
	- [0] week 1 udownloaders each media object in collection
	- [0][0] week 1 udownloaders first btih in btiha
	- [0][n] week 1 udownloaders last btih in btiha
  - collection_week_by_country
	- [0] week 1 udownloaders each media object in collection
	- [0][00] week 1 udownloaders for country BRA
	- [0][01] week 1 udownloaders for country CAN
	- [0][02] week 1 udownloaders for country CHN
	- [0][03] week 1 udownloaders for country DEU
	- [0][04] week 1 udownloaders for country ESP
	- [0][05] week 1 udownloaders for country FRA
	- [0][06] week 1 udownloaders for country HKG
	- [0][07] week 1 udownloaders for country JPN
	- [0][08] week 1 udownloaders for country KOR
	- [0][09] week 1 udownloaders for country MEX
	- [0][10] week 1 udownloaders for country NLD
	- [0][11] week 1 udownloaders for country RUS
	- [0][12] week 1 udownloaders for country SWE
	- [0][13] week 1 udownloaders for country TUR
	- [0][14] week 1 udownloaders for country UKR
	- [0][15] week 1 udownloaders for country USA

## shared data fields GeoJSON

In FeatureCollection objects
- datestamp: ISO 8601 formatted begin date "-to-" end date
- data_version: Data API version as compressed ISO datestamp.
- btiha_size: Number of elements in media collection, each elment has one BTIH
- swarm_geo_partition_by: "hexagon" means bin swarms into unique H3 Hexagons
						  "map" means bin swarms by COUNTRY-GEOID-CITY
- swarm_hexagon_resolution: H3 Hexagon resolution for data in file
- swarm_features_size: The number of feature elements in the FeatureCollection

In Feature.properties objects
- h3_hexagon: the corresponding unique H3 Hexagon ID at swarm_hexagon_resolution
- geoname_id: the unique numeric identifier from GeoNames.org
- country_code: the ISO 3 country code
- city: the city or region designation
- downloaders: swarm unique downloader counts and network characteristic counts
  (size,mobile,satellite,tor,tor_exit_nodes,vpn,relay,proxy,hosting,service)
- uploaders: swarm unique uploader counts and network characteristic counts
  (size,mobile,satellite,tor,tor_exit_nodes,vpn,relay,proxy,hosting,service)

## duration GeoJSON files

These files may be large. If so, they may compressed with either .zip or .xz compression.

### "*-cumulative.geojson"
- filename: (collection_key)-cumulative.geojson
  - FeatureCollection
	- features[0]
	  - properties object
	  - geometry Point

### "*-week-000[0-5][0-9].geojson"
- filename: (collection_key)-week-000[0-5][0-9].geojson
  - FeatureCollection
	  - features[0]
		- properties object
		- geometry Point
	  - collection_week_by_btiha[0 to btiha_size]
		  - FeatureCollection itemized for just this BTIH
			- features[0]
			  - properties object
			  - geometry Point


## metadata
- filename: (collection_key).json
  - collection_name
  - collection_key
  - collection_id [ "101", "102", "103" ]
  - collection_tags [ "star_wars_universe", "aapi", "animation" ]
  - metadata_datestamp "YYYY-MM-DD"
  - updated_datestamp "YYYY-MM-DD"
  - imdb_id
  - url_wikipedia
  - url_fandom
  - box_office_usa
  - box_office_international
  - box_office_global
  - ecount
  - eruntime
  - ecost [ 1, 2] # per episode cost range in M USD
  - distribution_tags [ "netflix" ]
  - production_tags [ "a24" ]
  - sample_duration "YYYY-MM-DD to YYY-MM-DD"
  - sample_days 105
  - sample_day_year_start 1
  - sample_day_year_end 365
  - sample_year_start YYYY
  - sample_year_end YYYY

## example with annotation
```
{
  "collection_name": "Zero Day",
  "collection_id": "1",
  "collection_key": "zero-day-01",
  "collection_notes": "",
  "data_version": "2026-06-18",
  "data_btiha_sort": 1,
  "ip_geolocation_version": "6:1777968300",
  "sample_duration": "2025-02-20-to-2025-06-04",
  "sample_days": 105,
  "sample_year_start": 2025,
  "sample_year_end": 2025,
  "sample_day_year_start": 51,
  "sample_day_year_end": 155,
  "collection_week": [

```


## References
[W3C Data on the Web Best Practices](https://w3c.github.io/dwbp/bp.html)
