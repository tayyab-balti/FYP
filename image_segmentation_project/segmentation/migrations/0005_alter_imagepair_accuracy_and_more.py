# Generated by Django 4.2.4 on 2024-11-30 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("segmentation", "0004_delete_performancedata_delete_uploadedimage_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="imagepair",
            name="accuracy",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="imagepair",
            name="segmented_image",
            field=models.ImageField(
                blank=True, null=True, upload_to="segmented_images/"
            ),
        ),
    ]
