# Nagios Plugin for UniFi Monitoring

This Nagios plugin allows monitoring of UniFi controller statistics such as connected devices, access points, and system health. It performs API calls to a UniFi controller and provides status information based on the configured thresholds.
## Prerequisites

   -  Python 3.x
   -  Nagios monitoring system installed and configured

## Installation

   1. Clone or download the repository to your Nagios server.
   2. Ensure Python requests library is installed: pip install requests.
   3.  Set up the necessary environment variables for authentication:
        UNIFI_USERNAME: UniFi controller username
        UNIFI_PASSWORD: UniFi controller password

## Usage

The plugin supports the following commands:

  - users: Checks the number of connected devices.
  - aps: Checks the status and number of Access Points.
  - status: Checks the overall system health status.

## Example Command

```python unifi_nagios_plugin.py users```

## Exit Codes

The plugin returns the following exit codes:

    0: OK - within acceptable thresholds
    1: WARNING - nearing thresholds or minor issues detected
    2: CRITICAL - outside acceptable thresholds or significant issues detected
    3: UNKNOWN - errors fetching data or unexpected issues

## Thresholds

  - Connected Devices (users):
     - OK: Less than or equal to 100
     - WARNING: Between 101 and 150
     - CRITICAL: Above 150

  - Access Points (aps):
    - OK: Number of APs matches the number of adopted APs
    - WARNING: Number of APs differs from adopted APs

  - System Status (status):
    - OK: All subsystems operational
    - WARNING: Not all subsystems are operational

# Notes

  - Ensure proper configuration of thresholds according to your network's specifications.
  - For any issues or feature requests, please open an issue in this repository.

# Contributors
  -  Felipe Lima
