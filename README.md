# Wasteplan TRV
Wasteplan component for Trondheim Renholdsverk (TRV).
This component provides sensors for your bins and gives you status about bin pickup.

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

### CONFIGURATION VARIABLES
**bin_number**
(integer)(Required) The ID bin number.

**pickup_day**
(integer)(Optional) Day of the week for pickups. 1 = Monday and so on.

## Configuration
```yaml
sensor:
  - platform: wasteplan_trv
    bin_number: 774
    pickup_day: 0
```

⭐️ this repository if you found it useful ❤️

<a href="https://www.buymeacoffee.com/jonkristian" target="_blank"><img src="https://bmc-cdn.nyc3.digitaloceanspaces.com/BMC-button-images/custom_images/white_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
