<table>
<tr>
<td width="100">
<img src="https://github.com/TheMegamind/PurpleAir_AQI/blob/main/assets/PurpleAir.png"
     width="100" alt="PurpleAir Logo">
</td>
<td>

# PurpleAir AQI

</td>
</tr>
</table>

### A custom integration for Home Assistant that calculates AQI, EPA categories, and EPA standard health advisories from nearby PurpleAir sensors.

### Key features include multi-sensor averaging, configurable conversion formulas, and automation-friendly polling control to manage API usage while ensuring timely, hyperlocal AQI data — especially during significant air quality events.

[![GitHub release](https://img.shields.io/github/v/release/TheMegamind/PurpleAir_AQI)](https://github.com/TheMegamind/PurpleAir_AQI/releases)
[![GitHub last commit](https://img.shields.io/github/last-commit/TheMegamind/PurpleAir_AQI)](https://github.com/TheMegamind/PurpleAir_AQI/commits/)
[![HACS Default](https://img.shields.io/badge/HACS-Default-blue.svg)](https://hacs.xyz)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024.4%2B-blue?logo=home-assistant)](https://www.home-assistant.io)
[![Python](https://img.shields.io/badge/Python-3.14%2B-blue?logo=python&logoColor=white)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ☁️ Why Use PurpleAir?

PurpleAir sensors provide **neighborhood-level, real-time air quality data**, which can provide a more representative picture of the air quality where you live. This is especially useful when:

* Official air quality monitors are **miles away**
* **Wildfire smoke** affects neighborhoods unevenly
* Terrain, inversions, or weather create **micro-climates**

---

## ✨ PurpleAir AQI Features

### Core Capabilities

* Automatically discovers **public PurpleAir sensors** near a given location
* **Multi-sensor averaging** of nearby monitors for improved stability and reliability, with automatic filtering of low-confidence sensors
* Optional **weighted averaging** by distance from the search center
* **Dynamic polling frequency** — automations can raise or lower the update interval on the fly (e.g., tighten to 10 min during a wildfire, relax to 30 min between events) to ensure responsive monitoring while minimizing API usage
* Optional use of **private sensors** via sensor index + read key

 ***Note:** If desired, this integration can be installed alongside the [official Home Assistant PurpleAir integration](https://www.home-assistant.io/integrations/purpleair/), which exposes raw per-sensor readings, without conflict.*

---

## 🔢 PM₂.₅ Conversion Formulas

This integration supports multiple conversion methods used by air-quality agencies and research groups:

| Conversion | Best For | Notes |
|-----------|---------|-------|
| **US EPA** | Most users | Recommended default |
| **Woodsmoke** | Wildfire regions | Better smoke accuracy |
| **AQ&U** | Mountain / inversion zones | Utah DEQ |
| **LRAPA** | Humid climates | Oregon LRAPA |
| **CF = 1** | Indoor sensors | Raw factory value |
| **None** | Research | No correction |

> **Recommendation:**
> Use US EPA for typical conditions. Switch to Woodsmoke during wildfire events. AQ&U and LRAPA are regional formulas developed for specific areas (Salt Lake City and Lane County, Oregon respectively).

For the official EPA AQI color scale and health guidance, see [AirNow AQI Basics](https://www.airnow.gov/aqi/aqi-basics/).

---

## 📦 Installation

### HACS (Recommended)

PurpleAir AQI is available in the [HACS](https://hacs.xyz) default store.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=TheMegamind&repository=PurpleAir_AQI&category=integration)

Or search for "PurpleAir AQI" in HACS → Integrations.

### HACS Custom Repository

To install a specific version or branch:
1. Open HACS → Integrations → ⋮ → Custom repositories
2. Add: `https://github.com/TheMegamind/PurpleAir_AQI`
3. Category: Integration
4. Install → Restart Home Assistant

After installation via either method, go to **Settings → Devices & Services → Add Integration** and select **PurpleAir AQI**.

---

## ⚙️ Configuration

Setup uses a two-step flow.

### Step 1 – API Key & Search Mode

> A PurpleAir API key is required before setup. [Register or retrieve your key here](https://community.purpleair.com/t/about-the-purpleair-api/7145).

| Setting | Description |
|-------|-------------|
| **API Key** | Your PurpleAir API key |
| **Name** | A name to identify this location (e.g. Home, Cabin, Office) |
| **Search by location** | Enable to discover nearby sensors automatically; disable to enter a specific sensor index |

### Step 2a – Location Search *(if Search by location is enabled)*

| Setting | Description |
|-------|-------------|
| **Latitude / Longitude** | Center point for sensor search |
| **Search radius** | Search radius (miles or km) |
| **Distance unit** | Miles or kilometers |
| **Distance-weighted averaging** | Weight readings by inverse distance from the search center |
| **PM₂.₅ conversion formula** | Formula applied before AQI calculation |
| **PM₂.₅ averaging period** | Time window for PM₂.₅ readings (default: 10 min — matches the PurpleAir map). Has no effect when using LRAPA, Woodsmoke, or CF=1 conversions. |
| **Update interval** | Polling interval (minutes) |

### Step 2b – Specific Sensor *(if Search by location is disabled)*

| Setting | Description |
|-------|-------------|
| **Sensor index** | PurpleAir sensor index number |
| **Read key** | Required for private sensors only |
| **PM₂.₅ conversion formula** | Formula applied before AQI calculation |
| **PM₂.₅ averaging period** | Time window for PM₂.₅ readings (default: 10 min — matches the PurpleAir map). Has no effect when using LRAPA, Woodsmoke, or CF=1 conversions. |
| **Update interval** | Polling interval (minutes) |

### Options (after setup)

Editable at any time via **Settings → Devices & Services → Configure**:

* Latitude / Longitude
* Name
* Search range (defines a rectangular bounding box around the specified coordinates)
* Miles / kilometers
* Weighted averaging (weights readings by inverse distance — nearer sensors have more influence)
* Conversion method
* PM₂.₅ averaging period
* Update interval

---

## 📊 Entities Provided

### Sensors

| Entity | Description |
|------|-------------|
| **AQI** | Calculated AQI value (0–500+) |
| **AQI Delta** | Change in AQI since the previous poll — useful for automations that respond to rapidly worsening or improving air quality |
| **AQI Color** | EPA color for the current AQI category (Green / Yellow / Orange / Red / Purple / Maroon) — intended for use in dashboards and HTML-enabled notifications such as Pushover |
| **Category** | Official EPA AQI category (Good, Moderate, Unhealthy for Sensitive Groups, etc.) |
| **Conversion** | Active PM₂.₅ conversion formula |
| **Health Advisory** | Health guidance based on the current AQI category, derived from EPA/AirNow descriptions |
| **Health Status** | `online` / `offline` |
| **Sites** | Sensors contributing to the average |

> Only sensors with a confidence score ≥ 90 contribute to AQI averages and appear in the **Sites** entity. This ensures data quality by filtering out sensors with channel disagreement or active flags, even if they are visible on the official PurpleAir map.

### Control

| Entity | Description |
|------|-------------|
| **Update Interval** | Live polling interval control (minutes) |

> The **Update Interval** control appears directly on the **device page** and takes effect immediately.

---

## ⏱ Update Interval Behavior

| Interval | Effect |
|--------|-------|
| **10 min** | Minimum useful interval when using 10-min PM₂.₅ averaging |
| **15–30 min** | Recommended balance |
| **60 min** | Lowest API usage |

**Notes:**

* Shorter intervals improve responsiveness, **not accuracy**
* Wildfire monitoring may benefit from shorter intervals
* Interval changes apply immediately without restart

---

## 💡 Example Automation

These examples show how to use AQI Delta and Category to drive dynamic polling. Adapt entity IDs and thresholds to your own setup.

```yaml
# Tighten polling when air quality is worsening rapidly
automation:
  - alias: "PurpleAir — Tighten polling on rapid AQI spike"
    trigger:
      - platform: numeric_state
        entity_id: sensor.purpleair_aqi_aqi_delta
        above: 50
    action:
      - service: number.set_value
        target:
          entity_id: number.purpleair_aqi_update_interval
        data:
          value: 10

  # Restore normal polling when conditions improve
  - alias: "PurpleAir — Restore polling when AQI improves"
    trigger:
      - platform: state
        entity_id: sensor.purpleair_aqi_category
        to:
          - "Good"
          - "Moderate"
    action:
      - service: number.set_value
        target:
          entity_id: number.purpleair_aqi_update_interval
        data:
          value: 30
```

---

## 📄 License

MIT License — see `LICENSE`.

---

## ⚠️ Trademarks & Disclaimers

* **PurpleAir®** name and logo are trademarks of **PurpleAir, Inc.**
* **Home Assistant®** name and logo are trademarks of **Nabu Casa, Inc.**
* This project is **independently maintained**, and not affiliated with or endorsed by PurpleAir or Nabu Casa.
* This project's code and documentation were reviewed and refined with the assistance of [Claude AI](https://claude.ai) (Anthropic).
