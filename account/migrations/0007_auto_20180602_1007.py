# Generated by Django 2.0.5 on 2018-06-02 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_user_integral'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='headimg',
            field=models.ImageField(default='headimg/苹果1_0OtvrIb.jpg', upload_to='headimg'),
        ),
    ]