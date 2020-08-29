#!/usr/bin/python3

from aiohttp import web
import os
import json
import logging
import optparse
import html_generator as html # my html generator


# Python web server for Fleet Manager. Or maybe Org Manager? (Name WIP)
# Note: This is designed to run behind a reverse-proxy. As such, it does not handle static files.


# handle command line options and args
version = "%prog 1.0"
usage = "usage: %prog [-p proxy_prefix]"
description = "Keeps track of a Star Citizen Fleet for an Organization plus easy json export for starship42.com/fleetview"
parser = optparse.OptionParser(version=version, usage=usage, description=description)
parser.add_option("-p", "--proxy_prefix", dest="proxy_prefix", default="", help="Set the proxy root this site will be attached to. (Default: '/')")
parser.add_option("-t", "--template", dest="template", default="template.html", help="Specify the html template that each page will be built off of. (Default: template.html)")
parser.add_option("-l", "--logfile", dest="logfile", default="fleet_manager.log", help="Specify the log file. (Default: fleet_manager.log)")
# parser.add_option("-s", "--ship_list", dest="ship_list", default="ships.json", help="!Not Implemented! Specify the local file for the list of ships. (Default: ships.json)")
# parser.add_option("-u", "--user_list", dest="user_list", default="users.json", help="!Not Implemented! Specify the local file for the list of users and their ships. (Default: users.json)")
# parser.add_option("-S", "--site_suffix", dest="suffix", default="", help="!Not Implemented! Set a default site suffix in the title of every page. (Default: None)")
# parser.add_option("-P", "--site_prefix", dest="prefix", default="", help="!Not Implemented! Set a default site prefix in the title of every page. (Default: None)")
(options, args) = parser.parse_args()


logging.basicConfig(filename=options.logfile, level=logging.INFO, format='%(asctime)s %(message)s')
logging.info('--------- A New Instance was Started ---------')


# Load page template.
if os.path.exists(options.template):
  with open(options.template,'r') as template_file:
    template = template_file.read()
else:
  template = '{title}{pageContent}'

default_headers = { "Content-Type": "text/html" }


# When the web server shuts down,
# make sure to flush the current state to disk.
async def on_shutdown(app):
  await html.save()
  logging.info('[Web_app]: Application shutdown.')

app.on_shutdown.append(on_shutdown)


# This is for the '/' route.
# It returns the table of all the ships.
async def view(request):
  return web.Response(text=template.format(title='Fleet Manager',pageContent=await html.table()), headers=default_headers)


# This handles the route for Adding a ship to the list.
async def add(request):
  params = request.rel_url.query

  ign = params.get("user")
  ship = params.get("ship")

  # If pledge is checked, it will show up in the list. Otherwise it won't.
  # If any value is sent for "pledge" in the query string this will return true.
  pledge = True if params.get("pledge") else False 

  return web.Response(text=template.format(title='Adding Ship',pageContent=await html.add(ign,ship,pledge)),headers=default_headers)


# This handles the route for Removing a ship from the list.
async def remove(request):
  params = request.rel_url.query

  ign = params.get("user")
  ship = params.get("ship")

  # If pledge is checked, it will show up in the list. Otherwise it won't.
  # If any value is sent for "pledge" in the query string this will return true.
  pledge = True if params.get("pledge") else False

  return web.Response(text=template.format(title='Removing Ship',pageContent=await html.remove(ign,ship,pledge)),headers=default_headers)

app = web.Application()

app.add_routes([
  web.get(options.proxy_prefix+'/', view),
  web.get(options.proxy_prefix+'/add', add),
  web.get(options.proxy_prefix+'/remove', remove)
])


if __name__ == '__main__':
  web.run_app(app)
