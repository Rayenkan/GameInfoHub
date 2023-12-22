let nb = 6;


async function loadmore() {
    try {
        const pageData = String(nb);

        const response = await fetch("http://127.0.0.1:8080/loadmore", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                page_data: pageData,
            }),
        });
        if (nb >= 30) {
            document.getElementById("btn").disabled = true;
            document.getElementById("btn")
        }
        if (response.ok) {
            const dataReply = await response.json();
            console.log(dataReply);
            if (dataReply) {
                nb += 6;
            }
            const gamesContainer = document.getElementById('games-container');
            gamesContainer.innerHTML = ''; // Clear existing content
            for (const game of dataReply.games) {
                const item = document.createElement('div');
                item.className = 'item';
                item.onclick = function () {
                    openPopup(game.image_link, game.name, game.platforms, game.release_date, game.rating, game.tags);
                };

                const img = document.createElement('img');
                img.src = game.image_link;
                img.alt = '';

                item.appendChild(img);
                gamesContainer.appendChild(item);
            }


        } else {
            console.error(`Error: ${response.status} - ${response.statusText}`);
        }
    } catch (error) {
        console.error("Error:", error);
    }
}
async function search() {
    try {
        const pageData = document.getElementById("search").value;

        const response = await fetch("http://127.0.0.1:8080/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                page_data: pageData,
            }),
        });

        if (response.ok) {
            const dataReply = await response.json();

            // Check if there are games in the response
            if (dataReply && dataReply.length > 0) {
                const firstGame = dataReply[0];
                openPopup(firstGame.image_link, firstGame.name, firstGame.platforms, firstGame.release_date, firstGame.rating, firstGame.tags);
            } else {
                // Handle the case when no results are found
                console.log("No results found");
            }
        } else {
            document.getElementById("search").value = "Game Not Found !!"
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

function openPopup(imageSrc, name, platforms, rdate, rating, tags) {

    document.getElementById('popupImage').src = imageSrc;
    document.getElementById('popup').style.display = 'block';
    document.getElementById('overlay').style.display = 'block';
    document.querySelector(".name").innerText = name;
    document.querySelector(".releasedate").innerText = rdate;
    document.querySelector(".platforms").innerText = platforms;
    document.querySelector(".rating").innerText = rating;
    document.querySelector(".tags").innerText = tags;
}

function closePopup() {
    // Hide the popup and overlay
    document.getElementById('popup').style.display = 'none';
    document.getElementById('overlay').style.display = 'none';
}

