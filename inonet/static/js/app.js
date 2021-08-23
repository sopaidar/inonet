var get_new_likes = true;
var get_new_comment_likes = true;
console.log(sessionStorage.getItem("get_new_comment_likes = get_new_likes"));
if (sessionStorage.getItem("get_new_likes") == false) {
    get_new_likes = false;
    console.log("false");
}
if (sessionStorage.getItem("get_new_comment_likes") == false) {
    get_new_comment_likes = false;
    console.log("get_new_comment_likes = false");
}

//=================url ===================//
const urlParams = new URLSearchParams(window.location.search);

function go_to_comment() {
    const comment_id = urlParams.get('comment');
    if (comment_id) {
        const comment = document.getElementById(comment_id)
        comment.scrollIntoView();
        console.log("dorost")
    }
}

// autosize
function autosize_auto() {
    autosize(document.querySelectorAll(".autosize"));
}
autosize_auto();

// messages modals
var toastElList = [].slice.call(document.querySelectorAll(".start-toast"));
toastElList.map(function(toastEl) {
    toast = new bootstrap.Toast(toastEl, {
        delay: 20000,
    });
    toast.show();
});

// ========================== New Post ==========================//

// new post
const new_post_modal = new bootstrap.Modal(
    document.getElementById("new-post-modal")
);

function new_post() {
    document.getElementById("new-post-modal").classList.remove("succeed");
    document.getElementById("new-post-shared_post").value = "";
    document.getElementById("id_draft").checked = false;
    document.getElementById("id_draft").value = "off";
    new_post_modal.show();
}
document
    .getElementById("new-post-modal")
    .addEventListener("shown.bs.modal", () => {
        document.getElementById("new-post-text").focus();
        if (document.getElementById("new-post-text").value === "") {
            document.getElementById("new-post-button").classList.add("disabled");
        }
        document.getElementById("new-post-text").addEventListener("keyup", () => {
            if (document.getElementById("new-post-text").value !== "") {
                document.getElementById("new-post-button").classList.remove("disabled");
            } else {
                document.getElementById("new-post-button").classList.add("disabled");
            }
        });
    });
document.getElementById("new-post-nav").addEventListener("click", () => {
    new_post();
});

// new post image uploader

const new_post_image_file_reader = new FileReader();
const new_post_image_file_fileInput = document.getElementById(
    "post-picture-upload-file"
);
const new_post_image_file_img = document.getElementById(
    "new-post-picture-upload-img"
);
let new_post_image_file_file;

new_post_image_file_reader.onload = (e) => {
    new_post_image_file_img.src = e.target.result;
    document.getElementById("close-button").style.display = "block";
    document.getElementById("new-post-image-label").innerHTML = "تغییر تصویر";
};

new_post_image_file_fileInput.addEventListener("change", (e) => {
    const f = e.target.files[0];
    new_post_image_file_file = f;
    new_post_image_file_reader.readAsDataURL(f);
});

function reset_new_post_image_input() {
    new_post_image_file_img.src = "";
    document.getElementById("close-button").style.display = "none";
    document.getElementById("new-post-image-label").innerHTML = "افزودن تصویر";
    new_post_image_file_fileInput.value = "";
}
document.getElementById("close-button").addEventListener("click", () => {
    reset_new_post_image_input();
});

// check to save draft
const discard_post_modal = new bootstrap.Modal(
    document.getElementById("discard-post-modal"), {
        backdrop: "static",
        keyboard: false,
    }
);
document
    .getElementById("new-post-modal")
    .addEventListener("hide.bs.modal", () => {
        if (
            document.getElementById("new-post-text").value !== "" ||
            new_post_image_file_fileInput.value !== ""
        ) {
            if (
                document
                .getElementById("new-post-modal")
                .classList.contains("succeed") === false
            ) {
                discard_post_modal.show();
            }
        } else {}
    });
document.getElementById("discard-post").addEventListener("click", () => {
    document.getElementById("new-post-text").value = "";
    document.getElementById("new-post-shared_post").value = "";
    document.getElementById("shared-post").innerHTML = "";
    reset_new_post_image_input();
    discard_post_modal.hide();
});

document.getElementById("save-draft").addEventListener("click", () => {
    document.getElementById("id_draft").checked = true;
    document.getElementById("id_draft").value = "on";
    console.log(document.getElementById("id_draft").checked);
    discard_post_modal.hide();
    send_new_post();
});

