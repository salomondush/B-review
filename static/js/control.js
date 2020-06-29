

document.addEventListener('DOMContentLoaded', () => {
    //call the display channels function
    if (localStorage.getItem('channel') !== 'null') {
        select_channel(localStorage.getItem('channel'));
    } else {
        display_channels();
    }
    
    //CONST FUNCTIONS
    const messages_template = Handlebars.compile(document.querySelector("#messages").innerHTML);
    const messages = data =>{ //data will need to be a dictionary
        const channel = localStorage.getItem('channel');
        if (channel == data.channel) {
            const charts = messages_template({'channel': channel, 'messages': data.messages, 'admin': data.admin});

            document.querySelector('main').innerHTML = charts;
        }
    }
    
    const all_users = Handlebars.compile(document.querySelector('#channel-users').innerHTML);
    const get_messages = data =>{
        if (localStorage.getItem('channel') == data.channel){

            //get all user messages
            const all_charts = messages_template({'channel': data.channel, 'messages': data.charts, 'admin': data.admin})
            document.querySelector('main').innerHTML = all_charts;

            //get all users in the channel
            const all_channel_users = all_users({'users': data.users});
            document.querySelector('.users').innerHTML = all_channel_users;

            //direct messages users
            const ul = document.querySelector("#direct-users");
            ul.innerHTML = '';
            var direct = data.direct;
            direct.forEach(user => {
                let li = document.createElement('li');
                li.className = 'list-group-item 2'
                li.innerHTML = user;
                ul.appendChild(li);
            });

            //add an event listener for a click to display channels
            document.addEventListener('click', event => {
                const element = event.target;
                //THE 'IF' BLOCK IS NOT WORKING
                if (localStorage.getItem('channel') !== 'null'){
                    if (element.id == 'select-users'){
                        document.querySelector('.users').style.display = 'block';
                        document.querySelector('#message').style.marginRight = '230px';
                    } else if (element.id == 'hide') {
                        document.querySelector('.users').style.display = 'none';
                        document.querySelector('#message').style.marginRight = '0px';
                    }
                }
            });

        }
    }

    //template for displaying channels
    const channels_template = Handlebars.compile(document.querySelector("#channels").innerHTML);
    const non_channel_template = Handlebars.compile(document.querySelector('#channels-0').innerHTML);
    const channels = data =>{
        //clear the nav's particular channel specs
        document.querySelector('#current-channel').innerHTML = '';
        document.querySelector('#users-number').innerHTML = '';

        //1st display non-channels
        const your_channels = channels_template({"channels": data[0]});
        document.querySelector('main').innerHTML = your_channels;
       
       //2nd display non-channels
       const other_channels = non_channel_template({"non_channels": data[1]})
       document.querySelector('#add-channels').innerHTML += other_channels;

       //3rd display direct messaging of users
       const ul = document.querySelector("#direct-users");
       ul.innerHTML = '';
       data[2].forEach(user => {
           let li = document.createElement('li');
           li.className = 'list-group-item 2'
           li.innerHTML = user;
           ul.appendChild(li);
       });
    }

    const direct_user = Handlebars.compile(document.querySelector('#private_messages').innerHTML);
    const get_user_messages = data =>{
        let user = localStorage.getItem('name')
        //display the messages
        const private_chats = direct_user({'messages': data.messages, 'user': user});
        document.querySelector('main').innerHTML = private_chats;
    }

    //scrolling in messages 
    function scroll(name){
        name.scrollTop = name.scrollHeight - name.clientHeight;
    }

    //DISPLAY CHANNELS AND DIRECT MESSAGING USERS
    function display_channels(){
        //clear the local storage current channel
        localStorage.setItem('channel', null);
        localStorage.setItem('id', null);
        //clear the current channel's list of users
        document.querySelector('.users').innerHTML = '';
        //get channels from the server
        const request = new XMLHttpRequest();
        request.open('GET', '/channels');
        request.onload = ()=>{
            const data = JSON.parse(request.responseText);
            if (data.length === 0) {
                var empty = false;
                channels(empty);
            } else {
                channels(data);
            }
        };
        data = new FormData;
        request.send(data)
    }


    //select channels function
    function select_channel(name){
        //clear private messages chats id
        localStorage.setItem('id', null);
        //make request to the server
        const request = new XMLHttpRequest();
        request.open('POST', '/charts');
        request.onload = () =>{
            const data = JSON.parse(request.responseText);
            //store in the local storage
            localStorage.setItem('channel', data.channel);
            //update the nav about channel aspects
            var channel_users = data.users;
            document.querySelector('#current-channel').innerHTML = data.channel;
            document.querySelector('#users-number').innerHTML = channel_users.length;

            //now get the messages of the channel
            get_messages(data);

        }
        const data = new FormData();
        data.append('channel', name);
        request.send(data);
    }

    //user private messaging display function
    function user_chats(name){
        //clear any current channel from the local storage
        localStorage.setItem('channel', null);
        const request = new XMLHttpRequest();
        request.open('POST', '/direct');
        request.onload = () => {
            const data = JSON.parse(request.responseText);
            //now, we crate a unique indentifier for every private chat,
            //which is the length of the two names of the chatting people
            let all_names = data.current + data.other;
            localStorage.setItem('id', all_names.length);
            localStorage.setItem('name', name);
            //clear nav about any channel aspects
            document.querySelector('#current-channel').innerHTML = '';
            document.querySelector('#users-number').innerHTML = '';

            //now get messages btn the two users
            get_user_messages(data);
        }
        const data = new FormData();
        data.append('name', name);
        request.send(data);
    }

    //function to get time
    function get_time(){
        const today = new Date()
        let time = today.getHours() + ":" + today.getMinutes();
        return time;
    }

    //CLICKS
    document.addEventListener('click', event =>{
        const element = event.target;
        if (element.className == 'list-group-item'){
            let channel = element.innerText;
            let channel_name = channel.slice(0, channel.lastIndexOf(' '));

            //select the channel
            select_channel(channel_name);

        }else if (element.id == 'join-channel'){
            let area = element.parentElement;
            let inner_text = area.parentElement.innerText;
            let channel_name = inner_text.slice(0, inner_text.lastIndexOf('.'));

            //select the channel
            select_channel(channel_name);
        } else if (element.className == 'list-group-item 2'){
            let name = element.innerText;

            //select user's private chats
            user_chats(name);
        }
    });

    document.addEventListener('submit', e =>{
        e.preventDefault();
        const form = event.target;
        if (form.className == 'form-group 1') {
            const name = document.querySelector('#channel-name').value;
            if (!name) {
                return; 
            }
            const request = new XMLHttpRequest();
            request.open('POST', '/channel');
            request.onload = () =>{
                const data = JSON.parse(request.responseText);
                //store in local storage
                localStorage.setItem('channel', data.channel);
                if (data.success == 'yes') {
                    return messages(data);
                }else{
                    document.querySelector('#error1').innerHTML = 'Channel already exists!';
                }
            };
            const data = new FormData();
            data.append('channel', name);
            request.send(data);
        }
    });

    //WEB SOCKETS
    var socket = io.connect(location.protocol + "//" + document.domain + ":" + location.port);

    socket.on('connect', () => {

        //FORMS SUBMITTED
        document.addEventListener('submit', event => {
            event.preventDefault();
            const form = event.target;
            if (form.className == 'form-group 2'){

                let message = document.querySelector('#text').value;
                if(!message){
                    return;
                }
                
                let time = get_time();
                let channelName = localStorage.getItem('channel');

                //emit the message to the server
                socket.emit('send message', {'message': message, 'time': time, 'channel': channelName});

                //clear the input field
                document.querySelector('#text').value = '';
            }else if (form.className == 'form-group 3'){
                let message = document.querySelector('#text-1').value;
                if (!message){
                    return;
                }
                let user_name = localStorage.getItem('name');
                let time = get_time();

                //emit private message to the server
                socket.emit('private message', {'message': message, 'time': time, 'user': user_name});
                document.querySelector('#text-1').value = '';
            }
        });
    });
 
    
    //when the server broacasts new messages
    const post_template = Handlebars.compile(document.querySelector("#message0").innerHTML);
    socket.on('receive message', data => {
        if (localStorage.getItem('channel') == data[0]){
            
            const post = post_template({"message": data})
            document.querySelector('.texts-list').innerHTML += post;

            //scroll
            const listings = document.querySelector('.texts-list');
            scroll(listings);
        }
    });

    const private_message_template = Handlebars.compile(document.querySelector('#message0').innerHTML);
    socket.on('new private_message', data => {
        let all_names = data[0] + data[1];
        if (localStorage.getItem('id') == all_names.length){

            const private_post = private_message_template({'message': data});
            document.querySelector('.texts-list').innerHTML += private_post;
        }
    });


    //NAV LINKS CONFIGURATION
    const channels_list = document.querySelector("#get-channels");
    channels_list.onclick = () => {
        display_channels();
    };
});