document.getElementById("resumeForm").onsubmit = async function(e){

e.preventDefault()

let formData = new FormData(this)

try{

let response = await fetch("http://127.0.0.1:8000/analyze",{
method:"POST",
body:formData
})

let data = await response.json()

document.getElementById("result").textContent =
JSON.stringify(data,null,2)

}catch(error){

document.getElementById("result").textContent =
"Error connecting to backend"

console.error(error)

}

}