// New post

async function send_new_post() {
    let url = "/posts/new/";
    if (document.getElementById("new-post-shared_post").value !== "") {
        url =
            "/posts/new/" +
            document.getElementById("new-post-shared_post").value +
            "/";
    }
    console.log(url);
    const new_post_form = document.getElementById("new-post-form");
    formdata = new FormData(new_post_form);
    document.getElementById("new-post-button").classList.add("disabled");
    document.getElementById("new-post-button").innerHTML =
        'در حال ارسال <span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>';
    response = await fetch(url, {
        method: "POST",
        body: formdata,
    });
    console.log(formdata);
    res = await response.json();
    console.log(res);
    if (res.status === "success") {
        console.log(res.post);
        document.getElementById("new-post-modal").classList.add("succeed");
        new_post_modal.hide();
        document.getElementById("new-post-text").value = "";
        document.getElementById("new-post-shared_post").value = "";
        document.getElementById("shared-post").innerHTML = "";
        reset_new_post_image_input();
        document.getElementById("new-post-button").classList.remove("disabled");
        document.getElementById("new-post-button").innerHTML = "ارسال خبر";
    } else if (res.status === "success") {
        document.getElementById("new-post-button").classList.remove("disabled");
        document.getElementById("new-post-button").innerHTML = "ارسال خبر";
    }
}
document.getElementById("new-post-button").addEventListener("click", () => {
    console.log("a");
    send_new_post();
});

var post_id = 0;
// share with post
Array.prototype.forEach.call(
    document.getElementsByClassName("share-with-post"),
    (el) => {
        el.addEventListener("click", () => {
            console.log("share");
            if (post_id > 0) {
                document.getElementById("new-post-shared_post").value = post_id;
                share_modal.hide();
                new_post_modal.show();
            }
        });
    }
);

// likes
async function get_likes(is_new) {
    if (is_new == false) {
        if (
            localStorage.getItem("inonet_likes") &&
            localStorage.getItem("inonet_shares")
        ) {
            console.log("old_likes");
        } else {
            response = await fetch("/posts/user_likes/");
            res = await response.json();
            console.log(res.likes);
            localStorage.removeItem("inonet_likes");
            localStorage.setItem("inonet_likes", res.likes.likes);
            localStorage.removeItem("inonet_shares");
            localStorage.setItem("inonet_shares", res.shares.shares);
            sessionStorage.setItem("get_new_likes", false);
            get_new_likes = false;
            console.log("new_likes");
        }
    } else {
        response = await fetch("/posts/user_likes/");
        res = await response.json();
        console.log(res.likes);
        localStorage.removeItem("inonet_likes");
        localStorage.setItem("inonet_likes", res.likes.likes);
        localStorage.removeItem("inonet_shares");
        localStorage.setItem("inonet_shares", res.shares.shares);
        sessionStorage.setItem("get_new_likes", false);
        get_new_likes = false;
        console.log("new_likes");
    }
}

get_likes(get_new_likes);

//comment likes
async function get_comment_likes(is_new) {
    if (is_new == false) {
        if (
            localStorage.getItem("inonet_comment_likes")
        ) {
            console.log("old_comment_likes");
        } else {
            response = await fetch("/posts/user_comment_likes/");
            res = await response.json();
            console.log(res.comment_likes);
            localStorage.removeItem("inonet_comment_likes");
            localStorage.setItem("inonet_comment_likes", res.comment_likes.comment_likes);
            sessionStorage.setItem("get_new_comment_likes", false);
            get_new_comment_likes = false;
            console.log("new_comment_likes");
        }
    } else {
        response = await fetch("/posts/user_comment_likes/");
        res = await response.json();
        console.log(res.comment_likes);
        localStorage.removeItem("inonet_comment_likes");
        localStorage.setItem("inonet_comment_likes", res.comment_likes.comment_likes);
        sessionStorage.setItem("get_new_comment_likes", false);
        get_new_comment_likes = false;
        console.log("new_comment_likes");
    }
}

get_comment_likes(get_new_comment_likes);



// buttons

