from django.core.management.base import BaseCommand
from django.utils.text import slugify

from shop.models import Product


class Command(BaseCommand):
    help = "Create a curated Veltrion luxury product catalog for local development."

    def handle(self, *args, **options):
        products = [
            {
                "name": "Rolex-Inspired Celestial Chronograph",
                "category": "watches",
                "price": 128000.00,
                "image_url": "https://images.unsplash.com/photo-1524592094714-0f0654e20314?auto=format&fit=crop&w=1100&q=90",
                "featured": True,
                "stock": 3,
                "description": "A rare exhibition-grade automatic watch with a moonlit dial, brushed platinum presence, and hand-finished gold detailing.",
            },
            {
                "name": "Titanium Pro Max Signature Phone",
                "category": "smartphones",
                "price": 6499.00,
                "image_url": "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?auto=format&fit=crop&w=1100&q=90",
                "featured": True,
                "stock": 8,
                "description": "A flagship smartphone concept in aerospace titanium with a private concierge setup, ceramic glass, and ultra-premium finish.",
            },
            {
                "name": "Gucci-Inspired Obsidian Leather Coat",
                "category": "fashion",
                "price": 18400.00,
                "image_url": "https://images.unsplash.com/photo-1496747611176-843222e1e57c?auto=format&fit=crop&w=1100&q=90",
                "featured": True,
                "stock": 4,
                "description": "A sculptural designer coat in deep black leather, tailored for quiet wealth, evening arrivals, and gallery-level presence.",
            },
            {
                "name": "Dior-Inspired Pearl Noir Sneakers",
                "category": "sneakers",
                "price": 9200.00,
                "image_url": "https://images.unsplash.com/photo-1549298916-b41d501d3772?auto=format&fit=crop&w=1100&q=90",
                "featured": True,
                "stock": 6,
                "description": "Limited-run premium sneakers with pearlized panels, silver edge trims, and a soft architectural silhouette.",
            },
            {
                "name": "Imperial Sapphire Collar",
                "category": "jewelry",
                "price": 189000.00,
                "image_url": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?auto=format&fit=crop&w=1100&q=90",
                "featured": True,
                "stock": 2,
                "description": "An elite jewelry piece featuring sapphire tones, diamond light play, and a museum-grade evening profile.",
            },
            {
                "name": "Maison Aurora Private Parfum",
                "category": "perfumes",
                "price": 3200.00,
                "image_url": "https://images.unsplash.com/photo-1594035910387-fea47794261f?auto=format&fit=crop&w=1100&q=90",
                "featured": True,
                "stock": 12,
                "description": "A private-label extrait with smoked amber, iced iris, and rare oud in a faceted black crystal flacon.",
            },
            {
                "name": "Holographic Command Lens",
                "category": "gadgets",
                "price": 27500.00,
                "image_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1100&q=90",
                "featured": False,
                "stock": 5,
                "description": "A futuristic productivity device for spatial workflows, glass dashboards, and cinematic private offices.",
            },
            {
                "name": "Carbon Atelier Headphones",
                "category": "headphones",
                "price": 11800.00,
                "image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=1100&q=90",
                "featured": True,
                "stock": 7,
                "description": "High-end headphones with carbon fiber shells, lambskin cushions, and studio-grade acoustic isolation.",
            },
            {
                "name": "Veltrion Eclipse Gaming Suite",
                "category": "gaming",
                "price": 86000.00,
                "image_url": "https://images.unsplash.com/photo-1598550476439-6847785fcea6?auto=format&fit=crop&w=1100&q=90",
                "featured": False,
                "stock": 2,
                "description": "A luxury gaming setup with a panoramic display wall, silent workstation core, and ambient architectural lighting.",
            },
            {
                "name": "Sterling Carbon Travel Attaché",
                "category": "accessories",
                "price": 23600.00,
                "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=1100&q=90",
                "featured": True,
                "stock": 5,
                "description": "An exclusive accessory case in carbon weave, silver hardware, and hand-polished leather for private-terminal travel.",
            },
            {
                "name": "Diamond Signal Smart Ring",
                "category": "gadgets",
                "price": 15400.00,
                "image_url": "https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=1100&q=90",
                "featured": False,
                "stock": 9,
                "description": "A futuristic smart ring finished like fine jewelry, designed for biometric access and understated digital control.",
            },
            {
                "name": "Midnight Croc Card Vault",
                "category": "accessories",
                "price": 7800.00,
                "image_url": "https://images.unsplash.com/photo-1627123424574-724758594e93?auto=format&fit=crop&w=1100&q=90",
                "featured": False,
                "stock": 10,
                "description": "A rare card vault with crocodile texture, gold hardware, and glassy black edge finishing.",
            },
        ]

        Product.objects.all().delete()
        for product in products:
            Product.objects.create(slug=slugify(product["name"]), **product)
        self.stdout.write(self.style.SUCCESS("Veltrion luxury products are ready."))
