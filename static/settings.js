document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll("input").forEach((inpt) => {
        inpt.addEventListener("input", (e) => {
            e.target.parentElement.parentElement.querySelectorAll(".warn, .warnTWO").forEach((sp) => {
                if (!sp.getAttribute("hidden")){
                    sp.setAttribute("hidden", true);
                }
            })
        })
    })



    document.querySelectorAll(".book-lookup-form").forEach((form) => {
        form.addEventListener("submit", (e) => {
            e.preventDefault();

            element = e.target
            url = element.getAttribute("action")
            let obj = {}
            element.querySelectorAll("input").forEach((inpt) => {
                obj[inpt.getAttribute("id")] = inpt.value
            })

            let jsonData = JSON.stringify(obj);
            let request = new Request(url, {
                method: "POST",
                body: jsonData,
                headers: {"content-type": "application/json"}
            })

            let auxi = function(elmnt, resp_text){

                elmnt.forEach((elmt) => {
                    elmt.removeAttribute("hidden")
                    elmt.innerHTML = resp_text
                })

            }

            let errHandle = async function(request, element){
                let resp = await fetch(request)
                let resp_text = await resp.text()
                if (resp.ok){
                    element.querySelectorAll("input").forEach((inpt) => {
                        inpt.value = "";
                    })
                } else {

                    if (resp.status == 433){

                        auxi(element.querySelectorAll(".warn"), resp_text)

                    } else if (element.getAttribute("id") == "username"){

                        let el = element.querySelector("#passfield")
                        let el1 = element.querySelector("#userfield")
                        let elmnt = resp.status == 434 ? [el] : [el1]
                        auxi(elmnt, resp_text)

                    } else if (element.getAttribute("id") == "password" && resp.status == 435){

                       auxi(element.querySelectorAll("#cnwpass, #cnfrmpass"), resp_text)

                    } else if (element.getAttribute("id") == "password" && resp.status == 434){

                        let elmnt = element.querySelector("#crrntpass")
                        auxi([elmnt], resp_text)

                    }
                }
            }

            errHandle(request, element)

        })

    })

    const tabsContainer = document.querySelector("[role=tablist]");
    const tabButtons = document.querySelectorAll("[role=tab]");
    const tabPanels = document.querySelectorAll("[role=tabpanel]");

    tabsContainer.addEventListener("click", (e) => {
        const clickedTab = e.target.closest("button");
        const currentTab = document.querySelector("[aria-selected='true']");

        if (!clickedTab || currentTab === clickedTab) return;

        switchTab(clickedTab, currentTab);
    })

    function switchTab(clickedTab, oldTab){

        document.querySelectorAll(".warn").forEach((sp) => {
            sp.setAttribute("hidden", true);
        })

        const clickedpanelID = clickedTab.getAttribute("aria-controls");
        const activePanel = tabsContainer.nextElementSibling.querySelector("#" + CSS.escape(clickedpanelID));

        tabButtons.forEach((btn) => {
            btn.setAttribute("aria-selected", false);
            btn.setAttribute("tabindex", "-1");
        })

        tabPanels.forEach((tab) => {
            tab.setAttribute("hidden", true);
        })

        activePanel.removeAttribute("hidden", false);

        clickedTab.setAttribute("aria-selected", true);
        clickedTab.setAttribute("tabindex", "0");
        clickedTab.focus();
        moveIndicator(clickedTab, oldTab);

    }

    function moveIndicator(newTab, oldTab){
        const newTabposition = oldTab.compareDocumentPosition(newTab);
        const newTabWidth = newTab.offsetWidth / tabsContainer.offsetWidth;

        let transitionWidth;

        if (newTabposition === 4){
            transitionWidth = newTab.offsetLeft + newTab.offsetWidth;
        } else {
            transitionWidth = oldTab.offsetLeft + oldTab.offsetWidth - newTab.offsetLeft;
            tabsContainer.style.setProperty("--_left", newTab.offsetLeft + "px");
        }

        tabsContainer.style.setProperty("--_width", transitionWidth / tabsContainer.offsetWidth);

        setTimeout(() => {
            tabsContainer.style.setProperty("--_left", newTab.offsetLeft + "px");
            tabsContainer.style.setProperty("--_width", newTabWidth);
        }, 220);


    }

})
