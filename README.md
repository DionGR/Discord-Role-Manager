# Discord Role Manager Bot

Role Manager is a discord BOT that utilizes Google Sheets for the organization of a server's hierarchy and permissions.


## Details

This BOT allows for you to export and organize your roles in a Google Sheet in a very user friendly way.

Three requests are made per usage of !export. One for clearing the spreadsheet, one for updating the roles/permission titles and one for the permission values themselves, making it extremely light and difficult for it to hit the Google Docs quota limit.
## Installation - Add the BOT to your server

Paste this on your browser to invite the BOT to a server you manage. The BOT requires the Administrator permission.

```bash
https://discord.com/api/oauth2/authorize?client_id=823014411945377824&permissions=8&scope=bot
```

## Usage - BOT Commands

```python
!setuphelp # Instructions on how to set up the BOT for your server.

!configure # Add your server to the BOT's database, along with your Google Sheet.

!export # Export your server's roles and their permissions to your Google Sheet.
```

## Requirements (for Developers)

```python
# Regular Module Imports
from os import path, sys
# Discord API Imports
import discord
from discord.ext import commands
# Google Docs/Sheets API Imports
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
