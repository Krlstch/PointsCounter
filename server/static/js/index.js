function setScores() {
    const httpRequest = new XMLHttpRequest()
    httpRequest.onreadystatechange = () => {
        if (httpRequest.readyState === 4) {
            var response = JSON.parse(httpRequest.responseText)
            document.getElementById("score1").textContent = response["score1"]
            document.getElementById("score2").textContent = response["score2"]
        }
    }
    httpRequest.open("GET", "./points", true)
    httpRequest.setRequestHeader("Cache-Control", "no-cache")
    httpRequest.send()
}

setInterval(setScores, 1000)