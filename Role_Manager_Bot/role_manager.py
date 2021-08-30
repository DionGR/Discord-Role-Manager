# Regular Module Imports
from os import path, sys
# Discord API Imports
import discord
from discord.ext import commands
# Google Docs/Sheets API Imports
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
# Assistance Files Imports
from media import *
from request_data import *

""" Google API Initializations """
SCOPES = link("SCOPE")
CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name(path.join(sys.path[0], "credentials.json"), SCOPES)
CLIENT = gspread.authorize(CREDENTIALS)
SERVICE = build("sheets", "v4", credentials=CREDENTIALS)

""" Discord API Initializations """
BOT = commands.Bot(command_prefix='!')


@BOT.event
async def on_ready():
    print("BOT is ready and running!")


"""
!setuphelp - Admin Only
This command sends an embed with direct instructions on how
to get the Role Manager Bot set up and running on a server.
"""
@BOT.command()
@commands.has_permissions(administrator=True)
async def setuphelp(ctx):
    embed = discord.Embed(title="Role Manager Setup Tutorial", description="Click the link above for detailed instructions with pictures!", url=link("TUTORIAL"),  color=color("GREEN"))
    embed.add_field(name="Step 1:", value="Create a Google Sheets Worksheet.", inline=False)
    embed.add_field(name="Step 2:", value="Click the Share button on the top right and add this e-mail as an author: ```\n" + CREDENTIALS.service_account_email + "```", inline=False)
    embed.add_field(name="Step 3:", value="Select 8 columns and right-click >> Insert 8 Columns in your worksheet.", inline=False)
    embed.add_field(name="Step 4:", value="Run the !configure command and link your server with your Google spreadsheet.\n```!configure <WORKSHEET ID>```", inline=False)
    embed.add_field(name="Step 5:", value="Export the role permissions onto the Google Sheet using:\n``` !export ```", inline=False)
    embed.add_field(name="Finished!", value="The bot is now set up and you can start managing your roles! Make sure you provide a valid Spreadsheet ID, or you will encounter an error!", inline=False)
    embed.set_thumbnail(url=picture("GSHEET"))
    await ctx.send(embed=embed)


"""
!configure - Owner Only
This command creates a file for the server in the database (serverdata) 
and stores the Google Worksheet ID inside a .txt file named after the server's ID.
If a file already exists, it prompts the user to update the file instead of reconfiguring it.
"""
@BOT.command()
@commands.has_permissions(administrator=True)
async def configure(ctx, *, spreadsheet_id=None):
    if len(spreadsheet_id) == 44:  # Ensure input was given and that it is valid.
        if ctx.message.author.id == ctx.guild.owner_id:  # If the sender is the server owner, proceed.
            file_name = str(ctx.guild.id) + ".txt"  # The name of the file is that of the server's unique ID.
            try:  # If the file exists, open and read it and give the link.
                with open(path.join("serverdata", file_name), "r+") as server_file:
                    server_file.truncate(0)
                    server_file.write(spreadsheet_id)

                    embed = discord.Embed(title="You already have a worksheet!", description="Your spreadsheet ID has been updated instead!", color=color("GREEN"))
                    embed.add_field(name="Your worksheet has been linked! Here's the link: ", value=link("SPREADSHEET") + spreadsheet_id)
                    embed.set_thumbnail(url=picture("GSHEET"))
                    await ctx.send(embed=embed)
            except FileNotFoundError:  # If it doesn't, create it and give the complete link.
                with open(path.join("serverdata", file_name), "w+") as server_file:
                    server_file.write(spreadsheet_id)

                embed = discord.Embed(title="Worksheet Configuration Complete!", description="Your server has been added to the database.", color=color("GREEN"))
                embed.add_field(name="Your worksheet has been linked! Here's the link: ", value=link("SPREADSHEET") + spreadsheet_id)
                embed.set_thumbnail(url=picture("GSHEET"))
                await ctx.send(embed=embed)
            except Exception as exception:
                print("Server ID:" + ctx.guild.id + "\n Exception:" + str(exception))
                embed = discord.Embed(title="Something went wrong!", description="Please contact the BOT owner on GitHub!", color=color("RED"))
                embed.add_field(name="Error code: ", value=str(exception))
                embed.set_thumbnail(url=picture("ERROR"))
                await ctx.send(embed=embed)
        else:  # If the sender is a simple Admin, refuse permission with an error embed.
            embed = discord.Embed(title="Access Denied!", description="You have no proper authorization for this command.", color=color("RED"))
            embed.add_field(name="This command may only be used by the server owner! ", value='<@' + str(ctx.guild.owner_id) + '>')
            embed.set_thumbnail(url=picture("ERROR"))
            await ctx.send(embed=embed)
    else:  # If no valid ID was given, ask for a valid ID and show instructions.
        embed = discord.Embed(title="No worksheet ID specified!", description="Please specify a valid worksheet ID.", color=color("RED"))
        embed.add_field(name="If want to see how to setup this bot use the command: ", value="```!setuphelp```", inline=False)
        embed.set_thumbnail(url=picture("ERROR"))
        await ctx.send(embed=embed)

