# Green Mountain Power Home Assistant

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![pre-commit][pre-commit-shield]][pre-commit]
[![Black][black-shield]][black]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

**TO BE REMOVED: If you need help, as a developer, to use this custom component tempalte,
please look at the [User Guide in the Cookiecutter documentation](https://cookiecutter-homeassistant-custom-component.readthedocs.io/en/stable/quickstart.html)**

**This component will set up the following platforms.**

| Platform | Description |
| --- | --- |
| `sensor` | Energy usage and bill estimates from Green Mountain Power. |

![example][exampleimg]

## Installation

### HACS (recommended)

The integration can be installed directly from [HACS][hacs]. Use the quick links below or follow the manual steps.

**One-click setup**

[![Add repository to HACS](https://my.home-assistant.io/badges/hacs_repository.svg)][hacs-repository]
[![Start integration setup](https://my.home-assistant.io/badges/config_flow_start.svg)][integration-start]

1. In Home Assistant, open **HACS → Integrations → Custom repositories** and add this repository URL as the source. Select **Integration** as the category.
2. Return to **HACS → Integrations**, search for **Green Mountain Power Home Assistant**, and click **Download**.
3. Restart Home Assistant.
4. Open **Settings → Devices & Services → Add Integration**, search for **Green Mountain Power Home Assistant**, and follow the prompts (or use the button above to jump directly to the setup dialog).

### Manual installation

1. Open the directory for your Home Assistant configuration (where `configuration.yaml` is located).
2. If the `custom_components` directory does not exist, create it.
3. Inside `custom_components`, create a folder named `greenmountainpower`.
4. Download **all** files from this repository's `custom_components/greenmountainpower/` directory and place them in the folder you created.
5. Restart Home Assistant.
6. In the HA UI go to **Settings → Devices & Services → Add Integration**, click "+", and search for **Green Mountain Power Home Assistant**.

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/greenmountainpower/translations/en.json
custom_components/greenmountainpower/translations/fr.json
custom_components/greenmountainpower/translations/nb.json
custom_components/greenmountainpower/__init__.py
custom_components/greenmountainpower/api.py
custom_components/greenmountainpower/config_flow.py
custom_components/greenmountainpower/const.py
custom_components/greenmountainpower/manifest.json
custom_components/greenmountainpower/sensor.py
```

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

### Support the project (optional)

The "Buy Me a Coffee" badge above is simply a tip jar for the maintainer. Using this integration does **not** require creating a Buy Me a Coffee account or donating—it's entirely optional and separate from installation.

## Credits

This project was generated from [@oncleben31](https://github.com/oncleben31)'s [Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) template.

Code template was mainly taken from [@Ludeeus](https://github.com/ludeeus)'s [integration_blueprint][integration_blueprint] template

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[black]: https://github.com/psf/black
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
[buymecoffee]: https://www.buymeacoffee.com/plparadis
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/plparadis/greenmountainpower-homeassistant.svg?style=for-the-badge
[commits]: https://github.com/plparadis/greenmountainpower-homeassistant/commits/main
[hacs]: https://hacs.xyz
[hacs-repository]: https://my.home-assistant.io/redirect/hacs_repository/?owner=plparadis&repository=greenmountainpower-homeassistant&category=integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/plparadis/greenmountainpower-homeassistant.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40plparadis-blue.svg?style=for-the-badge
[pre-commit]: https://github.com/pre-commit/pre-commit
[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/plparadis/greenmountainpower-homeassistant.svg?style=for-the-badge
[releases]: https://github.com/plparadis/greenmountainpower-homeassistant/releases
[user_profile]: https://github.com/plparadis
[integration-start]: https://my.home-assistant.io/redirect/config_flow_start?domain=greenmountainpower
