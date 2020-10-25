let page = 1;
let posts = document.querySelector(".posts");
let pages = parseInt(posts.dataset.pages, 10);
const loader = document.querySelector('.loader')
const bottom = document.querySelector('.bottom')
document.addEventListener('DOMContentLoaded', () => {
    let options = {
        root: null,
        rootMargins: "100px",
        threshold: 0.5
    }
    let observer = new IntersectionObserver(intersectHandler, options)
    observer.observe(bottom)
})


function intersectHandler(entries) {
    if (entries[0].isIntersecting) {
        loadNext();
    }
}


async function loadNext() {
    page++;
    if (page <= pages) {
        loader.classList.add('show')
        bottom.querySelector('p').innerHTML = ''
        try {
            let result = await fetch("/more?page=" + page);
            if (!result.ok) {
                throw new Error(response.statusText);
            }
            let new_posts = await result.text();
            loader.classList.remove('show')
            posts.insertAdjacentHTML("beforeend", new_posts);
        } catch (err) {
            console.log("no more posts");
        }
    } else {
        loader.classList.remove('show')
        bottom.querySelector('p').innerHTML = 'No More Posts!'
    }
}
    

function scrollLoad() {
    let currnent = window.scrollY;
    let yHeight = document.documentElement.scrollHeight - window.innerHeight;
    let vh = currnent / yHeight;
    if (vh > 0.9) {
        loadNext();
    }
}