document.addEventListener("DOMContentLoaded", function () {
    //َAdd new post
    document.querySelector("#new-post-form").onsubmit = function () {
        const post_content = document.querySelector("#new-post-content");
        if (post_content.value.trim()) {

            fetch("/new_post", {
                method: "post",
                body: JSON.stringify({
                    post_content: post_content.value,
                })
            })
                .then(response => response.json())
                .then(data => {
                    post_content.value = '';
                    document.querySelector("#all-posts").innerHTML = "";
                    load_all_post();
                    alert(data.success);
                });

        } else {
            alert("Please write a text");
        }
        return false;
    }

    window.onscroll = function () {
        if (window.scrollY + window.innerHeight >= document.body.offsetHeight) {
            post_index += 10;
            load_all_post();
        }
    }

    load_all_post();
});

let post_index = 0;

function load_all_post() {

    const all_post = document.querySelector("#all-posts");

    fetch("/all_post", {
        method: "POST",
        body: JSON.stringify({
            index: post_index,
        })
    }).then(response => response.json())
        .then(data => {
            data.forEach(post => {
                let node = document.createElement("div");
                node.className = "post border m-3 p-3";
                node.innerHTML = `<div><h5>${post.owner} <small>Follow</small></h5><small style="float: right;">${post.create_date}</small> </div>
                                <p>${post.text}</p>
                                <i class="bi bi-heart" title="like"></i>
                                <small>Likes ${post.likes}</small>`;

                all_post.append(node);
            });
        });
}