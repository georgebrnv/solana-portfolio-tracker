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

function scrollToElement(elementId) {
    var element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: "smooth" });
    }
}

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
        } else if (screenWidth > 575) {
            numCardsPerPage = 3;
        } else if (screenWidth > 375) {
            numCardsPerPage = 2;
        } else {
            numCardsPerPage = 1;
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

            for (let j = i * numCardsPerPage; j < (i + 1) * numCardsPerPage && j < nftData.length; j++) {
                const nft = nftData[j];
                const card = createNFTCard(nft);
                rowContainer.appendChild(card);
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
    card.style.width = 'calc(100% / 3.2 - 1rem)';

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