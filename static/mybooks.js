document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".b-mark-bt").forEach((btn) => {
        btn.addEventListener("click", (e) => {

            let button = e.target;
            const isbn = button.dataset.isbn;
            let url = `/rvbookmark?isbn=${isbn}`;

            fetch(url)
            .then((resp) => {
                if (!resp.ok) throw new Error("Couldn't remove the bookmark");


                let html = button.parentElement;
                html.parentElement.style.animationPlayState = "running";
                html.parentElement.addEventListener("animationend", (e) => {
                        let element = e.target;
                        console.log(isbn);
                        element.remove();
                })


            })
            .catch((err) => {
                alert(err.message);
            })
        })
    })
})
