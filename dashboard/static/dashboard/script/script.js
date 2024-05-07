const popupContainer = document.getElementById('popupContainer');

// POP-UP WINDOW FUNCTIONS
function openPopup() {
    if (popupContainer) {
        popupContainer.style.display = 'block';
    }
}

function closePopup() {
    if (popupContainer) {
        popupContainer.style.display = 'none';
    }
}

// Navbar "Connect Wallet" button
const connectWalletBtn = document.getElementById('connectWalletBtnNavbar');
if (connectWalletBtn) {
    connectWalletBtn.addEventListener('click', openPopup);
}


// FAQ SECTION TOGGLE
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


// SCROLL DOWN TO AN ELEMENT ON CLICK
function scrollToElement(elementId) {
    var element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: "smooth" });
    }
}


// NAVBAR SCROLL BEHAVIOR
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


// NFT CAROUSEL ASSETS
const nftData = verifiedNFTs

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

// CREATE NFT CARD ELEMENTS FUNCTIONS
function createNFTCard(nft) {
    const card = document.createElement('div');
    card.classList.add('card', 'nft-carousel-card');

    const wrapper = document.createElement('div')
    wrapper.classList.add('square-image')

    const img = document.createElement('img');
    img.src = nft.imgUrl;
    img.classList.add('card-img-top', 'carousel-nft-img');

    const cardBody = document.createElement('div');
    cardBody.classList.add('card-body');

    const title = document.createElement('h5');
    title.classList.add('nft-card-title');
    title.textContent = nft.title;

    const currencies = document.createElement('div');
    currencies.classList.add('justify-content-between');

    const sol_currency = document.createElement('div');
    sol_currency.innerHTML = `<span class="badge bg-solana text-white mr-1">${nft.sol_currency.name}</span><span class="price">${nft.sol_currency.price}</span>`;

    const usdc_currency = document.createElement('div');
    usdc_currency.innerHTML = `<span class="badge bg-success text-white mr-1">${nft.usdc_currency.name}</span><span class="price">${nft.usdc_currency.price}</span>`;

    currencies.append(sol_currency, usdc_currency);
    cardBody.append(title, currencies);
    card.append(wrapper, cardBody);
    wrapper.append(img);

    return card;
}

// Render NFT cards
renderNFTCards();



