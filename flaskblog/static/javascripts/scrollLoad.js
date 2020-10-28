let page = 1;
let posts = document.querySelector(".posts");
let pages = parseInt(posts.dataset.pages, 10);
const loader = document.querySelector('.loader')
const bottom = document.querySelector('.bottom')
const toTop = document.querySelector('.to-top')

// trigger fetching when reaching bottom of current posts
document.addEventListener('DOMContentLoaded', () => {
    let options = {
        root: null,
        rootMargins: "100px",
        threshold: 0.5
    }
    let observer = new IntersectionObserver(intersectHandler, options)
    observer.observe(bottom)
})


// show back to top button after 2000px
window.addEventListener('scroll', () => {
    if (window.pageYOffset > 2500) {
        toTop.classList.add('show-top')
    } else {
        toTop.classList.remove('show-top')
    }
})


// fetch next page if reached the bottom of the current posts page
function intersectHandler(entries) {
    if (entries[0].isIntersecting) {
        loadNext();
    }
}

// check if still got more posts pages to load then fetch the next posts page
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

            // fire an event so postMenu script will add its functionality to
            // newly added posts
            newContentLoaded()

        } catch (err) {
            console.log("no more posts");
        }
    } else {
        loader.classList.remove('show')
        bottom.querySelector('p').innerHTML = 'No More Posts!'
    }
}

function newContentLoaded() {
    const event = new CustomEvent('NewContentLoaded', {})
    document.dispatchEvent(event)
}