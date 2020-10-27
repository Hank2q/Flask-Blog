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

window.addEventListener('click', (e) => {
    let openedMenu = document.querySelector('.show-menu')
        if (openedMenu && !openedMenu.parentElement.contains(e.target)) {
            openedMenu.classList.remove('show-menu')
        }
    
})

async function deleteModal(title, postId) {
    {
            let result = await Swal.fire({
                title: "Confirm Post Deleting?",
                text: `Post: ${title}`,
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#d33",
                cancelButtonColor: "#999",
                confirmButtonText: `Yes, Delete It!`,
            })

            if (result.isConfirmed) {
                let form = document.querySelector(`#delete-${postId}`)
                form.submit()
            }

        }
}