// Like buttons
async function like_post(id) {
    const csrf = document.getElementById("csrf");
    formdata = new FormData(csrf);
    response = await fetch("/posts/like/" + id + "/", {
        method: "POST",
        body: formdata,
    });
    res = await response.json();
    console.log(res.status);
    if (res.status === "success") {
        console.log("liked");
        new_likes = parseInt(
            parseInt(document.getElementById(`${id}-likes-count`).innerHTML) + 1
        );
        if (new_likes > -1) {
            document.getElementById(`${id}-likes-count`).innerHTML = new_likes;
        }
    } else if (res.status === "failed") {
        console.log(res.errors);
    }
}

async function dislike_post(id) {
    const csrf = document.getElementById("csrf");
    formdata = new FormData(csrf);
    response = await fetch("/posts/dislike/" + id + "/", {
        method: "POST",
        body: formdata,
    });
    res = await response.json();
    console.log(res.status);
    if (res.status === "success") {
        console.log("disliked");
        get_likes(true);
        new_likes = parseInt(
            parseInt(document.getElementById(`${id}-likes-count`).innerHTML) - 1
        );
        if (new_likes > -1) {
            document.getElementById(`${id}-likes-count`).innerHTML = new_likes;
        }
    } else if (res.status === "failed") {
        console.log(res.errors);
    }
}

//==========================Comment Like===========================//

async function like_comment(id) {
    const csrf = document.getElementById("csrf");
    formdata = new FormData(csrf);
    response = await fetch("/posts/like_comment/" + id + "/", {
        method: "POST",
        body: formdata,
    });
    res = await response.json();
    console.log(res.status);
    if (res.status === "success") {
        console.log("liked");
        document.getElementById(`${id}-like-button`).setAttribute("href", `javascript:dislike_comment('${id}');`)
        document.getElementById(`${id}-like-button`).innerHTML = "حذف پسند";
        document.getElementById(`${id}-comment-likes-icon`).innerHTML = "favorite";
        document.getElementById(`${id}-comment-likes-count`).innerHTML = res.likes;
    } else if (res.status === "failed") {
        console.log(res.errors);
    }
}

async function dislike_comment(id) {
    const csrf = document.getElementById("csrf");
    formdata = new FormData(csrf);
    response = await fetch("/posts/dislike_comment/" + id + "/", {
        method: "POST",
        body: formdata,
    });
    res = await response.json();
    console.log(res.status);
    if (res.status === "success") {
        console.log("disliked");
        document.getElementById(`${id}-like-button`).setAttribute("href", `javascript:like_comment('${id}');`)
        document.getElementById(`${id}-like-button`).innerHTML = "پسندیدن";
        document.getElementById(`${id}-comment-likes-icon`).innerHTML = "favorite_border";
        document.getElementById(`${id}-comment-likes-count`).innerHTML = res.likes;
    } else if (res.status === "failed") {
        console.log(res.errors);
    }
}



//===================//=========================//=======================//

function buttons() {
    get_likes(false);
    likes = localStorage.getItem("inonet_likes");
    els = document.getElementsByClassName("like-button");
    Array.prototype.forEach.call(els, function(el) {
        function get_likes_from_storage() {
            if (likes.includes(el.id)) {
                el.classList.add("is-active");
            }
        }
        get_likes_from_storage();
        el.addEventListener("click", () => {
            if (el.classList.contains("is-active")) {
                console.log("active");
                dislike_post(el.id);
            } else {
                console.log("not active");
                like_post(el.id);
                get_likes(true);
            }
            el.classList.toggle("is-active");
        });
    });
}

// share buttons
const post_share_modal = new bootstrap.Modal(
    document.getElementById("new-post-modal")
);
const share_modal = new bootstrap.Modal(document.getElementById("share-modal"));

function get_shares_from_storage(element) {
    shares = localStorage.getItem("inonet_shares");

    if (shares.includes(element.getAttribute("post-id"))) {
        element.classList.add("is-active");
    }
}

async function share_post(id) {
    const csrf = document.getElementById("csrf");
    formdata = new FormData(csrf);
    response = await fetch("/posts/share/" + id + "/", {
        method: "POST",
        body: formdata,
    });
    res = await response.json();
    console.log(res.status);
    if (res.status === "success") {
        console.log("shared");
        new_shares = parseInt(
            parseInt(document.getElementById(`${id}-share-count`).innerHTML) + 1
        );
        if (new_shares > -1) {
            document.getElementById(`${id}-share-count`).innerHTML = new_shares;
        }
    } else if (res.status === "failed") {
        console.log(res.errors);
    }
}

