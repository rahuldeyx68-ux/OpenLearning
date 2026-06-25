/*(function(){
    emailjs.init("vubH6SkYaEIdEpTix");
})();

window.onload = function() {
    const form = document.querySelector("from");

    form.addEventListener("submit", function(event){
        event.preventDefault();


        const templateParams = {
            name: document.getElementById("name").value,
            email: document.getElementById("email").value,
            title: document.getElementById("subject").value,
            message: document.getElementById("message").value
        };

        emailjs.send("service_2iylcrk","template_excdual",templateParams)
         .then(function(response){
            alert("Message sent successfully!");
            console.log("SUCCESS!", response.status, response.text);
         }, function(error){
            alert("Failed to send message. Please try again later.");
            console.log("FAILED...", error);
         });
    });
};*/

// Initialize EmailJS with your Public Key
emailjs.init("service_2iylcrk");

const form = document.getElementById("contact-form");
const status = document.getElementById("status");

form.addEventListener("submit", function (e) {
  e.preventDefault();

  status.textContent = "Sending...";
  status.style.color = "black";

  emailjs.sendForm("service_2iylcrk", "template_excdual", form)
    .then(() => {
      status.textContent = "✅ Message sent successfully!";
      status.style.color = "green";
      form.reset();
    })
    .catch((error) => {
      console.error("EmailJS error:", error);
      status.textContent = "❌ Failed to send message. Please try again.";
      status.style.color = "red";
    });
});
