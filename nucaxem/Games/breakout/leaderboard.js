const leaderboardList = document.getElementById("leaderboardList");

// For demo purposes: using localStorage
function saveScore(score) {
  let leaderboard = JSON.parse(localStorage.getItem("leaderboard")) || [];
  let name = prompt("Enter your name for the leaderboard") || "Anonymous";
  leaderboard.push({ name, score });
  leaderboard.sort((a,b) => b.score - a.score);
  if(leaderboard.length > 10) leaderboard = leaderboard.slice(0,10);
  localStorage.setItem("leaderboard", JSON.stringify(leaderboard));
  updateLeaderboard();
}

function updateLeaderboard() {
  let leaderboard = JSON.parse(localStorage.getItem("leaderboard")) || [];
  leaderboardList.innerHTML = "";
  leaderboard.forEach(entry => {
    const li = document.createElement("li");
    li.textContent = `${entry.name} - ${entry.score}`;
    leaderboardList.appendChild(li);
  });
}

// Load leaderboard on page load
updateLeaderboard();
