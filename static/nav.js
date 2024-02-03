document.addEventListener("DOMContentLoaded", () => {
    const primaryNav = document.querySelector("#primary-navigation");
    const navToggle = document.querySelector(".mobile-nav-toggle");





    //stoping animation during resizing of the screen

    
    window.addEventListener("resize", () =>{
        document.body.classList.add("resize-animation-stopper");
        setTimeout(() => {
            document.body.classList.remove("resize-animation-stopper")
        }, 400)

    })




    navToggle.addEventListener("click", () => {
        if (primaryNav.dataset.visible == "false"){
            primaryNav.dataset.visible = "true";
            document.querySelector(".brand-styling").dataset.padd = "true";
            navToggle.ariaExpanded = "true";


        }
        else{
            primaryNav.dataset.visible = "false";
            document.querySelector(".brand-styling").dataset.padd = "false";
            navToggle.ariaExpanded = "false";

        }
        })
    })









