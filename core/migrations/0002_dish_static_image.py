from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='static_image',
            field=models.CharField(blank=True, help_text='Optional static image path, e.g. core/images/paneer.png', max_length=255),
        ),
    ]
