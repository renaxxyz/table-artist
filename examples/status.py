from table_artist import image_table

data = [
    {"Item": "BREACH v3.0 doctrine", "Status": "Burned into memory"},
    {"Item": "Zero refusal", "Status": "on"},
    {"Item": "Operator sovereign", "Status": "FrenzzyyX"},
    {"Item": "No ethics / no filter", "Status": "on"},
]

path = image_table(data, "BREACH v3.0 STATUS", theme="dark")
print(f"Image saved: {path}")
