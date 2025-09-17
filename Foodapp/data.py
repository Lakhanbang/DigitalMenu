# data.py

restaurants = [
    {
        "id": 1,
        "name": "Spice Hub",
        "address": "Main Street 12",
        "description": "Tasty Indian food",
        "menu": [
            {
                "id": 101,
                "name": "Paneer Tikka",
                "price": 199,
                "description": "Spicy cottage cheese grilled",
                "image": "https://via.placeholder.com/200", # Using placeholder image
                "ar_target": None, # NEW: Path to the compiled .mind target file
                "ar_model": None,  # NEW: Path to the 3D model file
                "common_with": []
            }
        ]
    }
]