"""
!export - Owner Only
This command exports all the roles and their permissions
from the Discord Server, organizes them and imports them 
to the Google Sheet assigned to that Discord Server.
"""
@BOT.command()
@commands.has_permissions(administrator=True)
async def export(ctx):
    if ctx.message.author.id == ctx.guild.owner_id:
        file_name = str(ctx.guild.id) + ".txt"
        try:
            with open(path.join("serverdata", file_name), "r+") as server_file:
                spreadsheet_id = server_file.read()
                try:
                    role_list = ctx.guild.roles  # Export all the roles from a server. List of role type Objects.
                    role_list.reverse()
                    role_names = [role.name for role in role_list]  # Get all the role names from the role Objects.
                    role_permissions = {role: dict(role.permissions) for role in role_list}  # Put Roles in a dictionary and their permission_values in sub-dictionaries.
                    permission_names = list(role_permissions[role_list[0]].keys())  # Get all the permission names.
                    permission_values = permission_values_to_emojis(list(role_permissions.values()), permission_names)  # Get all of the permissions values and convert them to √ or X.

                    clear_request = SERVICE.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range="A1:AH1000", body=clear_request_body())
                    titles_request = SERVICE.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=titles_request_body(role_names, permission_names))
                    values_request = SERVICE.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=values_request_body(permission_values))
                    clear_request.execute()  # Clears the spreadsheet.
                    titles_request.execute()
                    values_request.execute()  # Handling and execution of the requests to the Google API. See request_data.py for more info.

                    embed = discord.Embed(title="Permission Export Complete!", description="Your server's role permission_values have been successfully exported!", color=color("GREEN"))
                    embed.add_field(name="Here's the link to your worksheet: ", value=link("SPREADSHEET") + spreadsheet_id)
                    embed.set_thumbnail(url=picture("GSHEET"))
                    await ctx.send(embed=embed)
                except Exception as exception:
                    print("Server ID:" + ctx.guild.id + "\n Exception:" + str(exception))
                    embed = discord.Embed(title="Worksheet unavailable!", description="There was an issue trying to access your server's worksheet!", color=color("RED"))
                    embed.add_field(name="Make sure you have followed the !setuphelp steps correctly. If the issue persists, contact the BOT Owner.", value="```!setuphelp```")
                    embed.set_thumbnail(url=picture("ERROR"))
                    await ctx.send(embed=embed)
        except FileNotFoundError:  # If the file does not exist, prompt user to configure.
            embed = discord.Embed(title="No file found!", description="There was an issue trying to import your server's file from the database.", color=color("RED"))
            embed.add_field(name="You have to configure your server first. Please try the command !setuphelp for more information.", value="```!setuphelp```")
            embed.set_thumbnail(url=picture("ERROR"))
            await ctx.send(embed=embed)
    else:  # If the sender is a simple Admin, refuse permission with an error embed.
        embed = discord.Embed(title="Access Denied!", description="You have no proper authorization for this command.", color=color("RED"))
        embed.add_field(name="This command may only be used by the server owner! ", value='<@' + str(ctx.guild.owner_id) + '>')
        embed.set_thumbnail(url=picture("ERROR"))
        await ctx.send(embed=embed)

"""
BOT RUN Command that logs in the bot with our credentials. 
Has to be in the end of the file.
"""
BOT.run('BOT_TOKEN_HERE')
