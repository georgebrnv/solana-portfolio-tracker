document.addEventListener('DOMContentLoaded', async function() {
    const connectButton = document.getElementById('connectWalletBtn');
    const disconnectButton = document.getElementById('disconnectWalletBtn');
    const navbarConnectButton = document.getElementById('connectWalletBtnNavbar');
    const logoutButton = document.getElementById('logoutBtn');

    connectButton.addEventListener('click', async () => {
        try {
            // Connect to Phantom wallet
            const wallet = await window.solana.connect();
            console.log('Connected to Phantom wallet:', wallet.publicKey.toString());

            // Store wallet connection information in local storage
            localStorage.setItem('walletConnected', 'true');

            // Send wallet info
            await sendWalletInfo(wallet.publicKey.toString());

            if (popupContainer) {
                popupContainer.style.display = 'none';
            }

            // Update UI
            navbarConnectButton.style.display = 'none';
            connectButton.style.display = 'none';
            disconnectButton.style.display = 'inline-block';

        } catch (error) {
            console.error('An error occurred while connecting your wallet:', error);
        }
    });

    disconnectButton.addEventListener('click', async () => {
        try {
            // Disconnect Phantom wallet
            await window.solana.disconnect();
            console.log('Wallet has been disconnected.');

            // Remove wallet connection information from local storage
            localStorage.removeItem('walletConnected');

            // Update UI
            disconnectButton.style.display = 'none';
            navbarConnectButton.style.display = 'inline-block';
            connectButton.style.display = 'inline-block';

        } catch (error) {
            console.error('An error occurred while disconnecting your wallet:', error);
        }
    });

    logoutButton.addEventListener('click', () => {
        try {
            // Disconnect Phantom wallet when logout button is clicked
            window.solana.disconnect();
            console.log('Wallet has been disconnected.');

            // Remove wallet connection information from local storage
            localStorage.removeItem('walletConnected');
        } catch (error) {
            console.error('An error occurred while disconnecting your wallet:', error);
        }
    });

    // Check if wallet is connected on page load
    const isWalletConnected = localStorage.getItem('walletConnected') === 'true';
    if (isWalletConnected) {
        try {
            const wallet = await window.solana.connect();
            console.log('Connected to Phantom wallet:', wallet.publicKey.toString());
        } catch (error) {
            console.error('An error occurred while connecting your wallet:', error);
        }
    }

    // Check if wallet is connected on page load
    if (window.solana.isConnected) {
        connectButton.style.display = 'none';
        navbarConnectButton.style.display = 'none';
        disconnectButton.style.display = 'block';
    } else {
        connectButton.style.display = 'block';
        navbarConnectButton.style.display = 'inline-block';
        disconnectButton.style.display = 'none';
    }

    async function sendWalletInfo(publicKey) {
    try {
        const csrftoken = Cookies.get('csrftoken');
        const response = await fetch('/connect-wallet', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                "publicKey": publicKey,
            })
        });
            if (response.ok) {
                console.log('Wallet information sent successfully.');
                window.location.href = '/profile';
            } else {
                console.error('Failed to send wallet information.');
            }
        } catch (error) {
            console.error('An error occurred while sending wallet information:', error);
        }
    }
});