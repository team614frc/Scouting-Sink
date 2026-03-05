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

async function serializeData()
{
    const fileHandle = await window.showSaveFilePicker({
        suggestedName: getName(),
        types: [
            {
                description: "JSON File",
                accept: { "application/json": [".json"]}
            }
        ]
    });

    const writable = await fileHandle.createWritable();

    await writable.write(JSON.stringify(data, null, 2));

    await writable.close();

    resetData()
}

function getName() { return COMPUTER_ID + "_" + new Date().toISOString().replace(/[:.]/g, "-") + ".json" }

function resetData()
{
    data = []
    localStorage.setItem("scoutingData", JSON.stringify(data))
}
