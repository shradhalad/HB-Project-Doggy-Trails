
// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.2/firebase-app.js";
import { } from "https://www.gstatic.com/firebasejs/9.6.2/firebase-database.js"

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBJ_jXR1TINqhNS_0pHglPR8M_ktne45Ro",
  authDomain: "hb-capstone-project.firebaseapp.com",
  databaseURL: "https://hb-capstone-project-default-rtdb.firebaseio.com",
  projectId: "hb-capstone-project",
  storageBucket: "hb-capstone-project.appspot.com",
  messagingSenderId: "1002315091926",
  appId: "1:1002315091926:web:8a926354689df3c3051e77",
  measurementId: "G-H483V8D1L1"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
firebase.initializeApp(firebaseConfig);
// const db = getFirestore(app);
const db = firebase.database();

const fetchChat = db.ref("messages/");

fetchChat.on("child_added", function (snapshot) {
  const messages = snapshot.val();
  const timestamp = snapshot.key;
  const dateTime = new Date(Number.parseInt(timestamp)).toLocaleString();
  const message = `<li class=${getCookie('user_name') === messages.username ? "sent" : "receive"
    }><span><p>${messages.username}: ${messages.message} <br/>@ ${dateTime} </p></span></li>`;
  // append the message on the page
  document.getElementById("messages").innerHTML += message;
});

function sendMessage(e) {
  e.preventDefault();

  // get values to be submitted
  const timestamp = Date.now();
  const messageInput = document.getElementById("message-input");
  const message = messageInput.value;

  // clear the input box
  messageInput.value = "";

  //auto scroll to bottom
  document
    .getElementById("messages")
    .scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });

  // create db collection and send in the data
    
  var username = getCookie('user_name');
    
  db.ref("messages/" + timestamp).set({
    'username': username,
    'message': message,
    'timestamp': Date.now()
  });
}

document.getElementById("message-form").addEventListener("submit", sendMessage);

const getCookie = (name) => {
  const cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
    let c = cookies[i].trim().split('=');
    if (c[0] === name) {
      return c[1];
    }
  }
  return "";
}

