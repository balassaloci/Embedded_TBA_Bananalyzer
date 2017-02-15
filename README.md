Things to DOOOO 
===============

## Physical Part - David A., David P.
 -  [x] Send data in json format to MQTT
 -  [x] Testing to get color data (What range is the banana ripe or rotten)
 -  [x] Decide which color palette to use + convert to it - YUV, HSL
 -  [x] Analysis on the color (ripe or rotten)
 
### Optional 
 -  [x] Measure on request
 -  [ ] Add temperature sensor
 -  [x] Make the code modular 
 -  [ ] Box or case for the module
 
## Website Backend - Nick
 -  [x] Download and store MQTT data
 -  [x] Serve data in API for website
 
### Optional
 -  [x] Button for forced measurement
 
## Website Frontend - Loci
 -  [x] Display latest measurements on graph
 -  [x] Display the analysed info
 
## Business Website - David P.
 -  [x] Pick a design
 -  [x] Write cool bs text about it
 -  [x] Add a few stock or not stock photos

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
