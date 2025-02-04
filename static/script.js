document.querySelector('form').addEventListener('submit', async function(e) {
            e.preventDefault();

            const formData = new FormData(this);
            const response = await fetch('/upload/', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            if (response.ok) {
                document.getElementById("roast").innerText = data.roast;
            } else {
                alert('There was an error uploading the resume.');
            }
        });

        document.querySelector('form').addEventListener('submit', async function(e) {
    e.preventDefault();

    // Show the spinner while the request is being processed
    document.getElementById("loadingSpinner").style.display = "block";

    const formData = new FormData(this);
    const response = await fetch('/upload/', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();

    // Hide the spinner once we get the response
    document.getElementById("loadingSpinner").style.display = "none";

    if (response.ok) {
        document.getElementById("roast").innerText = data.roast;
        } else {
        alert('There was an error uploading the resume.');
    }
});
        document.querySelector('form').addEventListener('submit', async function(e) {
    e.preventDefault();

    // Show the spinner while the request is being processed
    document.getElementById("loadingSpinner").style.display = "block";

    // Add animation to fade out the form and show loading
    gsap.to("form", { opacity: 0, duration: 0.5 });

    const formData = new FormData(this);
    const response = await fetch('/upload/', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();

    // Hide the spinner once we get the response
    document.getElementById("loadingSpinner").style.display = "none";

    // Fade in the results
    gsap.to("#result", { opacity: 1, duration: 1, y: 30 });

    // Display the roast and analysis in a fun way with animations
    if (response.ok) {
        gsap.fromTo("#roast", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 1 });
    } else {
        alert('There was an error uploading the resume.');
    }

    // Fade the form back in after response
    gsap.to("form", { opacity: 1, duration: 0.5 });
});

        // Wait for the DOM to fully load before applying animations
document.addEventListener("DOMContentLoaded", function () {

  // Button hover effect (scale and bounce)
  gsap.fromTo("#uploadButton",
    { scale: 1, rotation: 0 },
    {
      scale: 1.1,
      rotation: 10,
      duration: 0.5,
      repeat: -1,
      yoyo: true,
      ease: "power1.inOut"
    });

  // Fade-in animation for the form
  gsap.fromTo("#uploadForm",
    { opacity: 0 },
    { opacity: 1, duration: 1, delay: 0.5 });

  // Fade-in animation for the roast result
  gsap.fromTo("#roastResult",
    { opacity: 0 },
    { opacity: 1, duration: 1, delay: 1 });

});

        // Toggle Dark Mode
document.getElementById('themeToggle').addEventListener('click', function() {
  // Toggle the dark mode class on the body
  document.body.classList.toggle('dark-mode');
  // Toggle the button style
  this.classList.toggle('dark-mode');

  // Change the button text based on mode
  if (document.body.classList.contains('dark-mode')) {
    this.innerHTML = "🌞 Toggle Light Mode";
  } else {
    this.innerHTML = "🌙 Toggle Dark Mode";
  }
});