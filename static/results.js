document.addEventListener("DOMContentLoaded", () => {
    const b_button = document.querySelectorAll(".bt-mark");
    b_button.forEach( (button) => {
        button.addEventListener("click", (e) => {
            let btn = e.target;
            if (btn.dataset.active == "true"){

                const isbn = btn.dataset.isbn;
                let url = `/addbookmark?isbn=${isbn}`;

                fetch(url)
                .then((resp) => {
                    if (!resp.ok) throw new Error("Unable to Bookmark");

                    btn.innerHTML = "Bookmarked";
                    btn.classList.remove("b-mark");
                    btn.classList.remove("btn-colors");
                    btn.classList.add("dis-btn-colors");
                    btn.dataset.active = "false";

                    let r_btn = btn.parentElement.querySelector(".r-bt-mark");
                    r_btn.style.display = "block";

                    r_btn.addEventListener("click", (ev) => {

                        let rv_btn = ev.target;
                        let rv_url = `/rvbookmark?isbn=${isbn}`;

                        fetch(rv_url)
                        .then((resp) => {
                            if (!resp.ok) throw new Error("Unable to Remove");

                            rv_btn.style.display = "none";

                            btn.innerHTML = "Add to Bookmark";
                            btn.classList.add("b-mark");
                            btn.classList.add("btn-colors");
                            btn.classList.remove("dis-btn-colors")
                            btn.dataset.active = "true";


                        })
                        .catch((err) => {
                            alert(err.message);
                        })
                    })

                })
                .catch((err) => {
                    alert(err.message);
                })

            }
        })

    })
})

