/*
* Safari -- 
* This script was made with gpt and a little copilot for modifications
* I didn't use tutorials but I did use several reference sites to get inspiration 
* for the look and functionality of the timer 
* References used: https://pomofocus.io/
* https://studywithme.io/aesthetic-pomodoro-timer/
* https://www.tomatotimers.com/
*/





// Event listener to start the timer when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    let interval;
    let isRunning = false;
    let remaining = null; // To store remaining time when paused
    const display = document.querySelector('#timer-display');
    const durations = {
        pomodoro: 25 * 60,
        shortBreak: 5 * 60,
        longBreak: 10 * 60
    };
    let currentDuration = durations.pomodoro; // Default to Pomodoro

    // Function to start the timer
    function startTimer(duration) {
        let timer = remaining !== null ? remaining : duration;
        clearInterval(interval); // Clear any existing interval
        isRunning = true;
        interval = setInterval(function () {
            let minutes = parseInt(timer / 60, 10);
            let seconds = parseInt(timer % 60, 10);

            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;

            display.textContent = minutes + ":" + seconds;

            if (--timer < 0) {
                clearInterval(interval);
                if (currentDuration === durations.pomodoro) {
                    alert("Great work! Time for a break, lets go for a walk!");
                } else {
                    alert("Your doing great, let's get back to it!");
                }
                isRunning = false;
                remaining = null; // Reset remaining time
            } else {
                remaining = timer; // Store remaining time
            }
        }, 1000);
    }

    // Event listener for the start button
    document.querySelector('#start-button').addEventListener('click', function () {
        startTimer(currentDuration);
    });

    // Event listener for the stop button
    document.querySelector('#stop-button').addEventListener('click', function () {
        clearInterval(interval);
        isRunning = false;
    });

    // Event listener for the reset button
    document.querySelector('#reset-button').addEventListener('click', function () {
        clearInterval(interval);
        display.textContent = "25:00";
        isRunning = false;
        remaining = null; // Reset remaining time
        currentDuration = durations.pomodoro; // Reset to default Pomodoro time
    });

    // Event listener for the Pomodoro button
    document.querySelector('#pomodoro').addEventListener('click', function () {
        currentDuration = durations.pomodoro;
        display.textContent = "25:00";
        remaining = null; // Reset remaining time
        if (isRunning) {
            clearInterval(interval);
            startTimer(currentDuration); // Start new timer if one is running
        }
    });

    // Event listener for the Short Break button
    document.querySelector('#short-break').addEventListener('click', function () {
        currentDuration = durations.shortBreak;
        display.textContent = "05:00";
        remaining = null; // Reset remaining time
        if (isRunning) {
            clearInterval(interval);
            startTimer(currentDuration); // Start new timer if one is running
        }
    });

    // Event listener for the Long Break button
    document.querySelector('#long-break').addEventListener('click', function () {
        currentDuration = durations.longBreak;
        display.textContent = "10:00";
        remaining = null; // Reset remaining time
        if (isRunning) {
            clearInterval(interval);
            startTimer(currentDuration); // Start new timer if one is running
        }
    });
});