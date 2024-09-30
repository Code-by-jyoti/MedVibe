document.addEventListener("DOMContentLoaded", () => {
    const accordionButtons = document.querySelectorAll(".accordion-button1");

    accordionButtons.forEach(button => {
        button.addEventListener("click", () => {
            const accordionBody = button.parentElement.nextElementSibling;
            const caret = button.querySelector(".caret");
            
            if (accordionBody.style.display === "block") {
                accordionBody.style.display = "none";
                caret.style.transform = "rotate(0deg)";
            } else {
                // Hide all other accordion items
                document.querySelectorAll(".accordion-body").forEach(body => {
                    body.style.display = "none";
                });
                document.querySelectorAll(".caret").forEach(caret => {
                    caret.style.transform = "rotate(0deg)";
                });

                accordionBody.style.display = "block";
                caret.style.transform = "rotate(180deg)";
            }
        });
    });
});
