document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("#new-post-form").onsubmit = function (e) {
        e.preventDefault();
        const post_content = document.querySelector("#new-post-content");
        if (post_content.value.trim()) {

            fetch("/new_post", {
                method: "post",
                body: JSON.stringify({
                    post_content: post_content.value,
                })
            }).then(response => response.json())
                .then(data => {
                    post_content.value = '';
                    alert("Post added");
                });

        }
    }
    load_all_post();
});

function load_all_post() {

    const all_post = document.querySelector("#all-posts");

    fetch("/all_post")
        .then(response => response.json())
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