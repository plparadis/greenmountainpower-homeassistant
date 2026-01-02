# GMP HA Home Assistant Integration

<p align="center">
  <img src="logo.png" alt="Green Mountain Power in Home Assistant" width="320" />
</p>

<p align="center">
  Hourly electricity usage, costs, and billing insights from your Green Mountain Power account — ready for Home Assistant dashboards, automations, and the Energy panel.
</p>

<p align="center">
  <a href="https://github.com/hacs/integration"><img src="https://img.shields.io/badge/HACS-Custom-41BDF5.svg" alt="HACS"></a>
  <a href="https://github.com/plparadis/gmp-ha/releases"><img src="https://img.shields.io/github/v/release/plparadis/greenmountainpower-homeassistant" alt="Release"></a>
  <a href="https://github.com/plparadis/gmp-ha/releases/latest"><img src="https://img.shields.io/github/downloads/plparadis/greenmountainpower-homeassistant/latest/total?label=latest%20downloads" alt="Release Downloads"></a>
  <a href="https://github.com/plparadis/gmp-ha/blob/dev/LICENSE"><img src="https://img.shields.io/github/license/plparadis/greenmountainpower-homeassistant.svg" alt="License"></a>
  <br/>
  <a href="https://github.com/plparadis/gmp-ha/commits/main"><img src="https://img.shields.io/github/last-commit/plparadis/greenmountainpower-homeassistant" alt="Last Commit"></a>
  <a href="https://github.com/plparadis/gmp-ha/stargazers"><img src="https://img.shields.io/github/stars/plparadis/greenmountainpower-homeassistant?style=social" alt="Stars"></a>
  <br/>
</p>

**Navigation:** [What is this?](#what-is-this-integration) • [Installation](#installation) • [Configuration](#configuration) • [Sensors](#sensors) • [Energy Dashboard](#home-assistant-energy-dashboard) • [Troubleshooting](#troubleshooting)

---

> ⚠️ **Community project**
>
> This integration is **not affiliated with, endorsed by, or supported by Green Mountain Power**.
>
> Do **not** contact GMP customer support for issues related to this integration. Please open an issue on GitHub instead.

---

## What is this integration?

This Home Assistant integration connects to your **Green Mountain Power online account** and retrieves your electricity usage data.

It allows you to:

- Track your **energy consumption** directly in Home Assistant
- Estimate your **electricity costs**
- Feed data into the **Home Assistant Energy dashboard**
- Build automations based on real usage data

This integration focuses on **simplicity and reliability**. It does **not** attempt to predict peaks or perform demand response.

---

## Features

- **Grid energy total** (kWh) — cumulative electricity usage reported by GMP
- **Daily energy usage** (kWh) — total consumption for the current day
- **Month-to-date comparison** — current month-to-date energy with previous month-to-date and the delta
- **Estimated bill** (USD) — cost estimate using a configurable price per kWh
- **Automatic updates** — data is refreshed every 30 minutes by default

---

## Requirements

- An active Green Mountain Power online account
- Access to usage data in the GMP customer portal
- Your **account number**, **username**, and **password**
- Home Assistant **2023.7 or newer**

---

## Installation

### Option 1: HACS (recommended)

[![Add to HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=plparadis&repository=gmp-ha&category=integration)

1. Click the badge above to open HACS with this repository pre-filled.
2. Click **Download**.
3. Restart Home Assistant.
4. Go to **Settings → Devices & Services → Add Integration**.
5. Search for **GMP HA** and complete setup.

### Option 2: Manual installation

1. Copy `custom_components/gmp_ha/` to `<config>/custom_components/gmp_ha/`.
2. Restart Home Assistant.
3. Add the integration from the UI: **Settings → Devices & Services → Add Integration**.

---

## Configuration

Setup is fully UI-based. You will be asked for:

- **Account number** (required)
- **Username** (required)
- **Password** (required)
- **Price per kWh** (optional, default `0.0`)
- **Backfill days** (optional, default `365`)

You can change optional values later under **Integration Options** without re-entering credentials.

To jump straight into setup from the README, use the quick link below:

[![Start integration](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start?domain=gmp_ha)

---

## Sensors

The integration creates the following sensors:

| Sensor                                        | Description                                                        |
| --------------------------------------------- | ------------------------------------------------------------------ |
| `sensor.gmp_ha_grid_energy`                   | Total energy drawn from the grid (kWh)                             |
| `sensor.gmp_ha_daily_energy`                  | Energy used today (kWh)                                            |
| `sensor.gmp_ha_yesterday_energy`              | Energy used yesterday (kWh)                                        |
| `sensor.gmp_ha_current_hour_energy`           | Energy used in the current hour (kWh)                              |
| `sensor.gmp_ha_previous_hour_energy`          | Energy used in the previous hour (kWh)                             |
| `sensor.gmp_ha_hourly_trend`                  | Difference between current and previous hour usage (kWh)           |
| `sensor.gmp_ha_daily_trend`                   | Difference between today and yesterday usage (kWh)                 |
| `sensor.gmp_ha_current_month_energy`          | Energy used in the current month (kWh)                             |
| `sensor.gmp_ha_previous_month_energy`         | Energy used in the previous month (kWh)                            |
| `sensor.gmp_ha_month_to_date_energy`          | Energy used so far this month (kWh)                                |
| `sensor.gmp_ha_previous_month_to_date_energy` | Energy used during the same number of days last month (kWh)        |
| `sensor.gmp_ha_month_to_date_trend`           | Difference between this month-to-date and last month-to-date (kWh) |
| `sensor.gmp_ha_estimated_bill`                | Estimated cost for the current billing period (USD)                |
| `sensor.gmp_ha_previous_bill`                 | Cost of the previous month based on configured pricing (USD)       |

### Attributes

Sensors may expose attributes such as:

- Account number
- Billing period
- Last update timestamp

---

## Home Assistant Energy dashboard

To use this integration in the **Energy** dashboard:

1. Go to **Settings → Dashboards → Energy**.
2. Under **Electricity grid consumption**.
3. Select `sensor.gmp_ha_grid_energy`.
4. Set the unit to **kWh** if prompted.

Daily energy values will automatically populate historical views once data is available.

---

## Troubleshooting

### Setup fails or credentials are rejected

- Verify credentials by logging into the GMP web portal.
- Check for special characters in the password.
- Make sure the account has active service.

### No data after setup

- Wait up to **30–60 minutes** after first install.
- Check **Settings → System → Logs**.
- Enable debug logging:

  ```yaml
  logger:
    logs:
      custom_components.gmp_ha: debug
  ```

### Need help?

- Open a [GitHub issue](https://github.com/plparadis/gmp-ha/issues) with details and logs.
- Visit the [Home Assistant Community forum](https://community.home-assistant.io/).

---

<p align="center">
  <sub>If this integration helps you monitor your energy usage, please consider starring the repository on GitHub!</sub>
</p>
