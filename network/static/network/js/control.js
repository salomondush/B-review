document.addEventListener('DOMContentLoaded', () => {

    //ADDING A NEW POST
    const new_post = Handlebars.compile(document.querySelector('#new-post-temp').innerHTML);
    const add_post = (data) => {
        const post = new_post(data);
        const new_div = document.createElement('div')
        new_div.id = `p${data.id}`;
        new_div.className = 'post border'
        //append the handlebars temp to the new div
        new_div.innerHTML = post;
        document.querySelector(".posts").prepend(new_div)
    }

    //SUBMITTING FORMS FOR EDIT AND NEW POST
    document.addEventListener('submit', (e) => {
        const form = event.target;
        if (form.id == "new-post") {
            
            e.preventDefault()
            var content = document.querySelector('#textarea').value;
            //clear the input
            document.querySelector('#textarea').value = '';
            fetch(`/new_post?content=${content}`)
            .then(response => response.json())
            .then(data => {
                add_post(data);
            })
        } else if (form.id == "edit-post"){ 
            e.preventDefault()

            const post_id = form.parentElement.id.slice(1)
            const content = document.querySelector("#text-edit").value;
            //the new post template
            const edited_post = Handlebars.compile(document.querySelector("#edited-post").innerHTML);
            fetch(`/edit_post?content=${content}&post_id=${post_id}`)
            .then(response => response.json())
            .then(data => {
                    //add the liked variabel to the data
                    data['liked'] = localStorage.getItem('liked');
                    const edited = edited_post(data);
                    document.querySelector(`#p${post_id}`).innerHTML = edited;
            });
        }
    });

    //function for adding on followers
    function following(follow){
        var user = document.querySelector('.user-profile');
        var id = user.id.slice(1)
        fetch(`/follow?follow=${follow}&id=${id}`)
        .then(response => response.json())
        .then(data => {
            document.querySelector('#followers').innerHTML = data.followers;
        });
    }

    //TOGGLE BUTTONS FOR LIKING AND FOLLOWING
    var checkbox = document.querySelectorAll('input[type="checkbox"]');
    checkbox.forEach(toggle => {
        toggle.addEventListener('change', function () {

            if (toggle.className == 'following') {
                if (toggle.checked) {
                    document.querySelector('.slider').innerHTML = 'Unfollow';
                    let follow = 1;
                    following(follow);
                } else if (!toggle.checked) {
                    document.querySelector('.slider').innerHTML = 'Follow';
                    let follow = -1;
                    following(follow);
                }
            } else if (toggle.className === 'liking') {
                //get the id of the parent name 
                const id = toggle.parentElement.parentElement.id.slice(1);

                //define the function to add on likes
                function likes(like, id){
                    fetch(`/like?like=${like}&id=${id}`)
                    .then(response => response.json())
                    .then(data => {
                        var likes = data.likes;
                        document.querySelector(`#p${id} .likes-number`).innerHTML = likes;
                    });
                }

                if (toggle.checked) {
                    let like = 1;
                    likes(like, id)
                } else if (!toggle.checked) {
                    let like = -1;
                    likes(like, id);
                }
            }

        });
    });

    //THE CLICK EVENT FOR THE EDIT BUTTON
    const edit_post = Handlebars.compile(document.querySelector('#edit-post-temp').innerHTML);
    document.addEventListener('click', () => {
        const element = event.target;
        if (element.className == 'edit') {
            //get the parent element
            const parent = element.parentElement;
            const elements = parent.childNodes;
            //get current post information
            var current_text = elements[3].innerText;
            var username = elements[1].innerText;
            var time = elements[7].innerText;
            let id = parent.id;
            var liked = document.querySelector(`#${id} .liking`).checked;
            var likes = document.querySelector(`#${id} .likes-number`).innerHTML;

            //display the edit part
            const new_edit = edit_post({"username": username, "time": time, "liked": liked, "likes": likes});
            parent.innerHTML = new_edit;

            //include the current tweet content in the new edit area
            document.querySelector('#text-edit').value = current_text;

            //store the toggle state in the local storage
            localStorage.setItem('liked', liked)
        }
    })
});