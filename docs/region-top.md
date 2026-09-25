---
layout: default
title: "Region Top 50"
author: "Benjamin De Kosnik <bkoz@gnu.org>"
description: "Cumulative downloader geography across the 2017–2026 annual repositories"
---

{::nomarkdown}
<img src="../resources/a60-logo-block-gray.simple.svg?sanitize=true" height="50" width="100" alt="Alpha60">
<link rel="stylesheet" href="../resources/izzi-table-wcag-22.css">
<link rel="stylesheet" href="../resources/region-rankings.css">
{:/}

[Swarm Results](../index.html)

<div class="region-rankings" markdown="1">

# Region Top 50

Top **50** media objects per region, ranked by the percentage of each object’s cumulative worldwide downloader weight located in that region. The shared inventory covers **646 annual samples** and **644 eligible distinct media objects** from **2017–2026**.

{% for region in site.data.region_rankings.regions %}
- [{{ region.label }}](../{{ region.path }})
{% endfor %}

## Reading the rankings

Each regional page shows the sample dates and duration, regional percentage, regional weight and matching worldwide weight. Media-object links open the selected annual audit pages. These rankings cover all eligible media objects; they are independent of the contributor-identity group sites.

The regions share the same retained sample per collection key and the same worldwide denominator. Full sample windows and media scopes differ, so the percentages describe geographic concentration rather than a comparison of audience sizes. Repeated keys use the latest sample end date, then start date, then repository year.

EUR-27 uses the fixed 27 current EU member-country ISO-3 codes for every sample year. [Membership source](https://european-union.europa.eu/easy-read_en). USA + CAN uses exactly those two country codes. See each table for its complete definition.

Calculated **2026-09-25**; rendered **2026-09-25**.

[Complete ranking ledger](../data/region-rankings.json.gz) · [Region definitions](../data/region-ranking-definitions.json) · [Generator and Top N option](../resources/rank-geographic-share.py)

</div>
