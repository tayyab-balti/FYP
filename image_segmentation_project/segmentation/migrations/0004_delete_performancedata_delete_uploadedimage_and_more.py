# Generated by Django 4.2.4 on 2024-11-30 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("segmentation", "0003_imagepair_accuracy_imagepair_processing_time"),
    ]

    operations = [
        migrations.DeleteModel(
            name="PerformanceData",
        ),
        migrations.DeleteModel(
            name="UploadedImage",
        ),
        migrations.AlterModelOptions(
            name="imagepair",
            options={},
        ),
        migrations.AlterField(
            model_name="imagepair",
            name="segmented_image",
            field=models.ImageField(default="", upload_to="segmented_images/"),
            preserve_default=False,
        ),
    ]
