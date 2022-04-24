document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".like-button").forEach(like => {
        like.addEventListener("click", likePost);
    });

});

function likePost() {
    const like_button = this;
    fetch('/like_post', {
        method: "POST",
        body: JSON.stringify({
            post_id: this.dataset.id,
        })
    }).then(response => response.json()).then(data => {
        const like_info = like_button.nextElementSibling;
        let like_count = like_info.innerHTML.split(" ")[1];
        like_count = parseInt(like_count);

        if (data["status"] === "add like") {
            like_button.className = "bi bi-heart-fill like-button";
            like_button.setAttribute('title', 'unlike');
            like_button.style.color = "#dc3545";

            like_count += 1;
            like_info.innerHTML = `Likes ${like_count}`;
        } else {
            like_button.className = "bi bi-heart like-button";
            like_button.setAttribute('title', 'like');
            like_button.style.color = "";

            like_count -= 1;
            like_info.innerHTML = `Likes ${like_count}`;
        }
    })
}