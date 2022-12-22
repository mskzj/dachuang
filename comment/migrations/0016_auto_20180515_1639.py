# Generated by Django 2.0 on 2018-05-15 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0015_auto_20180508_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='admire_record',
            name='is_admired',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='admire_record',
            name='admire_comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='comment.Comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent_comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='parent', to='comment.Comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='root_comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='root', to='comment.Comment'),
        ),
    ]