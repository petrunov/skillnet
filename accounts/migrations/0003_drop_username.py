from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        # Remove the old username column
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        # Ensure email is unique & non-null
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(
                'email address',
                unique=True,
                max_length=254
            ),
        ),
    ]
