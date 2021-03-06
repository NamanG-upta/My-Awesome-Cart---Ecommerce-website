# Generated by Django 2.2.3 on 2019-08-06 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='blogpost',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('head0', models.CharField(default=' ', max_length=500)),
                ('head1', models.CharField(default=' ', max_length=500)),
                ('head2', models.CharField(default=' ', max_length=500)),
                ('pub_date', models.DateField()),
                ('thumbnail', models.ImageField(upload_to='')),
            ],
        ),
        migrations.DeleteModel(
            name='product',
        ),
    ]
