# LinkedIn Report
I want to know some stats about my LinkedIn connections!
This project crawls your profile connections (first level), uses an API to determine their genders and shows you their totals.

## Installation
This project needs python3 and a few pip packages.
To install pip dependencies:
- pip install -r pip_requirements

## Usage
Set up config.json based on the values on configs.json.default and run:
- python report.py

### Configurations
- default_country - default country of origin for profiles, used to help the gender engines be more accurate.
- linkedin_username - your linkedin user name
- linkedin_password - your linkedin password
- debug_mode - set to true and it will use a bunch of test profiles instead of gathering real data
- skip_gathering - set true if you have previously executed this script and just want to display the report again.

## TODO
- Find a better gender api
- Unit test everything

## DISCLAIMER
This is a study project and should not be used by anyone. I take no responsibility over the usage of these scripts or the data gathered by it.