async function unshare_post(id) {
    const csrf = document.getElementById("csrf");
    formdata = new FormData(csrf);
    response = await fetch("/posts/unshare/" + id + "/", {
        method: "POST",
        body: formdata,
    });
    res = await response.json();
    console.log(res.status);
    if (res.status === "success") {
        console.log("unshared");
        new_shares = parseInt(
            parseInt(document.getElementById(`${id}-share-count`).innerHTML) - 1
        );
        if (new_shares > -1) {
            document.getElementById(`${id}-share-count`).innerHTML = new_shares;
        }
        get_likes(true);
    } else if (res.status === "failed") {
        console.log(res.errors);
    }
}

function share_buttons() {
    get_likes(false);
    els = document.getElementsByClassName("share-button");
    Array.prototype.forEach.call(els, function(el) {
        get_shares_from_storage(el);
        el.addEventListener("click", () => {
            post_id = el.getAttribute("post-id");
            console.log("post_id: " + post_id);
            if (el.classList.contains("is-active")) {
                const unshare_modal = new bootstrap.Modal(
                    document.getElementById("unshare-modal")
                );
                unshare_modal.show();
                console.log("active");

                document
                    .getElementById("unshare-unshare-post")
                    .addEventListener("click", () => {
                        unshare_post(el.getAttribute("post-id"));

                        el.classList.remove("is-active");
                        unshare_modal.hide();
                    });
                document
                    .getElementById("unshare-share-post-with-post")
                    .addEventListener("click", () => {
                        unshare_modal.hide();
                        new_post();
                        share_with_post(el.getAttribute("post-id"));
                    });
            } else {
                console.log("not active");

                share_modal.show();
                document
                    .getElementById("share-share-post")
                    .addEventListener("click", () => {
                        share_post(el.getAttribute("post-id"));
                        get_likes(false);
                        el.classList.add("is-active");
                        share_modal.hide();
                    });
                document
                    .getElementById("share-share-post-with-post")
                    .addEventListener("click", () => {
                        share_modal.hide();
                        new_post();
                        share_with_post(el.getAttribute("post-id"));
                    });
            }
        });
    });
}

function share_with_post(id) {
    document.getElementById("new-post-modal").classList.remove("succeed");
    document.getElementById("id_draft").checked = false;
    document.getElementById("id_draft").value = "off";
    const post = document.getElementById(`post-text-${id}`).innerHTML;
    document.getElementById("new-post-shared_post").value = id;
    document.getElementById("shared-post").classList.remove("d-none");
    document.getElementById("shared-post").innerHTML = post;
}

