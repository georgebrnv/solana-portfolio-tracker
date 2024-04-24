


// FAQ section toggle
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


// Click to scroll down to an element
function scrollToElement(elementId) {
    var element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: "smooth" });
    }
}


// Navbar scroll behavior
let lastScrollTop = 0;
const navbar = document.querySelector('.nav-bar');

window.addEventListener('scroll', () => {
    let scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    if (scrollTop > lastScrollTop) {
        // Scroll down
        navbar.style.top = `-${navbar.offsetHeight}px`; // Hide navbar
    } else {
        // Scroll up
        navbar.style.top = 0; // Show navbar
    }

    lastScrollTop = scrollTop;
});


// Pop-up Add Wallet window
const addWalletBtnNavbar = document.getElementById('addWalletBtnNavbar');
const addWalletBtnProfile = document.getElementById('addWalletBtnProfile');
const popupContainer = document.getElementById('popupContainer');

addWalletBtnNavbar.addEventListener('click', () => {
    popupContainer.style.display = 'block';
});

addWalletBtnProfile.addEventListener('click', () => {
    popupContainer.style.display = 'block';
});

function closePopup() {
    popupContainer.style.display = 'none';
}

function saveWallet() {
    const walletInput = document.getElementById('walletInput').value;
    // Perform any action with the wallet input here
    console.log('Wallet address:', walletInput);
    closePopup();
}


// NFT Carousel assets
const nftData = [
    {
        imgUrl: "https://lh3.googleusercontent.com/nsZk2m9zkO3-fakZRYaXpqVSAFMS3fewSlKS-GhTwTbNEnZVrtymCAc-tuciJrEitgXqA4sUTj6dNtgQ2lljIZOkp-nlbtWmlA",
        title: "Backpack T-Shirt",
        description: "",
        currency1: { name: "SOL", price: 0.5 },
        currency2: { name: "$", price: 100 }
    },
    {
        imgUrl: "https://lh3.googleusercontent.com/yHCGA39S7d5AHCbHKY9g1j4gjU57SUFhyPL9Ph855JGTkWVYaHpZAmcdhnWc1TsZW7tP2XSUtxY4m2_CubJ5LUB5oeslfWSeIFk=k",
        title: "Backpack Surf",
        description: "",
        currency1: { name: "SOL", price: 0.25 },
        currency2: { name: "$", price: 50 }
    },
    {
        imgUrl: "https://lh3.googleusercontent.com/553o-snGZrBwiyalIG_qchkn5Yz5TEuOqBb2EnPYTRCucLGY5lmtSLCXtY7Qyu1S9FZkaZgVkVGLKKJE2CjvY6xEUOnMQqQiCg",
        title: "Backpack Surf",
        description: "",
        currency1: { name: "SOL", price: 0.25 },
        currency2: { name: "$", price: 50 }
    },
    {
        imgUrl: "https://lh3.googleusercontent.com/WOHTwAZMwuQdyLKwsypd2a_DzcPOE1OVlwfV8fegeOWwd4E0ApYsMGbSkh2uZviCETNyttJM7g_-7l9gTrP3NlOapzO9f1KRpA",
        title: "Backpack Surf",
        description: "",
        currency1: { name: "SOL", price: 0.25 },
        currency2: { name: "$", price: 50 }
    },
    {
        imgUrl: "https://lh3.googleusercontent.com/detHgC43iIiwrlClFQ5E6t-rMuZdPj7u9tlQfXtcGgkyA6x6Irm2EAvBIDBWShEzAq0y9-TSwOl4HcrIsCY76-7RFkd9ZXaTFw",
        title: "Backpack Surf",
        description: "",
        currency1: { name: "SOL", price: 0.25 },
        currency2: { name: "$", price: 50 }
    }
];

