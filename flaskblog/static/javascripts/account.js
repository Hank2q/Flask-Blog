const edit = document.querySelector(".edit");
const close = document.querySelector(".closebtn");
const update = document.querySelector(".update-container");
const pictureInput = document.querySelector("#profile_img");
const modal = document.querySelector(".modal");
const outsideBtn = document.querySelector(".edit-pic");
let outside = false;
edit.onclick = show_update;
close.onclick = show_update;
function show_update() {
    update.classList.toggle("invisible");
}
outsideBtn.addEventListener("click", () => {
    outside = true;
});
document.addEventListener("DOMContentLoaded", () => {
    if (document.querySelector(".error")) {
        update.classList.remove("invisible");
    }
});
modal.addEventListener("click", (event) => {
    let closeModal = modal.querySelector(".fa-times");
    console.log(event.target);
    if (event.target == modal || event.target == closeModal) {
        modal.classList.add("invisible");
    }
});
pictureInput.addEventListener("input", () => {
    if (outside) {
        let fileName = pictureInput.value.split("\\");
        modal.querySelector("h2").innerHTML = fileName[fileName.length - 1];
        var output = document.getElementById("output");
        output.src = URL.createObjectURL(event.target.files[0]);
        output.onload = function () {
            URL.revokeObjectURL(output.src);
        };
        modal.classList.remove("invisible");
        outside = false;
    } else {
        var output = document.getElementById("output2");

        output.src = URL.createObjectURL(event.target.files[0]);
        output.onload = function () {
            URL.revokeObjectURL(output.src);
        };
        output.classList.remove("invisible");
    }
});