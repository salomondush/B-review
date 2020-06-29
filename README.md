# Project 2

Web Programming with Python and JavaScript

Flack

    This is a messaging web app application. At first, users can get in using only their display names. New users are required to create a display name inorder to join channels or groups. An added feature is that users can message others privately, but only when they share the same group or channel.

TEMPLATES (pages)

    - hello.html: This is the landing page for all users when not logged in. There are two fields for users already with display names and new ones respectively. Users are warned if they are trying to create dispaly names that already exists or if they try to login with a non valid display name.

    - layout.html: After the user gets in using a display name, this is the next page. First, the page displays all available channels showing those that a user is included in, and other ones that the user can join. On every channel, there's a badge showing the number of users in it. Moreover, a user is welcome to create a new channel by which he/she is redirected to the new channel empty chats to start chating. 
    
    When users join a new channel or select an existing one, they are taken to the channel's messages. The side navigation bar shows the active channel, and the number of users in it, which if clicked opens a side bar showing the names of those users. In addition, if there are any messages, they are all loaded up to 100 only.

    Now, a user can send and recieve messages without reloading the page. When sending a message, it posted showing the display name of the user, time, and the actual message. 

PERSONAL TOUCH (private messaging)

    - The user is able to privately chat with those sharing the same groups by clicking on any user on the list under the DIRECT MESSAGING part of the side navigation.

PYTHON FILES:

    -application.py: It contains all the python code that works on the server side to store and send data that allows for all of the above to work. 
    
    Four global datastructures are used to store all data. First is the messages dictionary which stores channels as keys and channel's messages as list of lists values. Second is the channels dicionary which stores all channel and user related data. Channels are keys and values are lists of users respective. The third data sctructure, users dictionary, stores all users with user number as keys and names as values. The fourth data stracture, direct dictionary, is responsible for all direct messaging; keys are certain users and values are also dictionaries storing private charts btn two users.

    -functions.py: it contains a function to prevents users from any form fo chatting without a display name.

JAVASCRIPT FILES:

    - control.js: This javascript is responsible for client-side operations. AJAX is used to comunicate with the server, and web sockets are used to display real-time messages. Futhermore, local storage is used to store data like current channel, current private chat id, and current user. Also, all buttons and clicks are configured through this javascript file. It's a little bit messy, but it works. 

    Using local storage, a user can close the browser when on a particular channel, and when he comes back, he gets directed to the channel that he/she left off. However, this does not work for private chats, only for channels.

All css files are used for design purposes. The requirements.txt contains cs50's required modules to run this project.