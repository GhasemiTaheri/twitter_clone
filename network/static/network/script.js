document.addEventListener("DOMContentLoaded", function () {
    // َAdd new post
    document.querySelector("#new-post-form").onsubmit = add_new_post;
});

function add_new_post() {
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
                alert(data.success);
                location.reload();
            });

    } else {
        alert("Please write a text");
    }
    return false;
}

// function load_post() {
//     let type;
//     if (window.location.pathname === "/following-post")
//         type = "following";
//     else
//         type = "all";
//
//     const all_post = document.querySelector("#all-posts");
//
//     fetch(`/load_post/${type}`, {
//         method: "Get"
//     }).then(response => response.json())
//         .then(data => {
//             data.forEach(post => {
//                 let node = document.createElement("div");
//                 node.className = "post border m-3 p-3";
//                 node.innerHTML = `<div><h5><a href="/user/${post.owner}">${post.owner}</a> <small>Follow</small></h5><small style="float: right;">${post.create_date}</small> </div>
//                                 <p>${post.text}</p>
//                                 <i class="bi bi-heart" title="like"></i>
//                                 <small>Likes ${post.likes}</small>`;
//
//                 all_post.append(node);
//             });
//         });
//
//
// }