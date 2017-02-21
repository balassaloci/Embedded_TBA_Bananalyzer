Embedded Systems 2017 TBA - Bananalyzer
=======================================

An IOT device that lets you know whether your banana has gone bad from anywhere in the world.

# Git cheatseet
How to push and pull code form /to github

```
git pull
git add --all
git commit -m "message about the changes made in this commit"
git push
```

If there's a conflict with your code, you might want to use 
```
git stash
```
to stash away your changes and overwrite them.

## Generating an SSH key:
If you don't want to type in your github password every time you push or pull, you can use an ssh-key

#### Step 1
Check if you already have an ssh key which is located in `~/.ssh/id_rsa.pub`
Only proceed, if you do not have a file under that name

#### Step 2
Generate a new ssh-key
```
ssh-keygen -t rsa -C "your_github@email.com"
```
Press enter a few times, no need to type in anything.

Find the file `~/.ssh/id_rsa.pub` and copy its contents.

#### Step 3
Go to GitHub and under your profile settings find the SSH Keys tab.
Add a new key and paste the contents of the previously generated file.

#### Step 4
Delete the old Git repo from your laptop.
Go to the GitHub repo online, click Clone or Download and select Use SSH before copying the link.
Use `git clone LINK` to clone the repository again.

#### Step 5
GitHub shouln't ask for any username or password anymore
