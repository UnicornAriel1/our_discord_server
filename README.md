# our_discord_server
A place to work with my friend group's discord server

## Bot Functionality

### Event Management

- When a scheduled event is created the bot creates a new private channel named after the event and adds the event creator to it. 
- When a user clicks "interested" on a scheduled event they are added to the existing channel for the event. 
- Upcoming events for the week are posted in a specified channel at a specified day and time.
- Channels for events with an end date before the current date are deleted once a day.

### Setup

## Deployment

- Deployed to DigitalOcean App Platform with one worker node and an attached Postgres database
- Two instances running based on `staging` and `production` branches
- Deployed automatically on push to either of the environment branches using GHA to build Docker image and push to DigitalOcean Container Registry with autodeployment to App Platform
- Using OnePassword developer tools to fetch secrets at runtime using a vault and service user per environment

## Database

- Requires user with `CREATE` permission on `discord-events` database. Bot runs schema migration on setup. 