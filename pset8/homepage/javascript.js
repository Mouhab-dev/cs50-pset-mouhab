function sayhello()
{
  let name = document.querySelector("#textbox").value;
  if (name === ""){
    alert("The textbox field is empty, please type your name again");
  }
    alert("Hello, "+ name + "!");
}

// Dark mode button
document.querySelector('#dark-bt').onclick = function(){
  document.querySelector('#navbar').style.backgroundColor = 'black';
  document.querySelector('#navbarDropdown').style.color = 'white';
  document.querySelector('#title').style.color = 'white';
  document.querySelector('#home').style.color = 'white';
};

// Light mode button
document.querySelector('#light-bt').onclick = function(){
  document.querySelector('#navbar').style.backgroundColor = 'white';
  document.querySelector('#navbarDropdown').style.color = 'black';
  document.querySelector('#title').style.color = 'black';
  document.querySelector('#home').style.color = 'black';
};