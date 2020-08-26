const supportForm = document.querySelector("#support-form");
openSupportForm = () => {
    supportForm.style.display = "block";
}

closeSupportForm = () => {
    supportForm.style.display = "none";
}

function openOrders(evt, tab) {
    var i, tabcontent, tablinks;

    tabcontent = document.getElementsByClassName('tab-content-user-profile');
    for (i=0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    tablinks = document.getElementsByClassName('tablinks-user-profile');
    for (i=0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    document.getElementById(tab).style.display = "flex";
    evt.currentTarget.className += " active";
}

function cancelButton() {
    cancel_div = document.getElementById("cancel-div");

    cancel_div.style.display = "block";
}
function hide() {
    cancel_div = document.getElementById("cancel-div");

    cancel_div.style.display = "none";
}

function openProfileEdit() {
    profileEdit = document.querySelector('#profile-edit');
    console.log(profileEdit.style.display);
    profileEdit.style.display = "flex";
    console.log(profileEdit.style.display);
}

function closeProfileEdit() {
    profileEdit = document.querySelector('#profile-edit');
    
    profileEdit.style.display = "none";
}