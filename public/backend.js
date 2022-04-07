async function list_online() {
  raw_response = await window.fetch("https://gsgtafelmanager.pythonanywhere.com/online")
  return raw_response.json()
}

async function is_online(id) {
  raw_response = await window.fetch("https://gsgtafelmanager.pythonanywhere.com/online/" + id)
  return raw_response.text() == "True"
}

async function send_command(id, data) {
  raw_response = await window.fetch("https://gsgtafelmanager.pythonanywhere.com/send/" + id, {"method":"POST","body": JSON.stringify(data)})
  response = await raw_response.json()
  return response
}
