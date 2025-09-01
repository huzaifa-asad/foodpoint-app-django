from django.core.management.base import BaseCommand
from core.models import Dish

DEFAULT_DISHES = [
    {
        "name": "Paneer Tikka",
        "description": "Grilled cottage cheese marinated in spices.",
        "price": 10.99,
    "static_image": "core/images/Paneer Tikka.png",
    },
    {
        "name": "Butter Paneer",
        "description": "Creamy tomato gravy with soft paneer cubes.",
    "price": 10.49,
    "static_image": "core/images/Butter Paneer.png",
    },
    {
        "name": "Paneer Masala",
        "description": "Rich and spicy paneer curry.",
    "price": 9.99,
    "static_image": "core/images/Paneer Masala.png",
    },
    {
        "name": "Sushi Platter",
        "description": "Aromatic rice layered with paneer and spices.",
    "price": 12.99,
    "static_image": "core/images/paneer.png",
    },
]

class Command(BaseCommand):
    help = "Seed default dishes into the database"

    def handle(self, *args, **options):
        created = 0
        for d in DEFAULT_DISHES:
            obj, was_created = Dish.objects.get_or_create(
                name=d["name"],
                defaults={
                    "description": d["description"],
                    "price": d["price"],
                    "static_image": d.get("static_image", ""),
                    "is_featured": True,
                },
            )
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(f"Seeded {created} dishes (idempotent)."))
