function trans() {
    input = document.getElementById("menu-icon").src;
    if (input === "https://image.flaticon.com/icons/svg/149/149176.svg") {
        input = "https://image.flaticon.com/icons/svg/149/149147.svg";
        console.log("switched")
    } else {
        input = "https://image.flaticon.com/icons/svg/149/149176.svg";
        console.log("switched 1")
    }
}