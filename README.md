<h1 align="center">
    ApplicationTracker - Track your job applications with ease!
</h1>

<p align="center">
    <a href="https://github.com/Symplexity/ApplicationTracker/issues/new">Report Bug</a>
    |
    <a href="https://github.com/Symplexity/ApplicationTracker/issues/new">Request Feature</a>
</p>

<h1> Key Features</h1>
<ul>
    <li> Add completed application entries for easy tracking </li>
    <li> Add job listings to a todo list if you arent ready to apply </li>
    <li> Get reminded to send a followup on a per-application basis </li>
    
</ul>

<h1> Getting Started </h1>

<h2> Configuring Environment </h2>

This project uses uv to manage python versions and package dependencies. Instructions for installing
can be found [here](https://docs.astral.sh/uv/).

<h2> Setting up Discord Application </h2>

<h3> Creating the Application </h3>

Instructions can be found [here](https://discord.com/developers/docs/quick-start/getting-started) on how to set up a Discord app.
The relevant bit here is in
[step 1](https://discord.com/developers/docs/quick-start/getting-started#step-1-creating-an-app).

There are two things to make note of while setting up the app

-   Make sure you rename `.env.sample` to `.env`, and replace `<YOUR_TOKEN_HERE>` and
    `<YOUR_CLIENT_ID>` with your bots token and **OAuth2** Client ID
-   In the application setting, under **Bot** and **Privleged Gateway Intents**, enable the option
    for **Message Content Intent**, as some commands may not function as expected without this

<h2> Running the Bot </h2>

If you have not already added the bot to your server, run `uv run bot.py -g` to create an invite
link. Follow this link, and add the bot to the desired server that you have the proper permissions
for.

Once you have set up the bot, run `uv run bot.py` to start the bot, and connect it to Discord.
