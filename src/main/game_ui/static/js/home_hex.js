let size = 5;
let player = 1;
let gamemode = 1;

function changeBoardSize(newSize) {
    size = newSize;
}

function selectGamemode(selectedGamemode) {
    gamemode = selectedGamemode;
}

function startGame() {
    submitForm(gamemode);
}

function submitForm(formNumber) {
    if (formNumber === 1) {
        document.getElementById('size_input_1').value = size;
        document.querySelector('form[action="/game_hex"]').submit();
    } else if (formNumber === 2) {
        document.getElementById('player').value = player;
        document.getElementById('size_input_2').value = size;
        document.querySelector('form[action="/game_hexia"]').submit();
    } else if (formNumber === 3) {
        document.getElementById('size_input_3').value = size;
        document.querySelector('form[action="/game_hexiaia"]').submit();
    } else if (formNumber === 4) {
        document.getElementById('playerMCTS').value = player;
        document.getElementById('size_input_4').value = size;
        document.querySelector('form[action="/game_mcts_hexia"]').submit();
    } else if (formNumber === 5) {
        document.getElementById('size_input_5').value = size;
        document.querySelector('form[action="/game_mcts_hexiaia"]').submit();
    }
}

function player_red() {
    document.getElementById("button_red").classList.add("selected_2")
    document.getElementById("button_blue").classList.remove("selected_2")
    player = 2;
}

function player_blue() {
    document.getElementById("button_red").classList.remove("selected_2")
    document.getElementById("button_blue").classList.add("selected_2")
    player = 1;
}


function back() {
    window.location.href = '/';
}

// ========== fenetre regles ==================================

const openModalBtn = document.getElementById('reglesBtn');
const modal = document.getElementById('modal');
const closeBtn = document.getElementsByClassName('close')[0];

// Fonction pour ouvrir la fenêtre regles
openModalBtn.onclick = function() {
    modal.style.display = 'block';
}

// Fonction pour fermer la fenêtre modale lorsque l'utilisateur clique sur le bouton de fermeture (×)
closeBtn.onclick = function() {
    modal.style.display = 'none';
}

// Fermer la fenêtre modale si l'utilisateur clique en dehors de la fenêtre modale
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

const sizeButtons = document.querySelectorAll(".size_buttons > button")
sizeButtons.forEach(button => {
    button.addEventListener("click", () => { 
        sizeButtons.forEach(b => b.classList.remove("selected"));
        button.classList.add("selected");
     });
});

const modeButtons = document.querySelectorAll(".gamemode_buttons > button")
modeButtons.forEach(button => {
    button.addEventListener("click", () => { 
        modeButtons.forEach(b => b.classList.remove("selected"));
        button.classList.add("selected");
     });
});