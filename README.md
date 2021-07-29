# Wasteplan TRV
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

Wasteplan component for Trondheim Renholdsverk (TRV).
This component provides sensors for your bins or containers and gives you status about pickup.

[![image-1.png](https://i.postimg.cc/hGs0gPr7/image-1.png)](https://postimg.cc/f33dfs1w)

## Installation

### Manual installation
Download or clone and copy the folder `custom/components/wasteplan_trv` into your `custom_components/`

### Installation via Home Assistant Community Store (HACS)
1. Ensure [HACS](http://hacs.xyz/) is installed.
2. Search for and install the "Wasteplan TRV" integration
3. Configure the sensor
4. Restart Home Assistant

## Finding your ID

To locate your ID, append your address to the end of one of the URLs below, either bin or container.
- Bins: https://trv.no/wp-json/wasteplan/v1/bins/?s=
- Containers: https://trv.no/wp-json/wasteplan/v1/containers/?s=

### Configuration variables
| Variable |  Required  |  Type  | Description |
| -------- | ---------- | ----------- | ----------- |
| `id` | yes | integer |  Bin/Container ID. |
| `pickup_day` | no | integer | Pickup day of the week. Defaults to 0 (Monday). |

## Example
```yaml
sensor:
  - platform: wasteplan_trv
    id: 774
    pickup_day: 0
```

⭐️ this repository if you found it useful ❤️

<a href="https://www.buymeacoffee.com/jonkristian" target="_blank"><img src="https://bmc-cdn.nyc3.digitaloceanspaces.com/BMC-button-images/custom_images/white_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
