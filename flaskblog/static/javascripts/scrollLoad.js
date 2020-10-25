let page = 2;
let main = document.querySelector("main");
window.addEventListener("scroll", scrollLoad);
async function loadNext() {
    try {
        let result = await fetch("/more?page=" + page);
        page++;
        if (!result.ok) {
            throw new Error(response.statusText);
        }
        let new_posts = await result.text();
        main.insertAdjacentHTML("beforeend", new_posts);
    } catch (err) {
        console.log("no more posts");
        window.removeEventListener("scroll", scrollLoad);
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