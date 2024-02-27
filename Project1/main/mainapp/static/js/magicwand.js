/*
* Made by safari
* Just one copilot prompt for the JS and the added couple lines of html for the base template
* Super simple no other resources needed
*/

// Event listener for when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    const facts = [
        // Array of facts about New College
        "New College was founded on October 11, 1960, as a private college.",
        "In 1961, trustees secured options to purchase the former Charles Ringling estate and 12 acres of airport land for the campus.",
        "The campus was dedicated on November 18, 1962, with soil from Harvard mixed with New College's as a symbol of shared ideals.",
        "The 'Blue Goose' bus transported students from the Landmark Hotel to New College in 1964.",
        "The charter class enrolled in 1964 and graduated in 1967.",
        "In 1969, the faculty adopted a contract system emphasizing individualized study plans and undergraduate research.",
        "Caples Campus was created in 1971 through a gift from Mr. and Mrs. Ralph Caples.",
        "New College joined the State University System in 1975 as part of the University of South Florida.",
        "The Sudakoff Conference Center on the Pei Campus opened in 1983.",
        "The New College Alumni Association was formed in 1985.",
        "A new library dedicated on November 1, 1986, later named for benefactor Jane Bancroft Cook.",
        "In 1988, USA Today listed New College among the 43 'choosiest' colleges in the nation.",
        "A new fitness center was constructed on the Pei Campus in 1990.",
        "Time magazine's Money Guide listed New College as the No.2 'Best College Buy' in 1993.",
        "The Betty Isermann Fine Arts Building broke ground in 1996 on the Caples campus.",
        "The Four Winds Café, a student-run coffee house, was established in 1998.",
        "The R.V. Heiser Natural Sciences Complex opened in 2000 with a $6.6 million investment.",
        "The Pritzker Marine Biology Research Center opened in 2001 with a $2.5 million investment.",
        "New College achieved independence as the 11th member of the State University System on July 1, 2001.",
        "In 2006, USF Sarasota-Manatee's relocation supported a bold new master plan for New College.",
        "Five new 'green' residence halls opened on East Campus in 2007.",
        "The Palm Court was restored with new palm trees in 2008.",
        "A 10-year Strategic/Academic Master Plan was approved in 2008 to guide academic changes.",
        "The Hamilton Student Center renovation in 2010 included a new Black Box Theater.",
        "New College celebrated its 50th anniversary with activities in 2011, including a stunning sunset on the Bayfront.",
        "The Academic Center (ACE) opened in 2011 with Gold LEED status for sustainability.",
        "A new seawall and esplanade were completed in 2012, enhancing the Bayfront area.",
        "Dr. Donal O’Shea was appointed as the College's fifth president in 2012.",
        "In 2013, a new bell tower was dedicated at President O’Shea's inauguration.",
        "The Cross College Alliance, formerly C4 Consortium, was renamed in 2017, including New College and other local institutions."
    ];

    // Event listener for when the magic-wand element is clicked
    document.querySelector('#magic-wand').addEventListener('click', function(e) {
        e.preventDefault(); // Prevent the default action
        const randomFact = facts[Math.floor(Math.random() * facts.length)]; // Get a random fact from the facts array
        alert(randomFact); // Display the random fact in an alert
    });
});
