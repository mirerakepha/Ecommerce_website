document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("loginForm");

    form.addEventListener("submit", async function (e) {
        e.preventDefault();  // stop normal form submit

        let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

        let formData = new FormData(form);
        let response = await fetch(form.action, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken
            },
            body: formData
        });

        if (response.redirected) {
            // Django redirects to "home" on success
            window.location.href = response.url;
        } else {
            let text = await response.text();
            document.getElementById("message").innerHTML =
                "<p style='color:red;'>Invalid username or password</p>";
            console.log(text); // debug response
        }
    });
});
