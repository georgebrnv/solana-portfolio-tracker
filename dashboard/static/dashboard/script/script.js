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

// NFT CAROUSEL PORTFOLIO OBJECT
const nftAssets = [
    { title: "SOLANA NFT 1", imageUrl: "path/to/image1.jpg" },
    { title: "NFT 2", imageUrl: "path/to/image2.jpg" },
];

// Function to generate carousel items dynamically
function generateCarouselItems() {
    const carouselInner = document.querySelector(".carousel-nft-inner");

    // Clear existing carousel items
    carouselInner.innerHTML = "";

    // Loop through the NFT assets data
    nftAssets.forEach((asset, index) => {
        // Create carousel item
        const carouselItem = document.createElement("div");
        carouselItem.classList.add("carousel-item");
        if (index === 0) {
            carouselItem.classList.add("active");
        }

        // Create container div for the NFT asset
        const container = document.createElement("div");
        container.classList.add("container");

        // Create image element for the NFT asset
        const image = document.createElement("img");
        image.src = asset.imageUrl;
        image.alt = asset.title;
        image.classList.add("d-block", "w-50");

        // Append image to the container
        container.appendChild(image);

        // Append container to the carousel item
        carouselItem.appendChild(container);

        // Append carousel item to the carousel inner
        carouselInner.appendChild(carouselItem);
    });
}

// Call the function to generate carousel items
generateCarouselItems();


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