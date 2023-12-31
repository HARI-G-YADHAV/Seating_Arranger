function toggleForm(e) {
    var signupForm = document.getElementById("signupForm");
    var signinForm = document.getElementById("signinForm");
    
    if (signupForm.style.display === "none") {
      signupForm.style.display = "block";
      signinForm.style.display = "none";
    } else {
      signupForm.style.display = "none";
      signinForm.style.display = "block";
    }
}
const userToken = 'your-user-token-value'; 
function signIn() {
  var username = document.getElementById('Username').value;
  var password = document.getElementById('Password').value;

  // Create JSON payload
  var jsonData = {
    username: username,
    password: password
  };

  // Make POST request to sign-in API endpoint
  fetch('http://localhost:8000//api/sign-in/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Token ${userToken}`,
    },
    body: JSON.stringify(jsonData)
  })
    .then(response => response.json())
    .then(data => {
      // Handle the response from the sign-in API
      console.log(data);
      const message = data.message;
      const is_admin = data.is_admin;
      const is_staff = data.is_staff; // Check if the user is verified
   
      localStorage.setItem("token", data.token);
      // Update the content of the placeholder element
      const messagePlaceholder = document.getElementById('messagePlaceholder');
      messagePlaceholder.textContent = message;
   
      if (data.token && is_staff) {
        if (is_admin) {
          // Redirect admin to an admin-specific page
          console.log('Redirecting to admin page');
          window.location.href = 'option/option.html';
        } else {
          // Redirect regular users to a regular user page
          console.log('Redirecting to regular user page');
          window.location.href = 'option/seating_arranger/home.html';
        }
      } else {
        console.error('Authentication failed or user is not verified by the admin:', data);
      }
   })
    .catch(error => {
      // Handle any errors
      console.error(error);
    });
}

function signUp() {
    var username = document.getElementById('username').value;
    var email = document.getElementById('email').value;
    var password1 = document.getElementById('password1').value;
    var password2 = document.getElementById('password2').value;

    // Create the JSON payload
    var jsonData = {
      username: username,
      email: email,
      password1: password1,
      password2:password2,
    };

    // Make the API request to the Django backend
    fetch('http://localhost:8000//api/sign-up/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(jsonData)
    })
      .then(response => response.json())
      .then(data => {
        // Handle the response from the Django backend
        console.log(data);
        const message = data.message;

        // Update the content of the placeholder element
        const messagePlaceholder = document.getElementById('messagePlaceholder');
        messagePlaceholder.textContent = message;
      })
      .catch(error => {
        // Handle any errors
        console.error(error);
      });

      signinForm.style.display = "block";
      signupForm.style.display = "none";
  }
  