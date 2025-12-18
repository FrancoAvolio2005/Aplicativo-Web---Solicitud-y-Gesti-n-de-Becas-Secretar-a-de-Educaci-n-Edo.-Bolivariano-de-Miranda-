const data = {
    "words": [
        {"english": "book", "spanish": ["libro", "cuaderno", "revista", "diario", "enciclopedia"]},
        {"english": "sun", "spanish": ["sol", "estrella", "luz", "brillo", "calor"]},
        {"english": "friend", "spanish": ["amigo", "compañero", "colega", "camarada", "socio"]},
        {"english": "computer", "spanish": ["computadora", "ordenador", "equipo", "máquina", "sistema"]},
        {"english": "school", "spanish": ["escuela", "colegio", "instituto", "academia", "universidad"]}
    ]
};

let correctCount = 0;
let incorrectCount = 0;

// Obtener una pregunta aleatoria con opciones incorrectas
function getRandomQuestion() {
    let shuffledWords = [...data.words].sort(() => Math.random() - 0.5);
    let selectedWord = shuffledWords[0];
    let correctAnswer = selectedWord.spanish[0];

    let allOptions = data.words.flatMap(word => word.spanish).filter(word => word !== correctAnswer);
    let wrongAnswers = allOptions.sort(() => Math.random() - 0.5).slice(0, 3);

    return { english: selectedWord.english, correct: correctAnswer, options: [...wrongAnswers, correctAnswer].sort(() => Math.random() - 0.5) };
}

// Mostrar la pregunta actual
function showQuestion() {
    if (correctCount === 5 || incorrectCount > 3) {
        evaluatePerformance();
        return;
    }

    const questionData = getRandomQuestion();
    document.getElementById("question").innerText = `¿Cuál es la traducción correcta de "${questionData.english}"?`;
    const optionsContainer = document.getElementById("options");
    optionsContainer.innerHTML = "";

    questionData.options.forEach(option => {
        let btn = document.createElement("button");
        btn.classList.add("btn");
        btn.innerText = option;
        btn.onclick = () => checkAnswer(option, questionData.correct);
        optionsContainer.appendChild(btn);
    });
}

// Verificar respuesta
function checkAnswer(selectedOption, correctAnswer) {
    if (selectedOption === correctAnswer) {
        correctCount++;
        document.getElementById("result").innerText = `✅ ¡Correcto!`;
    } else {
        incorrectCount++;
        document.getElementById("result").innerText = `❌ Incorrecto`;
    }

    document.querySelectorAll(".btn").forEach(btn => {
        btn.disabled = true;
        if (btn.innerText === correctAnswer) {
            btn.classList.add("correct");
        } else {
            btn.classList.add("incorrect");
        }
    });

    setTimeout(() => nextQuestion(), 1000);
}

// Evaluar desempeño
function evaluatePerformance() {
    const resultContainer = document.getElementById("result");
    const questionContainer = document.getElementById("question");
    const optionsContainer = document.getElementById("options");

    questionContainer.innerText = "¡Evaluación completada!";
    optionsContainer.innerHTML = "";
    if (incorrectCount > 3) {
        resultContainer.innerText = `😢 Tienes ${incorrectCount} respuestas incorrectas. No pasaste el examen, pero sigue intentándolo.`;
    } else if (correctCount >= 3) {
        resultContainer.innerText = `🎉 ¡Felicidades! Obtuviste ${correctCount} respuestas correctas. Pasaste el examen.`;
    } else {
        resultContainer.innerText = `😢 Obtuviste ${correctCount} respuestas correctas. No pasaste el examen, pero sigue intentándolo.`;
    }
}

// Siguiente pregunta
function nextQuestion() {
    document.getElementById("result").innerText = "";
    showQuestion();
}

// Ejecutar la primera pregunta al cargar la página
window.onload = showQuestion;