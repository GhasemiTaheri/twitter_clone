document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".edit-post").forEach(post => {
        post.addEventListener("click", editPost);
    });

});

function editPost() {
    let modal = document.getElementById("myModal");
    modal.style.display = "block";
    let span = document.getElementsByClassName("close")[0];
    span.onclick = function () {
        modal.style.display = "none";
    }
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    const post_id = this.dataset.id
    document.querySelector("#update-post-form").onsubmit = function () {
        let content = document.querySelector("#update-post-input").value;
        if (content.trim()) {
            fetch('/update_post', {
                method: 'PUT',
                body: JSON.stringify({
                    post_id: post_id,
                    content: content
                })
            }).then(response => response.json())
                .then(data => {
                    modal.style.display = "none";
                    alert(data['success']);
                    location.reload();
                })
        }
        return false
    };


}