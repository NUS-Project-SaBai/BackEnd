# Migration to populate initial village data for the new admin settings feature
# This ensures all villages have the is_hidden field properly initialized for visibility control

from django.db import migrations


# Function to populate database with initial village data
def populate_villages(apps, schema_editor):
    Village = apps.get_model("api", "Village")

    # Initial village data with names, colors, and visibility status
    villages_data = [
        {"village_name": "PC", "colour_code": "text-red-400", "is_hidden": False},
        {"village_name": "CA", "colour_code": "text-blue-400", "is_hidden": False},
        {"village_name": "TT", "colour_code": "text-green-400", "is_hidden": False},
        {"village_name": "TK", "colour_code": "text-yellow-400", "is_hidden": False},
        {"village_name": "SV", "colour_code": "text-purple-400", "is_hidden": False},
    ]

    # Create villages if they don't exist, skip if already present
    for village_data in villages_data:
        Village.objects.get_or_create(
            village_name=village_data["village_name"],
            defaults={
                "colour_code": village_data["colour_code"],
                "is_hidden": village_data["is_hidden"],
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        (
            "api",
            "0012_file_description_file_is_deleted",
        ),  # Update to your latest migration
    ]
    operations = [
        migrations.RunPython(populate_villages),  # Run the village population function
    ]
