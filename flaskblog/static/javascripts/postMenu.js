const menuBtns = document.querySelectorAll('.menu-btn');

menuBtns.forEach((btn)=> {
    let options = btn.nextElementSibling;
    let post = btn.parentElement.parentElement;
    btn.addEventListener('click', ()=> {
        options.classList.toggle('show-menu')
    });
    const deleteBtn = options.querySelector('.delete-post');
    const postTitle = post.querySelector(".post-title").textContent;
    deleteBtn.addEventListener("click", () => {deleteModal(postTitle, post.id)});
})

function deleteModal(title, postId) {
    {
            Swal.fire({
                title: "Confirm Post Deleting?",
                text: `Post: ${title}`,
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#d33",
                cancelButtonColor: "#999",
                confirmButtonText: `<label for="delete-${postId}">Yes, Delete It!</label>`,
            })
        }
}