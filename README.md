# FlaskPyrezAPI
[![License](https://img.shields.io/github/license/luissilva1044894/FlaskPyrezAPI.svg?style=plastic&logoWidth=10)](./LICENSE "FlaskPyrezAPI LICENSE")
[![Runtime Version](https://img.shields.io/pypi/pyversions/pyrez.svg?style=plastic&logo=python&logoWidth=10)](https://pypi.org/project/pyrez "Python Runtime Versions")
[![Discord Server](https://img.shields.io/discord/549020573846470659.svg?style=plastic&logo=discord&logoWidth=10)](https://discord.gg/XkydRPS "Support Server on Discord")

**FlaskPyrezAPI** is an open-source endpoint for [`Twitch`](https://twitch.tv "Twitch") commands, written in Python, that provides datas about players, matches and others stats of the game [`Paladins`](https://paladins.com "Paladins Game"). This API uses [`Pyrez`](https://github.com/luissilva1044894/Pyrez "Pyrez Repo") for handling connections and requests to [`Hi-Rez Studios'`](https://www.hirezstudios.com) API.

### Support
For support using Pyrez, please join the official [*support server*](
https://discord.gg/XkydRPS "Support Server on Discord") on [Discord](https://discordapp.com/ "Discord App")

## Requirements
* [Python](http://python.org "Python.org") 3.x(3.5 or higher).
    * The following libraries are required: [`Pyrez`](https://github.com/luissilva1044894/Pyrez "Pyrez repo"), [`Requests`](https://pypi.org/project/requests "requests") and `requests-aeaweb`.
- [Access](https://fs12.formsite.com/HiRez/form48/secure_index.html "Form access to Hi-Rez API") to Hi-Rez Studios' API.

## Installation
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/luissilva1044894/FlaskPyrezAPI/tree/master)

### Deploy (Heroku)
1. Go to [Heroku](https://id.heroku.com/login) and create a new app (eg: `your-app-name`)
2. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
3. `heroku login`
4. `git init`
5. `heroku git:remote -a your-app-name`
6. Download this repo and copy all files into `your-app-name` folder
7. Edit [`.env`](./.env) and replace the `PYREZ_AUTH_ID` and `PYREZ_DEV_ID` with the `authId` and `devId` that you receive from [`Hi-Rez Studios`](https://fs12.formsite.com/HiRez/form48/secure_index.html).
8. `heroku config:push`
9. `git add .`
10. `git commit -m "Going to Heroku"`
11. `git push heroku master`
12. `heroku open` and a window will open with your app online

### Thanks
* [`Lukash`](https://www.facebook.com/PaladinsPoland/ "Paladins Poland") - Polish translation.

### License
This project is provided under the MIT License, which you can view in [`LICENSE.md`](./LICENSE "FlaskPyrezAPI License")
