/*
* Safari --
* This was a mix of copilot and tutorial code cobbled together to make the app
* https://www.codingnepalweb.com/build-drawing-app-html-canvas-javascript/
* https://www.w3schools.com/graphics/canvas_drawing.asp
* I also prompted GPT to understand some of the styling / functionality etc
*/



/**
 * This script handles the drawing functionality of a canvas element.
 * It provides tools for drawing shapes, changing colors, and saving the canvas image.
 * The script uses event listeners to respond to user interactions with the canvas and tool buttons.
 * It also includes functions for drawing rectangles, circles, and triangles.
 * @file This file contains the JavaScript code for the drawing functionality.
 * @summary Handles the drawing functionality of a canvas element.
 * @since 1.0.0
 */
// Get the canvas element
const canvas = document.querySelector("canvas");

// Get the tool buttons
const toolButtons = document.querySelectorAll(".tool");

// Get the fill color checkbox
const fillColorCheckbox = document.querySelector("#fill-color");

// Get the size slider
const sizeSlider = document.querySelector("#size-slider");

// Get the color buttons
const colorButtons = document.querySelectorAll(".colors .option");

// Get the color picker
const colorPicker = document.querySelector("#color-picker");

// Get the clear canvas button
const clearCanvasButton = document.querySelector(".clear-canvas");

// Get the save image button
const saveImageButton = document.querySelector(".save-img");

// Get the 2D rendering context of the canvas
const ctx = canvas.getContext("2d");

// Variables for tracking previous mouse coordinates, drawing state, selected tool, brush width, and selected color
let prevMouseX, prevMouseY, snapshot;
let isDrawing = false;
let selectedTool = "brush";
let brushWidth = 5;
let selectedColor = "#000";

// Function to set the canvas background color
const setCanvasBackground = () => {
    ctx.fillStyle = "#fff";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = selectedColor;
}

// Set the canvas dimensions and background color when the window loads
window.addEventListener("load", () => {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
    setCanvasBackground();
});

// Function to draw a rectangle
const drawRect = (e) => {
    if (!fillColorCheckbox.checked) {
        return ctx.strokeRect(e.offsetX, e.offsetY, prevMouseX - e.offsetX, prevMouseY - e.offsetY);
    }
    ctx.fillRect(e.offsetX, e.offsetY, prevMouseX - e.offsetX, prevMouseY - e.offsetY);
}

// Function to draw a circle
const drawCircle = (e) => {
    ctx.beginPath();
    let radius = Math.sqrt(Math.pow((prevMouseX - e.offsetX), 2) + Math.pow((prevMouseY - e.offsetY), 2));
    ctx.arc(prevMouseX, prevMouseY, radius, 0, 2 * Math.PI);
    fillColorCheckbox.checked ? ctx.fill() : ctx.stroke();
}

// Function to draw a triangle
const drawTriangle = (e) => {
    ctx.beginPath();
    ctx.moveTo(prevMouseX, prevMouseY);
    ctx.lineTo(e.offsetX, e.offsetY);
    ctx.lineTo(prevMouseX * 2 - e.offsetX, e.offsetY);
    ctx.closePath();
    fillColorCheckbox.checked ? ctx.fill() : ctx.stroke();
}

// Function to start drawing
const startDraw = (e) => {
    isDrawing = true;
    prevMouseX = e.offsetX;
    prevMouseY = e.offsetY;
    ctx.beginPath();
    ctx.lineWidth = brushWidth;
    ctx.strokeStyle = selectedColor;
    ctx.fillStyle = selectedColor;
    snapshot = ctx.getImageData(0, 0, canvas.width, canvas.height);
}

/**
 * Handles the drawing functionality based on the selected tool.
 * @param {MouseEvent} e - The mouse event object.
 */
const drawing = (e) => {
    if (!isDrawing) return;
    ctx.putImageData(snapshot, 0, 0);

    if (selectedTool === "brush" || selectedTool === "eraser") {
        ctx.strokeStyle = selectedTool === "eraser" ? "#fff" : selectedColor;
        ctx.lineTo(e.offsetX, e.offsetY);
        ctx.stroke();
    } else if (selectedTool === "rectangle") {
        drawRect(e);
    } else if (selectedTool === "circle") {
        drawCircle(e);
    } else {
        drawTriangle(e);
    }
}

// Add event listeners to the tool buttons
toolButtons.forEach(btn => {
    btn.addEventListener("click", () => {
        document.querySelector(".options .active").classList.remove("active");
        btn.classList.add("active");
        selectedTool = btn.id;
    });
});

// Add event listener to the size slider
sizeSlider.addEventListener("change", () => brushWidth = sizeSlider.value);

// Add event listeners to the color buttons
colorButtons.forEach(btn => {
    btn.addEventListener("click", () => {
        document.querySelector(".options .selected").classList.remove("selected");
        btn.classList.add("selected");
        selectedColor = window.getComputedStyle(btn).getPropertyValue("background-color");
    });
});

// Add event listener to the color picker
colorPicker.addEventListener("change", () => {
    colorPicker.parentElement.style.background = colorPicker.value;
    colorPicker.parentElement.click();
});

// Add event listener to the clear canvas button
clearCanvasButton.addEventListener("click", () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    setCanvasBackground();
});

// Add event listener to the save image button
saveImageButton.addEventListener("click", () => {
    const link = document.createElement("a");
    link.download = `${Date.now()}.jpg`;
    link.href = canvas.toDataURL();
    link.click();
});

// Add event listeners for mouse events on the canvas
canvas.addEventListener("mousedown", startDraw);
canvas.addEventListener("mousemove", drawing);
canvas.addEventListener("mouseup", () => isDrawing = false);
