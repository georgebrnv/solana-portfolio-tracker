function toggleAnswer(id) {
  // Get all answer elements
  var answers = document.querySelectorAll('.answer');

  // Hide all answer elements except the one associated with the clicked question
  answers.forEach(function(answer) {
    if (answer.id === id) {
      // Toggle the display of the answer associated with the clicked question
      answer.style.display = (answer.style.display === 'none' || answer.style.display === '') ? 'block' : 'none';
    } else {
      answer.style.display = 'none';
    }
  });
}