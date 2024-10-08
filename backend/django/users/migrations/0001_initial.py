# Generated by Django 4.1.1 on 2022-10-01 04:12

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('fullName', models.CharField(max_length=75)),
                ('verified', models.BooleanField(default=False)),
                ('eduright_Student', models.BooleanField(default=False, help_text='Whether the student is a student at Eduright.')),
                ('stdClass', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='api.classmodel')),
            ],
            options={
                'verbose_name': 'Student',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='StudentMarksData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marksObtained', models.PositiveIntegerField()),
                ('quizset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='markModel_quizset', to='api.quizset')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
            options={
                'ordering': ['-marksObtained'],
            },
        ),
    ]
