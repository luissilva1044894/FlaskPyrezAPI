<div  align="center">
<a href="https://github.com/luissilva1044894/FlaskPyrezAPI" title="FlaskPyrezAPI - Github repository" alt="FlaskPyrezAPI · Github repository"><img src="./static/img/pyrez.png" height="96" width="96"></a>

## FlaskPyrezAPI
[![License](https://img.shields.io/github/license/luissilva1044894/FlaskPyrezAPI.svg?logo=github&logoColor=white&logoWidth=10style=plastic)](./LICENSE "FlaskPyrezAPI · LICENSE")
[![Runtime Version](https://img.shields.io/pypi/pyversions/flask.svg?style=plastic&logo=python&logoColor=white&logoWidth=10)](https://pypi.org/project/pyrez "Python Runtime Versions")
[![Discord Server](https://img.shields.io/discord/549020573846470659.svg?logo=discord&logoColor=white&logoWidth=10&style=plastic)](https://discord.gg/XkydRPS "Support Server · Discord")


Built with: [![Python](https://img.shields.io/badge/Python-3.7.4-blue.svg?style=plastic&logo=python&logoWidth=15&logoColor=white)](https://docs.python.org/3.7/whatsnew/changelog.html#python-3-7-4-final "Python 3.7.4")
[![Pyrez](https://img.shields.io/badge/Pyrez-1.1.0.1-00bb88.svg?logo=github&logoColor=white&style=plastic)](https://github.com/luissilva1044894/Pyrez/tree/1.1.x "Pyrez · 1.1.0.1")
[![Flask](https://img.shields.io/badge/Flask-1.1.1-orange.svg?logo=flask&logoColor=white&style=plastic)](https://pypi.org/project/Flask/1.1.1/ "Flask · 1.1.1")
[![Bootstrap 4](https://img.shields.io/badge/Bootstrap-4.3.1-orange.svg?logo=bootstrap&logoColor=white&style=plastic)](https://getbootstrap.com/docs/4.3/getting-started/introduction/ "Bootstrap · 4.3.1")
[![Font Awesome](https://img.shields.io/badge/Font_Awesome-5.11.1-orange.svg?style=plastic)](https://github.com/FortAwesome/Font-Awesome/blob/master/CHANGELOG.md#5111---2019-09-18 "Font Awesome · 5.11.1")

</div>

FlaskPyrezAPI is an endpoint for custom commands ([`Twitch`](https://twitch.tv "Twitch")), that provides data about players, matches and others stats of the game [`Paladins`](https://paladins.com "Paladins Game"). It uses [Pyrez](https://github.com/luissilva1044894/Pyrez "Pyrez · Github repository"), my Python wrapper for Hi-Rez Studios API.

[Demo ![Website](https://img.shields.io/website/https/nonsocial.herokuapp.com.svg?logo=heroku&logoColor=white&)](https://nonsocial.herokuapp.com/)

### Key Features
 * English, Polish, Portuguese and Spanish language support.

### Requirements
- [Access](https://pyrez.readthedocs.io/en/stable/gettingstarted.html#registration "Form access to Hi-Rez Studios API") to Hi-Rez Studios API.

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
6. Edit [`.env`](./.env) and replace the `PYREZ_AUTH_ID` and `PYREZ_DEV_ID` with the `authId` and `devId` that you receive from [`Hi-Rez Studios`](https://luissilva1044894.github.io/Pyrez/docs#registration "Form access to Hi-Rez Studios API").
7. Run server: `python manage.py runserver`
8. Go to your browser and point it towards `http://127.0.0.1:5000`

#### Deploy (Heroku) [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/luissilva1044894/FlaskPyrezAPI/tree/master "Deploy to Heroku")
1. Go to [Heroku](https://id.heroku.com/login) and create a new app (eg: `your-app-name`)
2. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli "Heroku CLI")
3. `heroku login`
4. `git init`
5. `heroku git:remote -a your-app-name`
6. Download this repo and copy all files into `your-app-name` folder
7. Edit [`.env`](./.env) and replace the `PYREZ_AUTH_ID` and `PYREZ_DEV_ID` with the `authId` and `devId` that you receive from [`Hi-Rez Studios`](https://luissilva1044894.github.io/Pyrez/docs#registration "Form access to Hi-Rez Studios API").
8. `heroku config:push`
9. `git add .`
10. `git commit -m "Going to Heroku"`
11. `git push heroku master`
12. `heroku run python manage.py db migrate`
13. `heroku open` and a window will open with your app online

### Thanks
* [`Lukash (Paladins Poland)`](https://www.facebook.com/PaladinsPoland/ "Paladins Poland") - Polish translation.

### License 📝
This is an open source [![Open Source](https://raw.githubusercontent.com/abhishekbanthia/Public-APIs/master/opensource.png)](https://www.opensource.org "See http://www.opensource.org for the Open Source Definition") project provided under the MIT License, which you can view in [`LICENSE file`](./LICENSE "FlaskPyrezAPI · License").

> Raw data provided by Hi-Rez Studios API and is thus their property. © 2019 Hi-Rez Studios, Inc. All rights reserved.
