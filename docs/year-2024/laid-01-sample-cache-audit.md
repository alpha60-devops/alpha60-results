---
layout: default
title: "Laid Sample Cache Audit"
author: "Benjamin De Kosnik <bkoz@gnu.org>"
description: "Cache coverage and visualization audit for one media object."
---

# Laid sample cache audit

## 1. Media object

| Field | Value |
| --- | --- |
| Media object | Laid |
| Collection key | `laid-01` |
| Sample dates | 2024-12-19-to-2025-04-09 |
| Sample days | 112 (2024–2025) |
| BTIH count | 278 |
| Unique BTIH count | 255 |
| Downloaders total | 16,843,064 |
| Uploaders total | 289,940 |
| Data version | `2026-08-05` |
| IP geolocation version | `6:1777968300` |

## 2. Cache coverage report

- Generated: 2026-08-21T05:55:26Z
- Sample directory: `/home/bkoz/src/alpha60-samples/laid-01`
- Hour directories: 2666
- Zero-length sample files: 0
- Other unparsable sample files: 0
- Hourly discontinuities: 1 (1 missing hours)
- Missing days: 0

### Sample archive discontinuities

- hourly gap: last `2025-03-30 01:06`, resumed `2025-03-30 03:06` — missing 1 hour(s)

## 3. Visualization pass — graphs

### Downloads by week cumulative (normalized start)

![laid-01 downloads by week](figures/laid-01-downloads-by-week-laid-01-week.svg)

### Downloads by day, Saturday and Sunday in gray

![laid-01 downloads by day](figures/laid-01-downloads-by-day-day.svg)

## 4. Visualization pass — maps

### Cumulative network infrastructure

[![Laid cumulative map](figures/laid-01-carto.png)](figures/laid-01-carto-4k.webp){:target="_blank" rel="noopener"}

### Cumulative data maps

![laid-01-data-cumulative](figures/laid-01-data-cumulative.webp)

![laid-01-data-hd](figures/laid-01-data-hd.webp)

![laid-01-data-sd](figures/laid-01-data-sd.webp)
