

let timeRemaining = 30; // Total game time in seconds
let score = 0;

// Get the query parameters from the URL
const urlParams = new URLSearchParams(window.location.search);
const selectedLanguage = urlParams.get('language');
const category = urlParams.get('category');
const apiUrl = `language-game?language=${selectedLanguage}&category=${category}`;



// Map of languages to flag image paths
const flagImages = {
    italian: 'images/flags/italy.png',
    german: 'images/flags/germany.png',
    spanish: 'images/flags/spain.png',
    french: 'images/flags/france.png',
    english: 'images/flags/english.png'
};

// Update the flag image based on the selected language
const flagImageElement = document.getElementById('flagImage');

if (selectedLanguage && flagImages[selectedLanguage]) {
    flagImageElement.src = flagImages[selectedLanguage];
    flagImageElement.alt = `${selectedLanguage} flag`;
} else {
    console.error('Invalid or missing language selection');
    flagImageElement.style.display = 'none'; // Hide the flag image if no valid selection
}

//function display flag
function displayFlag() {
    const urlParams = new URLSearchParams(window.location.search);
    const selectedLanguage = urlParams.get('language');
    console.log('Selected Language:', selectedLanguage);
    const imageFlagPlaceholder = document.getElementById("gameFlagImage");
    if (selectedLanguage && flagImages[selectedLanguage]) {
        console.log('Flag Image URL:', flagImages[selectedLanguage]);
        imageFlagPlaceholder.src = flagImages[selectedLanguage];
        imageFlagPlaceholder.alt = `${selectedLanguage} flag`;
    } else {
        console.error('Invalid or missing language selection');
        imageFlagPlaceholder.style.display = 'none'; // Hide the flag image if no valid selection
    }
}

// Initialize score display
function updateScore() {
    document.getElementById('score').textContent = `Score: ${score}`;
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

const timerElement = document.getElementById('time-remaining');
// Function to update the timer every second
function startTimer() {
    const timerInterval = setInterval(() => {
        timeRemaining--;
        timerElement.textContent = timeRemaining;

        // When the timer reaches 0, stop the game
        if (timeRemaining <= 0) {
            clearInterval(timerInterval);
            endGame();
        }
    }, 1000);
}

// Assuming you have a function to play the word
function playAudio() {
    // Play audio
    if (timeRemaining > 0) {

    const audioPlayer = document.getElementById('audioPlayer');
    audioPlayer.play().catch(error => console.error('Audio play failed:', error));
    }
}
  

  

// Fetch data and start the game
function startGame() {
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            const category = data.category;
            const correctImage = data.correctImage;
            const incorrectImages = data.incorrectImages;
            const word = data.word;
            const audioUrl = data.audioUrl;

            // Display the word
            document.getElementById('word').textContent = word;

            // Play audio
            const audioPlayer = document.getElementById('audioPlayer');
            audioPlayer.src = `audio/${category}/${audioUrl}`;
            audioPlayer.play().catch(error => console.error('Audio play failed:', error));

            // Prepare image tiles
            const imageURLPrefix = `images/${category}/`;
            const imageContainer = document.getElementById('images');
            const imageUrls = [
                `${imageURLPrefix}${correctImage}`,
                ...incorrectImages.map(img => `${imageURLPrefix}${img}`),
            ];

            const shuffledImages = imageUrls.sort(() => Math.random() - 0.5);
            imageContainer.innerHTML = '';

            shuffledImages.forEach((imgUrl, index) => {
                const imgTile = document.createElement('img');
                imgTile.src = imgUrl;
                imgTile.alt = `Image ${index + 1}`;
                imgTile.className = 'image-tile';
                imgTile.onclick = () => handleImageClick(imgTile, imgUrl, `${imageURLPrefix}${correctImage}`);
                imageContainer.appendChild(imgTile);
            });

            // Hide result message and new game button
            document.getElementById('resultMessage').style.display = 'none';
            document.getElementById('newGameButton').style.display = 'none';
        })
        .catch(error => console.error('Error fetching API data:', error));
}

// Handle image tile click
function handleImageClick(tile, clickedImageUrl, correctImageUrl) {
    const resultMessage = document.getElementById('resultMessage');
    const newGameButton = document.getElementById('newGameButton');
    const correctAudio = document.getElementById('audioCorrect');
    const incorrectAudio = document.getElementById('audioIncorrect');


    if (clickedImageUrl === correctImageUrl) {
        correctAudio.play().catch(error => console.error('Audio play failed:', error));
        resultMessage.textContent = 'Correct! 🎉';
        resultMessage.className = 'result-message success';
        tile.style.borderColor = '#4CAF50'; // Green
        tile.style.borderWidth = '10px';
        score++;
    } else {
        incorrectAudio.play().catch(error => console.error('Audio play failed:', error));
        resultMessage.textContent = 'Incorrect! 😢';
        resultMessage.className = 'result-message error';
        tile.style.borderColor = 'red';
        tile.style.borderWidth = '10px';
    }

    if (timeRemaining > 0) {
        updateScore();
    

        // Disable further clicks and hover effect
        const tiles = document.querySelectorAll('.image-tile');
        //document.querySelectorAll('.image-tile').forEach(tile => (tile.onclick = null));
        tiles.forEach(tile => {
            tile.onclick = null; // Disable clicks
            tile.classList.add('no-hover'); // Add class to disable hover effect
        });
        resultMessage.style.display = 'block';
        //newGameButton.style.display = 'block';
        //check if timer > 0 then restart game
    
        sleep(1000).then(() => { startGame(); });
    } 
}

// Initialize the app
function initializeApp() {
    timeRemaining = 30; // Total game time in seconds
    score = 0;
    document.getElementById('startScreen').style.display = 'none';
    document.getElementById('gameArea').style.display = 'block';
    displayFlag();
    startGame();
    startTimer();
}

// Function to handle end-of-game logic
function endGame() {
    //alert('Time is up! Game over.');
    // Add any other logic to handle the end of the game
    // e.g., showing the final score or restarting the game
    const resultMessage = document.getElementById('resultMessage');
    resultMessage.textContent = `Final Score: ${score}`;
    resultMessage.className = 'result-message final';
    // Disable further clicks and hover effect
    const tiles = document.querySelectorAll('.image-tile');
    //document.querySelectorAll('.image-tile').forEach(tile => (tile.onclick = null));
    tiles.forEach(tile => {
        tile.onclick = null; // Disable clicks
        tile.classList.add('no-hover'); // Add class to disable hover effect
    });
    resultMessage.style.display = 'block';
    newGameButton.style.display = 'block';
}

// Event listeners
document.getElementById('startButton').addEventListener('click', initializeApp);
document.getElementById('newGameButton').addEventListener('click', initializeApp);
document.getElementById("repeatAudioButton").addEventListener("click", playAudio);
document.getElementById("home-button-img").addEventListener("click", () => {
    window.location.href = "index.html";
  });