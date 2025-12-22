# Green Mountain Power Home Assistant Integration

<p align="center">
  <img src="logo.png" alt="Green Mountain Power in Home Assistant" width="320" />
</p>

<p align="center">
  Hourly electricity usage, costs, and billing insights from your Green Mountain Power account — ready for Home Assistant dashboards, automations, and the Energy panel.
</p>

<p align="center">
  <a href="https://github.com/hacs/integration"><img src="https://img.shields.io/badge/HACS-Custom-41BDF5.svg" alt="HACS"></a>
  <a href="https://github.com/plparadis/greenmountainpower-homeassistant/releases"><img src="https://img.shields.io/github/v/release/plparadis/greenmountainpower-homeassistant" alt="Release"></a>
  <a href="https://github.com/plparadis/greenmountainpower-homeassistant/releases/latest"><img src="https://img.shields.io/github/downloads/plparadis/greenmountainpower-homeassistant/latest/total?label=latest%20downloads" alt="Release Downloads"></a>
  <a href="https://github.com/plparadis/greenmountainpower-homeassistant/blob/main/LICENSE"><img src="https://img.shields.io/github/license/plparadis/greenmountainpower-homeassistant.svg" alt="License"></a>
  <br/>
  <a href="https://github.com/plparadis/greenmountainpower-homeassistant/commits/main"><img src="https://img.shields.io/github/last-commit/plparadis/greenmountainpower-homeassistant" alt="Last Commit"></a>
  <a href="https://github.com/plparadis/greenmountainpower-homeassistant/stargazers"><img src="https://img.shields.io/github/stars/plparadis/greenmountainpower-homeassistant?style=social" alt="Stars"></a>
</p>

---

> ⚠️ **Community project**
>
> This integration is **not affiliated with, endorsed by, or supported by Green Mountain Power**.
>
> Do **not** contact GMP customer support for issues related to this integration.
> Please open an issue on GitHub instead.

---

## What is this integration?

This Home Assistant integration connects to your **Green Mountain Power online account** and retrieves your electricity usage data.

It allows you to:
- Track your **energy consumption** directly in Home Assistant
- Estimate your **electricity costs**
- Feed data into the **Home Assistant Energy dashboard**
- Build automations based on real usage data

This integration focuses on **simplicity and reliability**.
It does **not** attempt to predict peaks or perform demand response.

---

## Features

- **Grid energy total** (kWh)
  Cumulative electricity usage reported by GMP.

- **Daily energy usage** (kWh)
  Total consumption for the current day.

- **Estimated bill** (USD)
  Cost estimate using a configurable price per kWh.

- **Automatic updates**
  Data is refreshed every 30 minutes by default.

---

## Requirements

- An active Green Mountain Power online account
- Access to usage data in the GMP customer portal
- Your **account number**, **username**, and **password**
- Home Assistant **2023.7 or newer**

---

## Installation

### HACS (recommended)

1. Open **HACS → Integrations → Custom repositories**
2. Add this repository URL as **Integration**
3. Search for **Green Mountain Power Home Assistant**
4. Click **Download**
5. Restart Home Assistant
6. Go to **Settings → Devices & Services → Add Integration**
7. Search for **Green Mountain Power Home Assistant**

Quick links:
- [Add repository to HACS](https://my.home-assistant.io/redirect/hacs_repository/?owner=plparadis&repository=greenmountainpower-homeassistant&category=integration)
- [Start integration setup](https://my.home-assistant.io/redirect/config_flow_start?domain=greenmountainpower)

### Manual installation

1. Copy `custom_components/greenmountainpower/` to
   `<config>/custom_components/greenmountainpower/`
2. Restart Home Assistant
3. Add the integration from the UI

---

## Configuration

Setup is fully UI-based. You will be asked for:

- **Account number** (required)
- **Username** (required)
- **Password** (required)
- **Price per kWh** (optional, default `0.0`)
- **Backfill days** (optional, default `365`)

You can change optional values later under **Integration Options** without re-entering credentials.

---

## Sensors

The integration creates the following sensors:

| Sensor | Description |
|------|------------|
| `sensor.green_mountain_power_grid_energy` | Total energy drawn from the grid (kWh) |
| `sensor.green_mountain_power_daily_energy` | Energy used today (kWh) |
| `sensor.green_mountain_power_estimated_bill` | Estimated billing cost (USD) |

### Attributes

Sensors may expose attributes such as:
- Account number
- Billing period
- Last update timestamp

---

## Home Assistant Energy dashboard

To use this integration in the **Energy** dashboard:

1. Go to **Settings → Dashboards → Energy**
2. Under **Electricity grid consumption**
3. Select `sensor.green_mountain_power_grid_energy`
4. Set the unit to **kWh** if prompted

Daily energy values will automatically populate historical views once data is available.

---

## Troubleshooting

### Setup fails or credentials are rejected
- Verify credentials by logging into the GMP web portal
- Check for special characters in the password
- Make sure the account has active service

### No data after setup
- Wait up to **30–60 minutes** after first install
- Check **Settings → System → Logs**
- Enable debug logging:
  ```yaml
  logger:
    logs:
      custom_components.greenmountainpower: debug
