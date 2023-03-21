# GreenTCG
Discord bot for playing GTCG The Game™!

# Installing Python packages

Before you start installing packages, it's a really good idea to create a virtual environment first. This is especially true since this project is using a newer version of discord.py, and so chances are if you want to use discord.py for any other project you'll probably be using a different version. 

Having a virtual environment lets you use different versions of different packages install for different projects, and will make installing all the required packages much easier. We're going to make a virtual environment called `.venv`, since this name is already in the `.gitignore` file (if you know what you're doing you can name your venv something else, but be sure to ignore it in your git!):

```shell
GreenTCG> python -m venv .venv
```

Now we need to *activate* the virtual enviroment. What this basically does is tells python not to use the packages you've installed on your machine, but to use the packages you've installed locally inside your virtual environment. How you do this depends on what OS and shell you're running:

**Windows**
```shell
GreenTCG> .venv\Scripts\activate
```
**Unix, bash shell**
```shell
GreenTCG$ . .venv/bin/activate
```
**Unix, csh shell**
```shell
GreenTCG$ .venv/bin/activate.csh
```
**Unix, fish shell**
```shell
GreenTCG$ .venv/bin/activate.fish
```

Next we need to install all of the required packages in our virtual environment. You could do this manually, but luckily python has a way to do this automatically for us after we give it a list of required modules:

```shell
GreenTCG> pip install -r requirements.txt
```

This should install all the modules needed. If you add another required module to the project, be sure to update `requirements.txt`!

Keep in mind that any time you want to run the code you'll need to reactivate the venv again.

# Setting up the environment

There's an example `.env` in the repo, fill in all the correct values and you should be good to go.