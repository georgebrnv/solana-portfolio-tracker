from django.shortcuts import render
from django.http import HttpResponse

FAQ = {
    "What is Solana?": "Solana is a high-performance blockchain platform designed for decentralized applications and crypto projects.",
    "How does Solana achieve high throughput?": "Solana achieves high throughput through its unique consensus mechanism called Proof of History (PoH), which timestamps transactions before they are included in a block.",
    "What are some key features of Solana?": "Key features of Solana include its high transaction throughput, low transaction fees, fast confirmation times, and scalability.",
    "What programming languages are supported for developing on Solana?": "Solana supports programming languages such as Rust and C, with plans to support more languages in the future.",
    "Is Solana secure?": "Yes, Solana is designed with security in mind and utilizes various cryptographic techniques to ensure the integrity and security of the network and its transactions.",
    "How can I get started with Solana development?": "To get started with Solana development, you can explore the official Solana documentation, join the Solana developer community, and experiment with building decentralized applications (dApps) on the platform."
}


def index(request):
    return render(request, 'dashboard/index.html', context={
        'faq_questions': FAQ,
    })

def login(request):
    return render(request, 'dashboard/login.html')

def register(request):
    return render(request, 'dashboard/register.html')

def portfolio(request):
    return render(request, 'dashboard/portfolio.html')

def profile(request):
    return render(request, 'dashboard/profile.html')
