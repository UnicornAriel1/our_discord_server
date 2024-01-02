# our_discord_server
A place to work with my friend group's discord server

## Bot Functionality

### Event Management

- When a scheduled event is created the bot creates a new private channel named after the event and adds the event creator to it. 
- When a user clicks "interested" on a scheduled event they are added to the existing channel for the event. 
- Introduces bot command `?get_guild_events` which lists all scheduled events for the coming week. 

#TODO: 
- Add arguments for start date and number of days to list to `$get_guild_events`.
- Add functionality to delete channels after event occurs
- Add user facing read-me for events


