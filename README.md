
<div  align="center">
<a href="https://github.com/luissilva1044894/FlaskPyrezAPI" title="FlaskPyrezAPI - Github repository" alt="FlaskPyrezAPI · Github repository"><img src="./data/static/img/pyrez.png" height="96" width="96"></a>

## FlaskPyrezAPI

> If you are currently using this project, please ⭐️ this [repository][github-repo]!

[![License](https://img.shields.io/github/license/luissilva1044894/FlaskPyrezAPI.svg?logo=github&logoColor=white&logoWidth=10style=plastic)](./LICENSE "FlaskPyrezAPI · LICENSE")
[![Runtime Version](https://img.shields.io/pypi/pyversions/flask.svg?style=plastic&logo=python&logoColor=white&logoWidth=10)](https://pypi.org/project/pyrez "Python Runtime Versions")
[![Discord Server](https://img.shields.io/discord/549020573846470659.svg?logo=discord&logoColor=white&logoWidth=10&style=plastic)](https://discord.gg/XkydRPS "Support Server · Discord")

Built with:  [![Python](https://img.shields.io/badge/Python-3.7.6-blue.svg?style=plastic&logo=python&logoWidth=15&logoColor=white)](https://docs.python.org/3.7/whatsnew/changelog.html#python-3-7-6-final "Python 3.7.6")

[![Pyrez](https://img.shields.io/badge/Pyrez-1.1.0.1-00bb88.svg?logo=github&logoColor=white&style=plastic)](https://github.com/luissilva1044894/Pyrez/tree/1.1.x "Pyrez · 1.1.0.1")
[![discord.py][badge-discord-py]][discord-py]
[![Flask](https://img.shields.io/badge/Flask-1.1.1-orange.svg?logo=flask&logoColor=white&style=plastic)](https://pypi.org/project/Flask/1.1.1/ "Flask · 1.1.1")

[![Bootstrap 4](https://img.shields.io/badge/Bootstrap-4.4.1-orange.svg?logo=bootstrap&logoColor=white&style=plastic)](https://getbootstrap.com/docs/4.4/getting-started/introduction/ "Bootstrap · 4.4.1")
[![Font Awesome](https://img.shields.io/badge/Font_Awesome-5.12.0-orange.svg?style=plastic)](https://github.com/FortAwesome/Font-Awesome/blob/master/CHANGELOG.md#5120---2019-12-10 "Font Awesome · 5.12.0")
[![Pillow][badge-pillow]][pillow]

[![Become a Patron!][bagde-patreon]](https://www.patreon.com/bePatron?u=14686910 "Become a Patron!")
<a href="https://www.buymeacoff.ee/Nonsocial" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

> :construction: **DON'T USE THE MASTER VERSION, USE [`2.6.2`](https://github.com/luissilva1044894/FlaskPyrezAPI/tree/v2.6.2) INSTEAD!**

</div>

FlaskPyrezAPI is an endpoint for custom commands ([`Twitch`](https://twitch.tv "Twitch")), that provides data about players, matches and others stats of the game [`Paladins`](https://paladins.com "Paladins Game"). It uses [Pyrez](https://github.com/luissilva1044894/Pyrez "Pyrez · Github repository"), my Python wrapper for Hi-Rez Studios API.

[Demo ![Website](https://img.shields.io/website/https/nonsocial.herokuapp.com.svg?logo=heroku&logoColor=white&)](https://nonsocial.herokuapp.com/)

### Key Features
 * English, Polish, Portuguese and Spanish language support.

### Requirements
- [Access](https://pyrez.readthedocs.io/en/stable/gettingstarted.html#registration "Form access to Hi-Rez Studios API") to Hi-Rez Studios API.
- [Bot Token - Discord](https://discordapp.com/developers/applications/me) - In order to run the bot, you'll have to provide your own token, provided by Discord. See [here](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token) for a tutorial on creating a Discord bot account.

### Support
For support using Pyrez, please join the official [*support server*](
https://discord.gg/XkydRPS "Support Server · Discord") on [Discord](https://discordapp.com/ "Discord App").

### Installation
#### Locally
1. Clone this repository: `git clone https://github.com/luissilva1044894/FlaskPyrezAPI.git`
2. ``cd`` into it: `cd FlaskPyrezAPI`
3. Create a virtualenv: `virtualenv -p python venv`
4. Activate it.
5. Install Python Dependencies: `pip install --upgrade pip setuptools wheel` | `pip install -r requirements.txt`
6. Edit [`.env`](./.env.example) and replace the `PYREZ_AUTH_ID` and `PYREZ_DEV_ID` with the `authId` and `devId` that you receive from [`Hi-Rez Studios`](https://luissilva1044894.github.io/Pyrez/docs#registration "Form access to Hi-Rez Studios API").
7. Run: ` python manage.py db migrate`
8. Run server: `python main.py runserver`
9. Go to your browser and point it towards `http://127.0.0.1:5000`

#### Deploy (Heroku) [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/luissilva1044894/FlaskPyrezAPI/tree/master "Deploy to Heroku")

> [Heroku](https://heroku.com/) is a container based cloud platform that offers free plans to host web applications.

1. First, create a [Heroku account](https://id.heroku.com/login) if it isn't already done.
2. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli "Heroku CLI").
3. Sign in using `heroku login`.
4. Create an app using `heroku create your-app-name` if needed.
  - You may add the flag `--region eu` if you want to use their European servers instead of the US ones.
  - If your-app-name is not already taken, Heroku should now create your app.
5. Create a database using `heroku addons:create heroku-postgresql`
  - You should now have access to an empty [Postgres database](https://elements.heroku.com/addons/heroku-postgresql) whose address was automatically saved as an environment variable named `DATABASE_URL`.
  - The app will automatically connect to it when deployed.
<!--
6. Now, generate a secret key and save it to an ENV variable named SECRET_KEY using `heroku config:set SECRET_KEY=ruby -rsecurerandom -e "puts SecureRandom.hex(64)"`
-->
6. `git init`
7. `heroku git:remote -a your-app-name`
8. Download this repo and copy all files into `your-app-name` folder
9. Edit [`.env`](./.env.example) and replace the `PYREZ_AUTH_ID` and `PYREZ_DEV_ID` with the `auth_key` and `dev_id` that you receive from [`Hi-Rez Studios`](https://pyrez.readthedocs.io/en/stable/getting_started.html#registration "Form access to Hi-Rez Studios API").
10. `heroku config:push` - [Config addon](https://github.com/xavdid/heroku-config) is needed
11. `git add .`
12. `git commit -m "Going to Heroku"`
13. You can now push your app using `git push heroku master`
14. `heroku run python manage.py db migrate`
15. Your app should now be ready to use. You can open it with `heroku open`
  - You also can run the console on heroku using `heroku console --app your-app-name`

### Thanks
* [`Lukash (Paladins Poland)`](https://www.facebook.com/PaladinsPoland/ "Paladins Poland") - Polish translation.

### License 📝
This is an open source [![Open Source](https://raw.githubusercontent.com/abhishekbanthia/Public-APIs/master/opensource.png)](https://www.opensource.org "See http://www.opensource.org for the Open Source Definition") project provided under the MIT License, which you can view in [`LICENSE file`](./LICENSE "FlaskPyrezAPI · License").

> Raw data provided by Hi-Rez Studios API and is thus their property. © 2019 Hi-Rez Studios, Inc. All rights reserved.

[badge-discord-py]: https://img.shields.io/badge/discord.py-1.2.5-orange.svg?logo=discord&logoColor=white&style=plastic
[badge-pillow]: https://img.shields.io/badge/Pillow-7.0.0-orange.svg?logoColor=white&style=plastic

[discord-py]: https://discordpy.readthedocs.io/en/v1.2.5/ "Discord.py 1.2.5"
[pillow]: https://pillow.readthedocs.io/en/stable/releasenotes/7.0.0.html "Pillow 7.0.0"

[bagde-patreon]: https://img.shields.io/endpoint.svg?url=https%3A%2F%2Fshieldsio-patreon.herokuapp.com%2Fnonsocial&logoColor=white&style=plastic
[github-repo]: https://github.com/luissilva1044894/FlaskPyrezAPI
