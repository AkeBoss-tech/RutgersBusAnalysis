const CSV_URL = "https://raw.githubusercontent.com/AkeBoss-tech/RutgersBusAnalysis/main/output/A_Route_stop.csv";

async function fetchCSV(url) {
    const response = await fetch(url);
    const text = await response.text();
    return parseCSV(text);
}

function parseCSV(csvText) {
    const rows = csvText.split("\n").filter(row => row.trim() !== "");
    const headers = rows.shift().split(",");
    return rows.map(row => {
        const values = row.split(",");
        return headers.reduce((acc, header, index) => {
            acc[header] = values[index];
            return acc;
        }, {});
    });
}

function populateBusSelector(data) {
    const busSelector = document.getElementById("busSelector");
    const busIDs = [...new Set(data.map(row => row.bus_id))];
    busIDs.forEach(busID => {
        const option = document.createElement("option");
        option.value = busID;
        option.textContent = busID;
        busSelector.appendChild(option);
    });

    busSelector.addEventListener("change", () => {
        const selectedBusID = busSelector.value;
        const filteredData = data.filter(row => row.bus_id === selectedBusID);
        updateIndividualBusChart(filteredData);
    });

    // Trigger initial chart
    if (busIDs.length > 0) {
        busSelector.value = busIDs[0];
        const initialData = data.filter(row => row.bus_id === busIDs[0]);
        updateIndividualBusChart(initialData);
    }
}

function updateIndividualBusChart(data) {
    const timestamps = data.map(row => row.timestamp);
    const loads = data.map(row => parseFloat(row.load) || 0);
    const stopTimes = data.map(row => parseFloat(row.time_waiting) || 0);

    const ctx = document.getElementById("individualBusChart").getContext("2d");
    new Chart(ctx, {
        type: "line",
        data: {
            labels: timestamps,
            datasets: [
                {
                    label: "Bus Load",
                    data: loads,
                    borderColor: "blue",
                    fill: false,
                },
                {
                    label: "Time Waiting at Stops",
                    data: stopTimes,
                    borderColor: "red",
                    fill: false,
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: "time",
                    time: {
                        unit: "minute"
                    },
                    title: {
                        display: true,
                        text: "Time"
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: "Value"
                    }
                }
            }
        }
    });
}

function createAllBusesChart(data) {
    const aggregated = {};
    data.forEach(row => {
        const timestamp = row.timestamp;
        if (!aggregated[timestamp]) {
            aggregated[timestamp] = { loadSum: 0, count: 0 };
        }
        aggregated[timestamp].loadSum += parseFloat(row.load) || 0;
        aggregated[timestamp].count++;
    });

    const timestamps = Object.keys(aggregated);
    const averageLoads = timestamps.map(ts => aggregated[ts].loadSum / aggregated[ts].count);

    const ctx = document.getElementById("allBusesChart").getContext("2d");
    new Chart(ctx, {
        type: "line",
        data: {
            labels: timestamps,
            datasets: [
                {
                    label: "Average Bus Load",
                    data: averageLoads,
                    borderColor: "green",
                    fill: false,
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: "time",
                    time: {
                        unit: "minute"
                    },
                    title: {
                        display: true,
                        text: "Time"
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: "Average Load"
                    }
                }
            }
        }
    });
}

function createAverageLoopTimeChart(data) {
    const times = {};
    data.forEach(row => {
        const hour = new Date(row.timestamp).getHours();
        if (!times[hour]) {
            times[hour] = { sum: 0, count: 0 };
        }
        const loopTime = parseFloat(row.time_to_complete) || 0;
        times[hour].sum += loopTime;
        times[hour].count++;
    });

    const hours = Object.keys(times).map(Number);
    const averageLoopTimes = hours.map(hour => times[hour].sum / times[hour].count);

    const ctx = document.getElementById("averageLoopTimeChart").getContext("2d");
    new Chart(ctx, {
        type: "bar",
        data: {
            labels: hours.map(h => `${h}:00`),
            datasets: [
                {
                    label: "Average Loop Time",
                    data: averageLoopTimes,
                    backgroundColor: "orange",
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: "Hour of Day"
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: "Average Loop Time (seconds)"
                    }
                }
            }
        }
    });
}

// Main function
(async function main() {
    const data = await fetchCSV(CSV_URL);
    populateBusSelector(data);
    createAllBusesChart(data);
    createAverageLoopTimeChart(data);
})();