function renderNFTCards() {
    const cardBody = document.querySelector('.card-body');
    let numCardsPerPage;

    function updateCardsPerPage() {
        const cardBodyWidth = cardBody.offsetWidth;
        const screenWidth = window.innerWidth;
        if (screenWidth > 1200) {
            numCardsPerPage = 3;
            cardWidth = 'calc(100% / 3.2 - 1rem)'
        } else if (screenWidth > 575) {
            numCardsPerPage = 3;
            cardWidth = 'calc(100% / 2.9 - 1rem)'
        } else if (screenWidth > 400) {
            numCardsPerPage = 2;
            cardWidth = 'calc(100% / 2.15 - 1rem)'
        } else {
            numCardsPerPage = 1;
            cardWidth = 'calc(100% / 1.2 - 1rem)'
        }

        // Remove existing carousel items and indicators
        const carouselInner = document.getElementById('carouselInner');
        carouselInner.innerHTML = '';

        const carouselIndicators = document.getElementById('carouselIndicators');
        carouselIndicators.innerHTML = '';

        // Calculate the number of carousel items needed
        const numCarouselItems = Math.ceil(nftData.length / numCardsPerPage);

        for (let i = 0; i < numCarouselItems; i++) {
            const carouselItem = document.createElement('div');
            carouselItem.classList.add('carousel-item', 'px-3');
            if (i === 0) {
                carouselItem.classList.add('active');
            }

            // Render NFT cards for this carousel item
            const rowContainer = document.createElement('div');
            rowContainer.classList.add('d-flex', 'justify-content-between', 'flex-wrap');
            rowContainer.setAttribute('id', 'rowContainer');

            for (let j = i * numCardsPerPage; j < (i + 1) * numCardsPerPage && j < nftData.length; j++) {
                const nft = nftData[j];
                const card = createNFTCard(nft);
                card.style.width = cardWidth;
                rowContainer.appendChild(card);
            }

            // Center the row container if there's only one card and screen width is less than 375px
            if (screenWidth <= 400) {
                carouselItem.classList.add('carousel-item-400');
                carouselItem.classList.remove('px-3')
            }

            carouselItem.appendChild(rowContainer);
            carouselInner.appendChild(carouselItem);

            // Create indicators
            const indicator = document.createElement('button');
            indicator.setAttribute('type', 'button');
            indicator.setAttribute('data-bs-target', '#myCarousel');
            indicator.setAttribute('data-bs-slide-to', i.toString());
            indicator.setAttribute('aria-label', `Slide ${i + 1}`);
            if (i === 0) {
                indicator.classList.add('active');
            }
            carouselIndicators.appendChild(indicator);
        }

        // Get all carousel items
        const rowContainers = document.querySelectorAll('#rowContainer');

        // Iterate through each carousel item
        rowContainers.forEach(rowContainer => {
            // Get all card divs within the current carousel item
            const cards = rowContainer.querySelectorAll('.card');

            // Check if there are exactly 2 card divs
            if (cards.length === 2) {
                // Add the 'center-2' class to the carousel item
                rowContainer.classList.add('center-2');
                rowContainer.classList.remove('justify-content-between')
            }
        });
    }

    // Initial render
    updateCardsPerPage();

    // Update on window resize
    window.addEventListener('resize', updateCardsPerPage);
}

// Function to create an NFT card element
function createNFTCard(nft) {
    const card = document.createElement('div');
    card.classList.add('card', 'nft-carousel-card');

    const img = document.createElement('img');
    img.src = nft.imgUrl;
    img.classList.add('card-img-top', 'carousel-nft-img');

    const cardBody = document.createElement('div');
    cardBody.classList.add('card-body');

    const title = document.createElement('h5');
    title.classList.add('nft-card-title');
    title.textContent = nft.title;

    const description = document.createElement('div');
    description.classList.add('text-white');
    description.innerHTML = `<p>${nft.description}</p>`;

    const currencies = document.createElement('div');
    currencies.classList.add('d-flex', 'justify-content-between');

    const currency1 = document.createElement('div');
    currency1.innerHTML = `<span class="badge bg-success text-white">${nft.currency1.name}</span><span class="price">${nft.currency1.price}</span>`;

    const currency2 = document.createElement('div');
    currency2.innerHTML = `<span class="badge bg-primary text-white">${nft.currency2.name}</span><span class="price">${nft.currency2.price}</span>`;

    currencies.append(currency1, currency2);
    cardBody.append(title, description, currencies);
    card.append(img, cardBody);

    return card;
}

// Render NFT cards
renderNFTCards();

// Add event listener for window resize to update the carousel dynamically
window.addEventListener('resize', renderNFTCards);


