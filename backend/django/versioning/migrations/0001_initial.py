# Generated by Django 3.2.4 on 2021-07-25 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bugs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Max Characters: 20', max_length=20, unique=True)),
                ('comment', models.CharField(blank=True, help_text='Max Characters: 100', max_length=100, null=True)),
                ('solved', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_Feature_Title', models.CharField(help_text='New feature that can be added to the app.', max_length=100, unique=True)),
                ('pending', models.BooleanField(default=True)),
                ('scale', models.PositiveIntegerField(help_text='Impact on the app. Possible assumption.')),
                ('explain_Scale_Rating', models.CharField(help_text='Explain what could be the impact of this new feature on the app. Max Characters: 150', max_length=150)),
                ('drawbacks', models.CharField(blank=True, help_text='What drawback did/could this feature do.', max_length=100, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Packages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Name of the dependency.', max_length=30)),
                ('Version', models.CharField(max_length=10)),
                ('use', models.CharField(blank=True, help_text='What does this package do. Max Characters: 100', max_length=100, null=True)),
                ('implementation_Location', models.CharField(blank=True, help_text='Where is this package being implemented. Max Characters: 100', max_length=100, null=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('language', models.CharField(max_length=15)),
                ('language_Version', models.CharField(max_length=10)),
                ('area', models.CharField(help_text='Ex. Server-End, Front-End, Website, Application etc', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Security',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('future_Flaw_Warning', models.CharField(help_text='Possible future security flaw in this version.', max_length=100, unique=True)),
                ('niwaran', models.CharField(blank=True, help_text='Possible solution for this security flaw.', max_length=100, null=True)),
                ('solved', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('release', models.CharField(max_length=10)),
                ('testing', models.BooleanField(default=False, verbose_name='Under Testing')),
                ('slug', models.SlugField(unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('bugs', models.ManyToManyField(blank=True, null=True, to='versioning.Bugs')),
                ('feature', models.ManyToManyField(blank=True, null=True, to='versioning.Feature')),
                ('packages', models.ManyToManyField(to='versioning.Packages')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Product', to='versioning.project')),
                ('security', models.ManyToManyField(blank=True, null=True, to='versioning.Security')),
            ],
        ),
    ]
