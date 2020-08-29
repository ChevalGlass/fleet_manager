#!/usr/bin/python3

# Fleet Manager Web Front-end Generator

import asyncio
import json
import logging
import fleet_manager as fm # My api that handles the storage/retrieval of the data.


# A count down timer in javascript used for the redirect pages.
redirect = '''
  <label id="countdown"></label>
  <script type="text/javascript">
    var seconds = 3;

    function countDown() {
      seconds = seconds - 1;
      if (seconds < 0) {
        // Redirect to next page.
        window.location = "/wos/"
      } else {
        // Update remaining seconds.
        document.getElementById("countdown").innerHTML = seconds;

        // recursively call this in another second.
        window.setTimeout("countDown()", 1000);
      }
    }

    // Start the countdown.
    countDown();
  </script>'''


# Return an html dropdownlist with all the ships and their internal IDs.
async def ship_ddl():
  select = '<select id="ships" name="ship"><option value="-1" selected disabled>--Select Ship--</option>{}\t</select>'
  option = '\t\t<option value="{value}">{name}</option>\n'
  options = ''

  ships = await fm.ships()

  for ship in ships:
    options += option.format(value=ship["id"],name=ship["name"])#ship["manufacturer"]+ ' | '+ship["name"])

  return select.format(options)


# Return a "combobox" for users with a datalist of all the current users in the system.
async def user_combo():

  option = '\t\t<option value="{name}">{name}</option>\n'
  options = ''

  usersCombobox = '''
    <input list="users" id="ign" name="user">
    <datalist id="users">
      {}
    </datalist>'''

  for user in await fm.users():
    options += option.format(name=user.get('name'))

  return usersCombobox.format(options)


# Return the Form used to make Add/Remove requests.
# This generates the combobox and dropdownlist for each request.
# At some point the ship dropdownlist should be cached to save performance.
#   (Since it does not change regularly.)
async def userForm():
    return f'''
    <form>
      <label for="ign">Username </label>{await user_combo()}
      <label for="ship"> Ship </label>{await ship_ddl()}
      <input type="checkbox" id="pledge" name="pledge"><label for="pledge">Pledge</label>
      <input type="submit" value="Add" formaction="/wos/add">
      <input type="submit" value="Remove" formaction="/wos/remove">
    </form>
    '''


# Returns all the html for the body of the page.
# It includes the Form and generates the table of all the ships and users.
async def table():
  # List each user and the ships they own.
  user_list = await fm.users()
  ship_list = await fm.ships()

  # String templates for generating the table.
  table = '<br><div style="overflow-x:auto;"><table>{}</table></div>'
  tablebody = ''
  row = '<tr>{}</tr>'
  col = '<td>{}</td>'
  head = '<th>{}</th>'
  header = '<th>Ship</th>'

  # Users header formated "Username (#pledged,#aUEC)"
  for user in user_list:
    pledgedCount = 0
    aUECCount = 0

    for pledged in user.get("ships_pledge").keys():
      pledgedCount += user.get("ships_pledge").get(pledged)

    for aUEC in user.get("ships_aUEC").keys():
      aUECCount += user.get("ships_aUEC").get(aUEC)

    header += head.format(user.get("name",'')+f'({str(pledgedCount)},{str(aUECCount)})')

  # Main body of the table.
  # Loop through all the ships and check if any users have one listed.
  #   Future improvement: Only display ships which users have.
  for ship in ship_list:
    tableRow = col.format(ship.get("name"))

    shipCountPledge = 0
    shipCountaUEC = 0

    for user in user_list:
      pledgedCount2 = 0
      aUECCount2 = 0

      if user.get("ships_pledge").get(ship.get("id")) != None:
        pledgedCount2 += user.get("ships_pledge").get(ship.get("id"))

      if user.get("ships_aUEC").get(ship.get("id")) != None:
        aUECCount2 += user.get("ships_aUEC").get(ship.get("id"))

      tableRow += col.format(str(pledgedCount2)+', '+str(aUECCount2))

    tablebody += row.format(tableRow)

  return await userForm() + table.format(header+tablebody)


# This calls the back-end Add ship function and gives the user feedback with a redirect.
async def add(ign, ship, pledge):
  if await fm.addShip(ign, ship, pledge):
    return f'<p>Added Successfully. Redirecting in {redirect}</p>'
  else:
    return f'<p>Add failed. Redirecting in {redirect}</p>'


# This calls the back-end Remove ship function and gives the user feedback with a redirect.
async def remove(ign, ship, pledge):
  if await fm.removeShip(ign, ship, pledge):
    return f'<p>Removed Successfully. Redirecting in {redirect}</p>'
  else:
    return f'<p>Remove failed. Redirecting in {redirect}</p>'


# This runs the back-end to save function.
# If database support is added, this will be removed.
async def save():
  return await fm.saveUsers()


if __name__ == '__main__':
  # This is a library.
  # The following is just for testing.

  # Print out the body of the page for the table.
  print(
    asyncio.run(table())
  )