// comments
async function fetch_comments(post_id, is_new) {
    const comment_div = document.getElementById("comments-div-" + post_id);
    response = await fetch("/posts/" + post_id + "/comments/");
    res = await response.json();
    const seprator = document.createElement("div");
    seprator.classList.add("m-3");
    comment_div.append(seprator);
    if (is_new === false) {
        const old_comments = document.getElementsByClassName(
            `post-${post_id}-comments`
        );
        Array.prototype.forEach.call(old_comments, (comment) => {
            comment.innerHTML = "";
            comment.classList.add("d-none");
        });
    }
    get_comment_likes(get_comment_likes);
    const comment_likes = localStorage.getItem("inonet_comment_likes")
    Array.prototype.forEach.call(res, (comment) => {
        let comment_avatar = "/static/images/picture.svg";
        if (comment.fields.user.avatar_url) {
            comment_avatar = comment.fields.user.avatar_url;
        }
        let comment_html;
        if (comment_likes.includes(comment.fields.uuid)) {
            comment_html = `
            <div class="new-comment-div">
                <div class="comment-avatar me-1">
                <a href="/users/${comment.fields.user.username}/" class="image-link">
                    <img src="${comment_avatar}" class="avatar comment-avatar" alt="user avatar" width="40px" height="40px">
                </a>
                </div>
                <div class="comment">
                <p><a href="/users/${comment.fields.user.username}/">${comment.fields.user.first_name} ${comment.fields.user.last_name}</a></p>
                <p class="comment-text">${comment.fields.text}</p>
                <div class="comment-like-count">
                    
                    <p class="comment-like-div shadow ms-1 me-1">
                    <span class="material-icons-outlined align-middle comment-like-icon" id="${comment.fields.uuid}-comment-likes-icon">
                    favorite
                    </span>
                    <span id="${comment.fields.uuid}-comment-likes-count">
                    ${comment.fields.likes}
                    </span>
                </p>
                </div>
                </div>
                
            </div>
            <div class="comment-buttons">
                <div class="text-muted comment-date ">
                    <a href="javascript:dislike_comment('${comment.fields.uuid}');" id="${comment.fields.uuid}-like-button">حذف پسند</a> .
                    <span class="persian-date">${comment.fields.date_time}</span>
                    <li class="dropdown more-button-list" style="display:inline;">
                        <a href="#" class="more-text" id="comment-${comment.fields.uuid}-report" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <span class="p-0 m-o material-icons comment-more-icon align-middle">more_horiz</span>
                        </a>
                        <ul class="dropdown-menu shadow" aria-labelledby="navbarDropdown-2">
                            <li class="dropdown-item">
                                <a href="javascript:report('comment', '${comment.fields.uuid}');" class="nav-link text-reset comment-report-text">
                                    <span class="material-icons-outlined comment-more-icon align-middle">
                                        report
                                    </span> گزارش تخلف
                                </a>
                            </li>
                        </ul>
                    </li>
                </div>
            </div>
            `;
        } else {
            comment_html = `
            <div class="new-comment-div">
                <div class="comment-avatar me-1">
                <a href="/users/${comment.fields.user.username}/" class="image-link">
                    <img src="${comment_avatar}" class="avatar comment-avatar" alt="user avatar" width="40px" height="40px">
                </a>
                </div>
                <div class="comment">
                <p><a href="/users/${comment.fields.user.username}/">${comment.fields.user.first_name} ${comment.fields.user.last_name}</a></p>
                <p class="comment-text">${comment.fields.text}</p>
                <div class="comment-like-count">
                    
                    <p class="comment-like-div shadow ms-1 me-1">
                    <span class="material-icons-outlined align-middle comment-like-icon" id="${comment.fields.uuid}-comment-likes-icon">
                    favorite_border
                    </span>
                    <span id="${comment.fields.uuid}-comment-likes-count">
                    ${comment.fields.likes}
                    </span>
                </p>
                </div>
                </div>
                
            </div>
            <div class="comment-buttons">
                <div class="text-muted comment-date ">
                    <a href="javascript:like_comment('${comment.fields.uuid}');" id="${comment.fields.uuid}-like-button">پسندیدن</a> .
                    <span class="persian-date">${comment.fields.date_time}</span>
                    <li class="dropdown more-button-list" style="display:inline;">
                        <a href="#" class="more-text" id="comment-${comment.fields.uuid}-report" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <span class="p-0 m-o material-icons comment-more-icon align-middle">more_horiz</span>
                        </a>
                        <ul class="dropdown-menu shadow" aria-labelledby="navbarDropdown-2">
                            <li class="dropdown-item">
                                <a href="javascript:report('comment', '${comment.fields.uuid}');" class="nav-link text-reset comment-report-text">
                                    <span class="material-icons-outlined comment-more-icon align-middle">
                                        report
                                    </span> گزارش تخلف
                                </a>
                            </li>
                        </ul>
                    </li>
                </div>
            </div>
            `;
        }
        const one_comment = document.createElement("div");
        one_comment.classList.add(`post-${post_id}-comments`);
        one_comment.classList.add(`post-comment`);
        one_comment.id = comment.fields.uuid;
        one_comment.innerHTML = comment_html;
        comment_div.append(one_comment);
    });
    comment_div.classList.add("fetched");
    document.getElementById(`${post_id}-comments-count`).innerHTML = res.length;
    persian_date();
    go_to_comment();
}

