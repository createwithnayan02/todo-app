const ctx = document.getElementById("weeklyChart");

new Chart(ctx, {
    type: "line",
    data: {
        labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        datasets: [
            {
                label: "This Week",
                data: thisWeekChart,
                borderColor: "#3b82f6",
                backgroundColor: "#3b82f6",
                tension: 0.4,
                fill: false
            },
            {
                label: "Last Week",
                data: lastWeekChart,
                borderColor: "#ef4444",
                backgroundColor: "#ef4444",
                tension: 0.4,
                fill:false
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: "Tasks"
                }
            },
            x: {
                title: {
                    display: true,
                    text: "Days"
                }
            }
        }
    }
});

const categoryctx = document.getElementById("categoryChart");

console.log(categoryctx);
console.log(categoryChart);

new Chart(categoryctx, {
    type: "bar",
    data: {
        labels: [
            "Learning",
            "Work",
            "Personal",
            "Health",
            "Shopping",
            "Hobby",
            "Finance",
            "Meeting",
            "Design",
            "Special Event",
            "Other"
        ],
        datasets: [{
            label: "Number of Tasks",
            data: categoryChart,
            borderWidth: 1,
            backgroundColor: "#4F46E5",
            borderColor: "#4338CA",
            borderRadius: 8,
            borderSkipped: false,
            barPercentage: 0.7,
            categoryPercentage: 0.8,
        }]
    },

    options: {
        responsive: true,
        maintainAspectRatio: false,

        plugins: {
            legend: {
                display: true
            }
        },

        scales: {
            x: {
                
                ticks:{
                        maxRotation:0,
                        minRotation:0,
                        autoSkip:false,
                font:{
                            size:11
                        }
                    },
                title: {
                    display: true,
                    text: "Categories"
                },
                grid: {
                color: "rgba(0,0,0,0.06)"
            }
            },

            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: "Tasks"
                },
                grid: {
                color: "rgba(0,0,0,0.06)"
}
            }
        }
    }
});