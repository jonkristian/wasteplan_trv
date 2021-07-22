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

## Setup

Append your address to the end of the following url to look up your address id (bin_number):
https://trv.no/wp-json/wasteplan/v1/bins/?s=

### Configuration variables
| Variable |  Required  |  Type  | Description |
| -------- | ---------- | ----------- | ----------- |
| `bin_number` | yes | integer |  Bin number ID. |
| `container` | no | bool | Set to `true` if you use containers. |
| `pickup_day` | no | integer | Pickup day of the week. Monday starts with 0. |

## Example
```yaml
sensor:
  - platform: wasteplan_trv
    bin_number: 774
    container: false
    pickup_day: 0
```

⭐️ this repository if you found it useful ❤️

<a href="https://www.buymeacoffee.com/jonkristian" target="_blank"><img src="https://bmc-cdn.nyc3.digitaloceanspaces.com/BMC-button-images/custom_images/white_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