function comment_buttons() {
    const comment_els = document.getElementsByClassName("comment-button");
    Array.prototype.forEach.call(comment_els, function(el) {
        el.addEventListener("click", () => {
            el.classList.toggle("is-active");
            const post_id = el.getAttribute("post-id");
            document
                .getElementById("comments-div-" + post_id)
                .classList.toggle("d-none");
            if (
                document
                .getElementById("comments-div-" + post_id)
                .classList.contains("fetched") === false
            ) {
                fetch_comments(post_id, true);
            }
        });
    });
    const comment_inputs = document.getElementsByClassName("comment-form-input");
    Array.prototype.forEach.call(comment_inputs, function(el) {
        el.addEventListener("keypress", function(e) {
            if (e.keyCode === 13 && e.shiftKey) {} else if (e.keyCode === 13) {
                e.preventDefault();
                if (el.value == "" || el.value == "\n") {
                    return false;
                }
                el.classList.toggle("disabled");
                const form = document.getElementById(
                    "comment-form-" + el.getAttribute("post-id")
                );

                const formdata = new FormData(form);
                const csrf = document.getElementsByName("csrfmiddlewaretoken")[0];
                console.log(csrf.name + "/n" + csrf.value);
                formdata.append(csrf.name, csrf.value);
                async function send_comment() {
                    response = await fetch(
                        "/posts/" + el.getAttribute("post-id") + "/comments/new/", {
                            method: "POST",
                            body: formdata,
                        }
                    );
                    res = await response.json();
                    if (res.status === "success") {
                        console.log("success");
                        el.value = "";
                        el.classList.toggle("disabled");
                        fetch_comments(el.getAttribute("post-id"), false);
                    } else {
                        console.log(res.errors);
                        el.classList.toggle("disabled");
                    }
                }
                send_comment();
            }
        });
    });
}

// action buttons ?share buttons?
function action_buttons() {
    const action_els = document.getElementsByClassName("action-button");
    Array.prototype.forEach.call(action_els, function(el) {
        el.addEventListener("click", () => {
            el.classList.toggle("is-active");
        });
    });
}

// copy post address
function copyaddress(id) {
    const el = document.createElement("textarea");
    el.value = `https://inonet.ir/posts/${id}/`;
    document.body.appendChild(el);
    el.select();
    document.execCommand("copy");
    document.getElementById("toast-title").innerHTML = "آدرس پست کپی شد!";
    document.getElementById(
        "toast-body"
    ).innerHTML = `<p dir="ltr">https://inonet.ir/posts/${id}/</p>`;
    const toast_div = document.getElementById("liveToast");
    const toast = new bootstrap.Toast(toast_div, {
        delay: 3000,
    });
    toast.show();
    document.body.removeChild(el);
}

function copy_element_text(text) {
    const el = document.createElement("textarea");
    el.value = text;
    document.body.appendChild(el);
    el.select();
    document.execCommand("copy");
    document.getElementById("toast-title").innerHTML = "کپی شد!";
    document.getElementById("toast-body").innerHTML = `<p dir="ltr">${text}/</p>`;
    const toast_div = document.getElementById("liveToast");
    const toast = new bootstrap.Toast(toast_div, {
        delay: 3000,
    });
    toast.show();
    document.body.removeChild(el);
}

// system share post address
async function shareaddress(id) {
    try {
        await window.navigator.share({
            url: `https://inonet.ir/posts/${id}/`,
        });
        console.log("Success");
    } catch (err) {
        console.log("Error: " + err);
    }
}

// ============================= Follow =============================

async function get_followings(is_new) {
    if (is_new == false) {
        if (localStorage.getItem("inonet_followings")) {
            return localStorage.getItem("inonet_followings");
        } else {
            response = await fetch("/user/user_followings/");
            res = await response.json();
            if (res.status == "success") {
                localStorage.removeItem("inonet_followings");
                localStorage.setItem("inonet_followings", res.followings.followings);
                console.log("followings:" + localStorage.getItem("inonet_followings"));
                return res.followings.followings;
            }
        }
    } else {
        response = await fetch("/user/user_followings/");
        res = await response.json();
        if (res.status == "success") {
            localStorage.removeItem("inonet_followings");
            localStorage.setItem("inonet_followings", res.followings.followings);
            console.log("followings:" + res.followings.followings);
            return res.followings.followings;
        }
    }
}
async function buuton_is_followed() {
    const followings = await get_followings(false);
    console.log(followings);
    const follow_buttons = document.getElementsByClassName("follow-button");
    Array.prototype.forEach.call(follow_buttons, (follow_button) => {
        if (followings.includes(follow_button.id)) {
            follow_button.classList.add("followed");
            follow_button.innerHTML = "دنبال می‌کنید &#10003;";
            follow_button.classList.add("btn-primary");
            follow_button.classList.remove("btn-outline-primary");
        } else {
            follow_button.classList.add("not-followed");
            follow_button.innerHTML = "دنبال کردن";
            follow_button.classList.remove("btn-primary");
            follow_button.classList.add("btn-outline-primary");
        }
    });
}

