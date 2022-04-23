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