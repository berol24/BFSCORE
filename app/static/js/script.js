const select = document.getElementById("season-select");
const btn = document.getElementById("btn");

btn.addEventListener("submit", (e) => {
  e.preventDefault();
});

for (let i = 1993; i <= 2016; i++) {
  const option = document.createElement("option");
  option.value = `${i}`;
  option.textContent = `${i}`;
  select.appendChild(option);
}

function showTab(tabId) {
  var contents = document.querySelectorAll(".tab-content");
  contents.forEach(function (content) {
    content.classList.remove("active");
  });

  var tabs = document.querySelectorAll(".info-tabs li");
  tabs.forEach(function (tab) {
    tab.classList.remove("active");
  });

  document.getElementById(tabId).classList.add("active");
  document.querySelector(".tab-" + tabId).classList.add("active");
}

// document.addEventListener("DOMContentLoaded", () => {
//   console.log("Page loaded and script running");
//   const loadMoreButton = document.getElementById("load-more");
//   let offset = parseInt(loadMoreButton.getAttribute("data-offset"), 10);
//   const year = new URLSearchParams(window.location.search).get("annee") || 1993;

//   loadMoreButton.addEventListener("click", () => {
//     console.log(`Loading more matches: offset=${offset}, year=${year}`);

//     fetch(`/load_more?year=${year}&offset=${offset}`)
//       .then((response) => response.json())
//       .then((data) => {
//         console.log("Matches loaded:", data.matches);

//         const matchList = document.getElementById("match-list");
//         data.matches.forEach((match) => {
//           const matchItem = document.createElement("li");
//           matchItem.classList.add("match-item");
//           matchItem.onclick = () =>
//             (window.location.href = `/info/${match.Match_ID}`);
//           matchItem.innerHTML = `
//             <div class="flex">
//               <ion-icon name="star-outline"></ion-icon>
//               <div class="match-time">Terminé</div>
//             </div>
//             <div class="match-details">
//               <div class="home-team">
//                 <div class="wrap-team">
//                   <img src="https://placehold.jp/18x18.png" alt="" />
//                   <p>${match.HomeTeam}</p>
//                 </div>
//               </div>
//               <div class="score">
//                 <p>${match.FTHG}</p>
//                 <span style="margin: 0 30px;">-</span>
//                 <p>${match.FTAG}</p>
//               </div>
//               <div class="away-team">
//                 <div class="wrap-team">
//                   <p>${match.AwayTeam}</p>
//                   <img src="https://placehold.jp/18x18.png" alt="" />
//                 </div>
//               </div>
//             </div>
//           `;
//           matchList.appendChild(matchItem);
//         });
//         offset += 20;
//         loadMoreButton.setAttribute("data-offset", offset);
//       })
//       .catch((error) => console.error("Error loading more matches:", error));
//   });
// });



document.addEventListener("DOMContentLoaded", () => {
  console.log("Page loaded and script running");
  
  const loadMoreButton = document.getElementById("load-more");
  const loadMoinsButton = document.getElementById("load-moins");
  
  let offset = parseInt(loadMoreButton.getAttribute("data-offset"), 10);
  const year = new URLSearchParams(window.location.search).get("annee") || 1993;

  const loadMatches = (increment) => {
    console.log(`Loading matches: offset=${offset}, year=${year}`);

    fetch(`/load_more?year=${year}&offset=${offset}`)
      .then((response) => response.json())
      .then((data) => {
        console.log("Matches loaded:", data.matches);

        const matchList = document.getElementById("match-list");

        if (increment < 0) {
          // Remove elements when loading less
          for (let i = 0; i < Math.abs(increment); i++) {
            if (matchList.lastChild) {
              matchList.removeChild(matchList.lastChild);
            }
          }
        } else {
          // Add new elements when loading more
          data.matches.forEach((match) => {
            const matchItem = document.createElement("li");
            matchItem.classList.add("match-item");
            matchItem.onclick = () =>
              (window.location.href = `/info/${match.Match_ID}`);
            matchItem.innerHTML = `
              <div class="flex">
                <ion-icon name="star-outline"></ion-icon>
                <div class="match-time">Terminé</div>
              </div>
              <div class="match-details">
                <div class="home-team">
                  <div class="wrap-team">
                    <img src="https://placehold.jp/18x18.png" alt="" />
                    <p>${match.HomeTeam}</p>
                  </div>
                </div>
                <div class="score">
                  <p>${match.FTHG}</p>
                  <span style="margin: 0 30px;">-</span>
                  <p>${match.FTAG}</p>
                </div>
                <div class="away-team">
                  <div class="wrap-team">
                    <p>${match.AwayTeam}</p>
                    <img src="https://placehold.jp/18x18.png" alt="" />
                  </div>
                </div>
              </div>
            `;
            matchList.appendChild(matchItem);
          });
        }

        offset += increment;
        if (offset < 0) offset = 0; // Ensure offset doesn't go negative
        
        loadMoreButton.setAttribute("data-offset", offset);
        loadMoinsButton.setAttribute("data-offset", offset);
      })
      .catch((error) => console.error("Error loading matches:", error));
  };

  loadMoreButton.addEventListener("click", () => loadMatches(20));
  loadMoinsButton.addEventListener("click", () => loadMatches(-20));
});









