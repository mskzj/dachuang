# Generated by Django 2.0 on 2018-04-23 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0006_auto_20180423_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent_comment',
            field=models.ForeignKey(default=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='parent', to='comment.comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='root_comment',
            field=models.ForeignKey(default=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='root', to='comment.comment'),
        ),
    ]
