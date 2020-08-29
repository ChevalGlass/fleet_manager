# Fleet Manager (name WIP)
This application generates a basic web which displays added users ships which have been purchased by Pledge or aUEC in-game.

## Overview
The application is separated into three parts.

- The main web server. (Handles requests behind a reverse_proxy. aka Does not handle static files, only dynamic output.)
- The html generator. (Handles all of the html generation.)
- The back-end data. (Handles all of the data access/transformations.)

## Getting started

1. Install Git
2. Clone this repo `git clone https://github.com/ChevalGlass/fleet_manager.git`
3. Install python3.7+
4. Install additional python modules (via pip install <module>)
	- asyncio
	- aiohttp (Ideally with all the speedups `pip install aiohttp[speedups]` [aiohttp docs](https://docs.aiohttp.org/en/stable/))

