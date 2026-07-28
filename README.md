# Tildagon Googly Eyes

Give your badge googly eyes! Careful, they are prone to rolling around.

![A simulator screenshot of the app](./simulator_screenshot.png)

## Development

Run `make` to see a list of makefile targets. 

The `make run` target installs the badge on a simulator and runs it. It assumes the default location of the 
[badge simulator](https://tildagon.badge.emfcamp.org/tildagon-apps/simulate/) is at `~/code/badge-2024-software/sim/apps`.
Override the location by calling `make BADGE_SIM_DIR="/sim/path" run`

## Release

See the steps to [publish the app](https://tildagon.badge.emfcamp.org/tildagon-apps/publish/) to the tildagon app store.