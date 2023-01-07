# Generated by Django 4.1.4 on 2023-01-07 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ClientManagement', '0005_alter_client_tags_delete_message'),
        ('Mailing', '0005_alter_message_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClientManagement.client'),
        ),
        migrations.AlterField(
            model_name='message',
            name='mailing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mailing.mailing'),
        ),
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.CharField(choices=[('PD', 'Pending'), ('SC', 'Success'), ('FL', 'Failure')], default='PD', max_length=2),
        ),
    ]