#!/usr/bin/python3

import os
import json
import asyncio
import logging


# Load Ship List
if os.path.exists('ships.json'):
  with open('ships.json','r') as ship_list_file:
    ship_list = json.load(ship_list_file)
    logging.info('Ship list loaded.')
else:
  ship_list = {}
  logging.warning('Ship list failed to load. File: ships.json does not exist.')


# Load User List
if os.path.exists('users.json'):
  with open('users.json','r') as user_list_file:
    user_list = json.load(user_list_file)
    logging.info('User list loaded.')
else:
  user_list = {}
  logging.info('users.json does not exist. Empty list instantiated.')


# Return a dictionary of all the ships with just their names/ids.
async def ships():
  return ship_list


# Return a dictionary of all the users and their ship lists.
async def users():
  return user_list


# Add a ship given the username (ign) ship id (ship), and whether it was a pledge or not (True/False).
async def addShip(ign, ship, pledge):
  # Set pledge type to handle both cases.
  if pledge:
    pledge_type = "ships_pledge"
  else:
    pledge_type = "ships_aUEC"

  # Look at every user and find a match to the one given.
  for user in user_list:
    if user.get("name") == ign:
      if user.get(pledge_type).get(ship) == None:
        user[pledge_type][ship] = 1
      else:
        user[pledge_type][ship] = user.get(pledge_type).get(ship) + 1
      

      # If we found and successfully added the ship. Not it in the logs and return true.
      logging.info(f'[Added]: User:{ign} Ship: {ship} Pledge: {pledge}\n{user_list}')
      return True

  # If we did not find a match for the user. Add them as a new entry.
  try:
    if pledge:
      user_list.append( {"name": ign, "ships_pledge": { ship: 1 }, "ships_aUEC": { } } )
    else:
      user_list.append( {"name": ign, "ships_pledge": { }, "ships_aUEC": { ship: 1 } } )
    return True
  except Exception as error:
    logging.warning(error)
    return False


async def removeShip(ign, ship, pledge):
  pledge_type = "ships_pledge" if pledge else "ships_aUEC"

  for user in user_list:
    if user.get("name") == ign:
      if user.get(pledge_type).get(ship) != None:
        if user.get(pledge_type).get(ship) > 1:
          user[pledge_type][ship] = user.get(pledge_type).get(ship) - 1
        elif user.get(pledge_type).get(ship) == 1:
          user.get(pledge_type).pop(ship) # Ship removed.

          # check if the users still has other ships. (if they don't. remove them.)
          if len(user.get("ships_pledge").keys()) == 0 and len(user.get("ships_aUEC").keys()) == 0:
            user_list.remove(user)
      logging.info(f'[Removed]: User:{ign} Ship: {ship} Pledge: {pledge}\n{user_list}')
      return True
  # User not in the system. Nothing to remove.
  return False


async def saveUsers():

  try:
    # check if the user_dict is different than the user_list before trying to save.
    current_users_on_file = {}
    try:
      if os.path.exists('users.json'):
        with open('users.json','r') as current_users_file:
          current_users_on_file = json.load(current_users_file)
    except FileNotFoundError as e:
      logging.warn(f'The save file was not found. Was it mistakenly deleted? {e}')

    # If there has been changes. We save to disk again.
    if current_users_on_file != user_list:
      with open('user_dict.json','w') as users_file:
        json.dump(user_list, users_file)
        logging.info('[Saved]: user_list saved.')

    else:
      logging.info('Nothing changed since last save. Not saving to disk.')
  except Exception as error:
    logging.warning(f'[ERROR]: Could not save user_list to file. dumping user_list: {user_list}')


if __name__ == '__main__':
  # asyncio.run(addShip('chevalglass', "2", False))
  # asyncio.run(saveUsers())
  pass