get_followings(true);

async function follow(username) {
    const button = document.getElementById(username);
    if (button.classList.contains("not-followed")) {
        const form = document.getElementById("csrf");
        const formdata = new FormData(form);
        const response = await fetch(`/user/${username}/follow/`, {
            method: "POST",
            body: formdata,
        });
        const res = await response.json();
        if (res.status == "success") {
            button.classList.add("followed");
            button.classList.remove("not-followed");
            button.classList.add("btn-primary");
            button.classList.remove("btn-outline-primary");
            button.innerHTML = "دنبال می‌کنید &#10003;";
            console.log(res);
        } else {
            console.log("error" + res);
        }
    } else if (button.classList.contains("followed")) {
        const form = document.getElementById("csrf");
        const formdata = new FormData(form);
        const response = await fetch(`/user/${username}/unfollow/`, {
            method: "POST",
            body: formdata,
        });
        const res = await response.json();
        if (res.status == "success") {
            button.classList.remove("followed");
            button.classList.add("not-followed");
            button.classList.remove("btn-primary");
            button.classList.add("btn-outline-primary");
            button.innerHTML = "دنبال کردن";
            console.log(res);
        } else {
            console.log("error" + res);
        }
    }
}

// ============================= Notifications =============================

async function fetch_notifications() {
    const response = await fetch("/notifications/new/");
    const res = await response.text();
    document.getElementById("notification").innerHTML = res;
    const new_notifications = document
        .getElementById("notification")
        .getElementsByClassName("new-notification");
    if (new_notifications.length > 0) {
        document.getElementById("badge").innerHTML = new_notifications.length;
    } else if (new_notifications.length === 0) {
        document.getElementById("badge").innerHTML = "";
    }
}

async function send_seen() {
    const csrf = document.getElementById("csrf");
    formdata = new FormData(csrf);
    const response = await fetch("/notifications/seen/", {
        method: "POST",
        body: formdata,
    });
    const res = await response.json();
    if (res.status === "success") {
        return true;
    }
}

document.addEventListener("DOMContentLoaded", () => {
    fetch_notifications();
    setInterval(() => {
        fetch_notifications();
    }, 30000);
});
document.getElementById("notification-icon").addEventListener("click", () => {
    if (a) {
        clearTimeout(a);
    }
    // fetch_notifications()
    const send = send_seen();
    if (send) {
        const new_notifications = document
            .getElementById("notification")
            .getElementsByClassName("new-notification");
        var a = setTimeout(() => {
            Array.prototype.forEach.call(new_notifications, (notification) => {
                console.log("hey");
                notification.classList.remove("notification");
                notification.classList.add("seen-notification");
            });
            document.getElementById("badge").innerHTML = "";
        }, 1000);
    }
});

// ====================== loading =====================//
function loading(id) {
    const loading_div = `
    <div class="m-5">
      <div class="d-flex justify-content-center">
          <div class="spinner-grow text-primary m-2" role="status">
              <span class="visually-hidden">Loading...</span>
          </div>
          <div class="spinner-grow text-success m-2" role="status">
              <span class="visually-hidden">Loading...</span>
          </div>
          <div class="spinner-grow text-warning m-2" role="status">
              <span class="visually-hidden">Loading...</span>
          </div>
          <div class="spinner-grow text-info m-2" role="status">
              <span class="visually-hidden">Loading...</span>
          </div>
          <div class="spinner-grow text-danger m-2" role="status">
              <span class="visually-hidden">Loading...</span>
          </div>
      </div>
    </div>
    `;
    console.log("loading");
    document.getElementById(id).innerHTML = loading_div;
}

function persian_date() {
    const persian_date = document.querySelectorAll(".persian-date");
    Array.prototype.forEach.call(persian_date, (date) => {
        let new_date = new persianDate(date.innerHTML)
            .toLocale("fa")
            .toCalendar("persian")
            .format("D MMMM YYYY - HH:m:s");
        date.innerHTML = new_date;
    });
}
document.addEventListener("DOMContentLoaded", () => {
    persian_date();
});

//================== load posts ==========================//

