// Tunables
const COMPUTER_ID = "12345" // Change this to your computer's unique ID



let data = JSON.parse(localStorage.getItem("scoutingData")) || [];

document.getElementById("scoutingForm").addEventListener("submit", function(event) 
{ 
    event.preventDefault(); 
    
    const entry = {
        team_id: document.getElementById("Id").value,
        notes: document.getElementById("Notes").value
    }

    data.push(entry);
    localStorage.setItem("scoutingData", JSON.stringify(data))
    this.reset()

    serializeData()
})

document.getElementById("resetButton").addEventListener("click", resetData())

function serializeData()
{
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = getName()
    a.click()
    URL.revokeObjectURL(url)
    resetData()
}

function getName() { return COMPUTER_ID + "_" + new Date().toISOString().replace(/[:.]/g, "-") + ".json" }

function resetData()
{
    data = []
    localStorage.setItem("scoutingData", JSON.stringify(data))
}