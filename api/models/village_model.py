from django.db import models

class Village(models.Model):
    class Meta:
        db_table = "village"

    village_name = models.CharField(max_length=20)
    colour_code = models.CharField(max_length=20)
    is_hidden = models.BooleanField(default=False)
