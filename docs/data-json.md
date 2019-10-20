
#Documentaiton for the alpha60 JSON files

```js
{
// Version number for data migration and feature checks
    "data-version": "20191004",

// Date range of the sample duration
    "duration": "2017-10-27-to-2017-12-31",

// Media object name
    "collection-name": "Stranger Things",

// Media object season or episode number
    "collection-id": "2",

// Metadata tags for genre, production, and distribution details. Used for sorting say, Netflix.
    "collection-tag-genre": ["horror", “scifi”, “teen”, “romance”, “period”],
    "collection-tag-production": ["netflix","usa”],
    "collection-tag-distribution": ["netflix"],

// Summary of BTIHA, even if some of the individual BTIH have duplicates.
// (Ie, t002 and t134 have the same BTIH.
    "collection-all-btiha": {

// Number of BTIH in BTIHA
        "btiha-size": 274,

// Number of unique peers found
        "upeers-total": 33765789,

// Number of unique seeds found
        "useeds-total": 13814398,

// Number of peers that have IP addresses that cannot be resolved to a geo Country, geo Region, or geo City
// (and as a percentage of upeers-total, above)
        "anomaly-total": 625848,
        "anomaly-percentage": "1.85"
    },

// Summary of BTIHA, each all BTIH are unique.
// (Ie, if t002 and t134 have the same BTIH, a synthetic t275 torrent will be created that combine the upeers of
// t002 with the upeers of t134 and remove any duplicates.
    "collection-unique-btiha": {

// Number of unique BTIH in UBTIHA. If BTIHA is unique, call it a Unique BTIHA, or UBTIHA
        "btiha-size": 209,

// Number of unique peers, seeds, and anomalies (as above)
        "upeers-total": 20555123,
        "useeds-total": 9632217,
        "anomaly-total": 241874,
        "anomaly-percentage": "1.18"
    },

// Unit of measure for network transfer
    "transfer-units": "terabyte",

// Total network transfer size of the duration of the sample. 
// Assume every unique peer downloaded all the files in the torrent to completion once.
    "transfer-size": 43089.66182721779,

// Given transfer-size above, price cost of bandwidth on AWS
    "transfer-cost": "",

// For the UBTIHA above ie collection-unique-btiha, split the unique peers into groupings based on
// the resolution of the media media files.
// Ordered array of different resolution and/or encoding grouping for the media files.
// Sorted as descending by percentage of upeers. 
// Groups: 
// standard definition resolution (sd), encoded with MPEG4/AVC, aka H264
// standard definition resolution (sd), encoded with XviD
// ultra high definition resolution (uhd) of 2160p, encoded with any variant
// high definition resolution (hd) of 1080p, encoded with any variant
// high definition resolution (hd) of 720p, encoded with any variant
    "resolution-partitions": [
        {

// In this case, it is standard definition (sd) video  encoded with H264, with 39% of peers
            "number": 1,
            "name": "sd-264",
            "total-percentage-upeers": "39.71",
            "total-percentage-bytes": "9.28",
            "upeers-total": 8161820
        },

// In this case, it is high definition (hd) video  with the resolution of 720p, with 36% of peers
        {
            "number": 2,
            "name": "720",
            "total-percentage-upeers": "36.74",
            "total-percentage-bytes": "28.26",
            "upeers-total": 7551087
        },

// In this case, it is high definition (hd) video  with the resolution of 1080p, with 15% of peers
        {
            "number": 3,
            "name": "1080",
            "total-percentage-upeers": "15.11",
            "total-percentage-bytes": "42.65",
            "upeers-total": 3106228
        },

// In this case, it is standard definition (sd) video  encoded with xViD, with 6% of peers
        {
            "number": 4,
            "name": "sd-xvid",
            "total-percentage-upeers": "6.17",
            "total-percentage-bytes": "11.92",
            "upeers-total": 1268477
        },

// In this case, it is standard definition (sd) video  with unknown encoding, with 2% of peers
        {
            "number": 5,
            "name": "sd-other",
            "total-percentage-upeers": "2.27",
            "total-percentage-bytes": "7.89",
            "upeers-total": 467511
        },

// In this case, it is ultra high definition (uhd) video  with 4k resolution, with 0% of peers
        {
            "number": 6,
            "name": "2160",
            "total-percentage-upeers": "0.00",
            "total-percentage-bytes": "0.00",
            "upeers-total": 0
        }
    ],

// Ordered array of different geographic groups, descending by percentage of upeers. 
// Groups are three longitude regions (aka “slices”):
// AfroEurAsia -30 to 60
// AsiaPacifica 60 to 180.0
// Americas  -175.0 to -30
    "geo-slices-3-longitude-regions": [
        {

// Highest rank slice #1, with 43% of all upeers
            "number": 1,
            "name": "AfroEurAsia",
            "total-percentage-upeers": "43.93"
        },

// Second rank slice #2, with 30% of all upeers
        {
            "number": 2,
            "name": "AsiaPacifica",
            "total-percentage-upeers": "30.11"
        },

// Third rank slice #3, with 25% of all upeers
        {
            "number": 3,
            "name": "Americas",
            "total-percentage-upeers": "25.96"
        }
    ],


// Ordered array of different geographic groups, descending by percentage of upeers. 
// Group by Country, where 
// country-code is ISO Alpha-3 Numeric Country Code from MaxMind’s geolocation database
//  country-name is the name of the country from MaxMind’s geolocation database
    "geo-country-top-10": [
        {

// Largest percentage of upeers comes from USA with 11% 
            "number": 1,
            "country-code": "USA",
            "country-name": "United States of America",
            "total-percentage-upeers": "11.81",
            "upeers-total": 2428213
        },

... to. ...

// 9th largest percentage of upeers comes from France with 2%
        {
            "number": 10,
            "country-code": "FRA",
            "country-name": "France",
            "total-percentage-upeers": "2.02",
            "upeers-total": 414909
        }
    ],

// Ordered array of different geographic groups, descending by percentage of upeers. 
// Group by Country AND City AND Region or Region Code
    "geo-country-region-city-top-30": [
        {

// Largest percentage of upeers comes from no known region or city of the USA (aka, rural or uknown)
            "number": 1,
            "country-code": "USA",
            "country-name": "United States of America",
            "total-percentage-upeers": "2.98",
            "upeers-total": 612502
        },

... to. ...

// 30th largest percentage of upeers comes from the Manila suburb of Quezon City, Philippines with 0.37%
        {
            "number": 30,
            "country-code": "PHL",
            "country-name": "Philippines, Quezon City, F2",
            "total-percentage-upeers": "0.37",
            "upeers-total": 75619
        }
    ]
}
```