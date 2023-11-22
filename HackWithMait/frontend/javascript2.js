function castVote(party) {
    const voteButtons = document.querySelectorAll('.vote-btn');
    voteButtons.forEach(button => {
      button.disabled = true;
      button.classList.remove('voted');
    });
  
    const votedButton = document.querySelector(`.party h2:contains(${party}) + .vote-btn`);
    votedButton.disabled = false;
    votedButton.classList.add('voted');
  
    const votedMessage = document.querySelector('.voted-message');
    votedMessage.style.display = 'block';
    votedMessage.textContent = `Congratulations! You have voted for ${party}.`;
  }