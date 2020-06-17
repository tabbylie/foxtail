var onImg = "https://image.flaticon.com/icons/svg/149/149176.svg";
var offImg = "https://image.flaticon.com/icons/svg/149/149147.svg";
trans = () => {
    var img = document.getElementById("menu-icon");
    img.src = img.src == offImg ? onImg : offImg;
}

const supportForm = document.querySelector("#support-form");
openSupportForm = () => {
    supportForm.style.display = "block";
}

closeSupportForm = () => {
    supportForm.style.display = "none";
}