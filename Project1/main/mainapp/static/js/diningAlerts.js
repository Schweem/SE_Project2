// diningAlerts.js
document.addEventListener("DOMContentLoaded", function() {
    // Define meal times
    const mealTimes = {
        weekdays: {
            breakfast: { start: 8, end: 10, mealName: "Breakfast" },
            lunch: { start: 11, end: 13.5, mealName: "Lunch" },
            dinner: { start: 16.5, end: 19, mealName: "Dinner" }
        },
        weekends: {
            brunch: { start: 11, end: 13.5, mealName: "Brunch" },
            dinner: { start: 16.5, end: 18.5, mealName: "Dinner" }
        }
    };

    // Get the current time and day
    const now = new Date();
    const currentHour = now.getHours() + now.getMinutes() / 60;
    const currentDay = now.getDay(); // Sunday - 0, Monday - 1, ..., Saturday - 6

    // Determine if it's a weekday or weekend and select the appropriate meal times
    const todayMeals = currentDay >= 1 && currentDay <= 5 ? mealTimes.weekdays : mealTimes.weekends;

    // Check each meal time to see if we're within the serving window
    for (const meal in todayMeals) {
        const { start, end, mealName } = todayMeals[meal];

        const mealKey = `alertShownFor${mealName}${currentDay}`;
        const alertShown = localStorage.getItem(mealKey);

        if (currentHour >= start && currentHour <= end && !alertShown) {
            alert(`${mealName} is currently open and closes at ${formatTime(end)} today.`);
            localStorage.setItem(mealKey, 'true');
        }
    }
});

function formatTime(hourDecimal) {
    const hour = Math.floor(hourDecimal);
    const minutes = Math.round((hourDecimal - hour) * 60);
    return `${hour}:${minutes.toString().padStart(2, '0')}`;
}
