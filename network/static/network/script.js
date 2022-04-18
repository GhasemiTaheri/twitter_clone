document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("#new-post-form").onsubmit = function (e) {
        e.preventDefault();
        const post_content = document.querySelector("#new-post-content");
        if (post_content.value.trim()) {

            fetch("new_post", {
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
});