function add_loading(div_id, number) {
    const loading_div = `
    <div class="m-5" id="loading-post-${number}">
      <div class="d-flex justify-content-center">
          <div class="spinner-grow text-primary m-2" role="status">
              <span class="visually-hidden">Loading...</span>
          </div>
          <div class="spinner-grow text-success m-2" role="status">
              <span class="visually-hidden">Loading...</span>
          </div>
          <div class="spinner-grow text-warning m-2" role="status">
              <span class="visually-hidden">Loading...</span>
          </div>
          <div class="spinner-grow text-info m-2" role="status">
              <span class="visually-hidden">Loading...</span>
          </div>
          <div class="spinner-grow text-danger m-2" role="status">
              <span class="visually-hidden">Loading...</span>
          </div>
      </div>
    </div>
    `;
    console.log(`loading-post-${number}`);
    document.getElementById(div_id).insertAdjacentHTML("beforeend", loading_div);
}



// Globals
let isFetching = false;
let currentPage = 1;
let has_pages = true;

// Functions
const fetchPosts = async(url, div_id, resize) => {
    if (has_pages != true) {
        return
    }
    if (currentPage > 1) {
        add_loading(div_id, currentPage);
    }
    isFetching = true;
    const response = await fetch(`${url}?page=${currentPage}`, {
        method: "GET",
    });
    res = await response.text();
    if (response.status != 200) {
        document.getElementById(`loading-post-${currentPage}`).innerHTML = "<hr>"
        has_pages = false
        return
    }
    if (currentPage < 2) {
        document.getElementById(div_id).innerHTML = res;
    } else {
        document.getElementById(div_id).insertAdjacentHTML("beforeend", res);
    }
    buttons();
    share_buttons();
    comment_buttons();
    action_buttons();
    autosize_auto();
    persian_date();
    if (resize) {
        const posts_div = document.getElementsByClassName("post-div");
        Array.prototype.forEach.call(posts_div, (post) => {
            post.classList.remove("col-md-6");
            post.classList.add("col-md-8");
        });

    }
    if (currentPage > 1) {
        document.getElementById(`loading-post-${currentPage}`).classList.add("d-none")
    }
    currentPage++;
    isFetching = false;
};

//==================== report ========================//
const report_modal = new bootstrap.Modal(
    document.getElementById("report-modal")
);

function report(r_type, id) {
    const report_type = document.getElementById("report-form-report_type");
    const post = document.getElementById("report-form-post");
    const user = document.getElementById("report-form-user");
    const comment = document.getElementById("report-form-comment");
    const work = document.getElementById("report-form-work");
    report_type.value = ""
    post.value = ""
    user.value = ""
    comment.value = ""
    work.value = ""
    if (r_type === "user") {
        report_type.value = "کاربر";
        user.value = id;
    } else if (r_type === "post") {
        report_type.value = "پست";
        post.value = id;
    } else if (r_type === "comment") {
        report_type.value = "نظر";
        comment.value = id;
    } else if (r_type === "work") {
        report_type.value = "اثر";
        work.value = id;
    }
    report_modal.show();
}

async function fetch_report(url) {
    const form = document.getElementById("report-form");
    formdata = new FormData(form);
    const response = await fetch(url, { method: "POST", body: formdata });
    const res = await response.json();
    console.log(res)
    if (res.status == "success") {
        report_modal.hide();
        document.getElementById("toast-title").innerHTML = "گزارش شما ارسال شد!";
        document.getElementById(
            "toast-body"
        ).innerHTML = "از شما برای آن که به جامعه کاربری اینونت کمک نمودید متشکریم.";
        const toast_div = document.getElementById("liveToast");
        const toast = new bootstrap.Toast(toast_div, {
            delay: 3000,
        });
        toast.show();
    }
    document.getElementById("report-submit").classList.remove("disabled");
    document.getElementById("report-submit").innerHTML = 'ارسال';
}

function send_report() {
    document.getElementById("report-submit").classList.add("disabled");
    document.getElementById("report-submit").innerHTML =
        'در حال ارسال <span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>';
    let url = "/report/"
    const post = document.getElementById("report-form-post").value;
    const user = document.getElementById("report-form-user").value;
    const comment = document.getElementById("report-form-comment").value;
    const work = document.getElementById("report-form-work").value;
    if (user) {
        url = `/report/user/${user}/`
    } else if (post) {
        url = `/report/post/${post}/`
    } else if (comment) {
        url = `/report/comment/${comment}/`
    } else if (work) {
        url = `/report/work/${work}/`
    }
    fetch_report(url);

}