# Green Mountain Power Home Assistant Integration

<p align="center">
  <img src="logo.png" alt="Green Mountain Power in Home Assistant" width="320" />
</p>

<p align="center">
  <a href="https://github.com/hacs/integration"><img src="https://img.shields.io/badge/HACS-Custom-41BDF5.svg" alt="HACS"></a>
  <a href="https://github.com/plparadis/greenmountainpower-homeassistant/releases"><img src="https://img.shields.io/github/v/release/plparadis/greenmountainpower-homeassistant" alt="Release"></a>
  <a href="https://github.com/plparadis/greenmountainpower-homeassistant/releases/latest"><img src="https://img.shields.io/github/downloads/plparadis/greenmountainpower-homeassistant/latest/total?label=latest%20downloads" alt="Release Downloads"></a>
  <a href="https://github.com/plparadis/greenmountainpower-homeassistant/releases"><img src="https://img.shields.io/github/downloads/plparadis/greenmountainpower-homeassistant/total?label=total%20downloads" alt="Total Downloads"></a>
  <a href="https://github.com/plparadis/greenmountainpower-homeassistant/blob/main/LICENSE"><img src="https://img.shields.io/github/license/plparadis/greenmountainpower-homeassistant.svg" alt="License"></a>
  <br/>
  <a href="https://github.com/plparadis/greenmountainpower-homeassistant/commits/main"><img src="https://img.shields.io/github/last-commit/plparadis/greenmountainpower-homeassistant" alt="Last Commit"></a>
  <a href="https://github.com/plparadis/greenmountainpower-homeassistant/stargazers"><img src="https://img.shields.io/github/stars/plparadis/greenmountainpower-homeassistant?style=social" alt="Stars"></a>
</p>

<p align="center">
  Hourly electricity usage, costs, and billing insights from your Green Mountain Power account—ready to power Home Assistant dashboards, automations, and the Energy panel.
</p>

**Quick navigation:** [Installation](#installation) • [Configuration](#configuration) • [Sensors](#sensors) • [Troubleshooting](#troubleshooting) • [Contributing](#contributing)

> **⚠️ Community project** — This integration is not affiliated with or supported by Green Mountain Power. Please open an [issue on GitHub](https://github.com/plparadis/greenmountainpower-homeassistant/issues) if you run into problems.

## Features

- **Grid energy total** (kWh) – cumulative usage fetched from your GMP account.
- **Daily energy usage** (kWh) – total consumption for the current day.
- **Estimated bill** (USD) – running cost estimate using your configured price per kWh.
- Data is refreshed every 30 minutes by default.

## Requirements

- An active Green Mountain Power online account with access to usage data.
- Your **account number**, **username**, and **password** for Green Mountain Power online services.
- Home Assistant 2023.7 or later (tested with modern releases).

## Installation

### HACS (recommended)

1. In Home Assistant, open **HACS → Integrations → Custom repositories** and add this repository URL as a **Integration** source.
2. From **HACS → Integrations**, search for **Green Mountain Power Home Assistant** and click **Download**.
3. Restart Home Assistant.
4. Go to **Settings → Devices & Services → Add Integration** and search for **Green Mountain Power Home Assistant**.

You can also use Home Assistant quick links:

- [Add repository to HACS](https://my.home-assistant.io/redirect/hacs_repository/?owner=plparadis&repository=greenmountainpower-homeassistant&category=integration)
- [Start integration setup](https://my.home-assistant.io/redirect/config_flow_start?domain=greenmountainpower)

### Manual installation

1. Download the contents of `custom_components/greenmountainpower/` into `<config>/custom_components/greenmountainpower/` in your Home Assistant configuration directory.
2. Restart Home Assistant.
3. Add the integration via **Settings → Devices & Services → Add Integration** and search for **Green Mountain Power Home Assistant**.

## Configuration

Setup is completed entirely through the Home Assistant UI. When adding the integration you will be prompted for:

- **Account number** (required)
- **Username** (required)
- **Password** (required)
- **Price per kWh** (optional; default `0.0` USD)
- **Backfill days** (optional; default `365`) – how many days of history to import on first setup.

You can adjust the optional values later under **Integration Options** without re‑entering your credentials.

## Sensors

The integration creates the following sensors:

- `sensor.green_mountain_power_grid_energy` – Total energy drawn from the grid (kWh).
- `sensor.green_mountain_power_daily_energy` – Energy used today (kWh).
- `sensor.green_mountain_power_estimated_bill` – Estimated cost for the current billing period (USD).

## Troubleshooting

- Verify your Green Mountain Power credentials by logging into the web portal; invalid credentials will prevent setup.
- If setup fails with a connection error, wait a few minutes and try again; GMP’s API can occasionally be slow to respond.
- Enable debug logging in `configuration.yaml` if you need more detail:
  ```yaml
  logger:
    logs:
      custom_components.greenmountainpower: debug
  ```

## Contributing

Contributions are welcome! Please review the [CONTRIBUTING.md](CONTRIBUTING.md) guidelines before opening issues or pull requests.

## License

This project is licensed under the [MIT License](LICENSE).
