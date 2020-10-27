// elements
const edit = document.querySelector(".edit");
const close = document.querySelector(".closebtn");
const update = document.querySelector(".update-container");
const pictureInput = document.querySelector("#profile_img");
const pictureContainer = document.querySelector('.img-cont')
const outsideBtn = document.querySelector(".edit-pic");
const expand = document.querySelector('.list')
const updateForm = document.querySelector('#update-form')
let expanded = false;

// event listeners
edit.onclick = toggleUpdate;
close.onclick = toggleUpdate;
expand.onclick = expandPosts;
outsideBtn.onclick = outsideUpload;

document.addEventListener("DOMContentLoaded", () => {
    // loads posts menu as it was in the session, cloased or open
    loadExpanded();
    // show the profile edit menu after a failed form submission
    if (document.querySelector(".error")) {
        update.classList.remove("invisible");
    }

});

pictureInput.addEventListener("input", () => {
    // changing profile picture within the form, to show the sample
    var output = document.getElementById("output");
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function () {
        URL.revokeObjectURL(output.src);
    };
    output.classList.remove("invisible");

});

pictureContainer.addEventListener('mouseover', picIn)


pictureContainer.addEventListener('mouseout', picOut)

//functions
// opens the post menu if it was already opened in the session
function loadExpanded() {
    let memory = sessionStorage.getItem('expanded');
    if (memory=='true') {
        expandPosts();
    }
};

function expandPosts() {
    let posts = document.querySelector('.posts')
    if (posts.dataset.pages > 1) {
        let pages = document.querySelector('.pages')
        pages.classList.toggle('invisible')
    }
    posts.classList.toggle('expanded');
    expand.querySelector('i').classList.toggle('rotated');
    expanded = !expanded;
    sessionStorage.setItem('expanded', expanded);
}

function toggleUpdate() {
    update.classList.toggle("invisible");
}


// simulate css hover, to fix issue with sweetalert intigration
function picIn() {
    pictureContainer.classList.add('img-cont-hover')
    outsideBtn.classList.add('edit-pic-show')
}
function picOut() {
    pictureContainer.classList.remove('img-cont-hover')
    outsideBtn.classList.remove('edit-pic-show')
}

// handle picture changing outside the form, by a modal
async function outsideUpload() {
    const result = await Swal.fire({
    title: 'Select image',
    input: 'file',
    inputAttributes: {
    'accept': 'image/png, image/jpeg, image/jpg',
    'aria-label': 'Upload your profile picture'
    },
    confirmButtonText: `Upload`,
    showCloseButton: true
    })

    // handel dissmissing the modal without uploading
    // to fix hover issue
    if (result.isDismissed || !result.value) {
        picIn()
        setTimeout(picOut, 500)
    }
    let file = result.value;
    if (file) {
    pictureInput.files = new FileListItems(file)
    const reader = new FileReader()
    reader.onload = async(e) => {
        let res = await Swal.fire({
        title: `New Profile Picture: ${file.name}`,
        imageUrl: e.target.result,
        imageAlt: `The uploaded picture`,
        showCloseButton: true,
        confirmButtonText: `Update Profile Picture`,
        confirmButtonColor: '#4caf50'
        })
        // handle dismissing the modal after hovering, return the form file input to empty
        if (res.isDismissed) {
            pictureInput.files = new FileListItems(null)
            picIn()
            setTimeout(picOut, 500)

        } else if (res.isConfirmed){
            updateForm.submit()
        }
    }
    reader.readAsDataURL(file)
    }  
}

function FileListItems (file) {
    var b = new ClipboardEvent("").clipboardData || new DataTransfer()
    if (file != null) {
        b.items.add(file)
    }
    return b.files
}