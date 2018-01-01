# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=80)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(null=True, blank=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(unique=True, max_length=30)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('cno', models.AutoField(serialize=False, primary_key=True)),
                ('uno', models.CharField(max_length=30)),
                ('uname', models.CharField(max_length=10)),
                ('uphone', models.CharField(max_length=20)),
                ('uwechat', models.TextField()),
                ('ufirm', models.TextField()),
                ('udepartment', models.TextField()),
                ('ucode', models.CharField(max_length=10)),
                ('utime', models.DateTimeField()),
            ],
            options={
                'db_table': 'contact',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(null=True, blank=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.SmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Equip',
            fields=[
                ('eno', models.AutoField(serialize=False, primary_key=True)),
                ('tno', models.IntegerField()),
                ('ename', models.TextField()),
                ('eurl', models.TextField()),
            ],
            options={
                'db_table': 'equip',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('hno', models.AutoField(serialize=False, primary_key=True)),
                ('htitle1', models.TextField()),
                ('htitle2', models.TextField()),
                ('htitle3', models.TextField()),
                ('hdetail', models.TextField()),
                ('haddress', models.TextField()),
                ('hlongitude', models.FloatField()),
                ('hlatitude', models.FloatField()),
                ('hprice', models.IntegerField()),
                ('hprice_old', models.IntegerField()),
                ('hsquare', models.IntegerField()),
                ('htype', models.TextField()),
                ('hpic', models.TextField()),
                ('hvalue', models.FloatField()),
            ],
            options={
                'db_table': 'house',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HouseDiscount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hno', models.IntegerField()),
                ('hour', models.IntegerField()),
                ('discount', models.IntegerField()),
            ],
            options={
                'db_table': 'house_discount',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HouseDisplay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hno', models.IntegerField()),
                ('hflag', models.IntegerField()),
            ],
            options={
                'db_table': 'house_display',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HouseEquip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hno', models.IntegerField()),
                ('eno', models.IntegerField()),
            ],
            options={
                'db_table': 'house_equip',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HouseIcon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hno', models.IntegerField()),
                ('ino', models.IntegerField()),
            ],
            options={
                'db_table': 'house_icon',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HouseLabel',
            fields=[
                ('lno', models.AutoField(serialize=False, primary_key=True)),
                ('lname', models.CharField(max_length=8)),
                ('hno', models.IntegerField()),
            ],
            options={
                'db_table': 'house_label',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HouseMemory',
            fields=[
                ('mno', models.AutoField(serialize=False, primary_key=True)),
                ('hno', models.IntegerField()),
                ('murl', models.TextField()),
            ],
            options={
                'db_table': 'house_memory',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HousePic',
            fields=[
                ('pno', models.AutoField(serialize=False, primary_key=True)),
                ('hno', models.IntegerField()),
                ('purl', models.TextField()),
            ],
            options={
                'db_table': 'house_pic',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Icon',
            fields=[
                ('ino', models.AutoField(serialize=False, primary_key=True)),
                ('iname', models.TextField()),
                ('iurl', models.TextField()),
            ],
            options={
                'db_table': 'icon',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('lno', models.AutoField(serialize=False, primary_key=True)),
                ('ldetail', models.TextField()),
                ('ltime', models.DateTimeField()),
            ],
            options={
                'db_table': 'logs',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('ono', models.AutoField(serialize=False, primary_key=True)),
                ('oid', models.CharField(max_length=30)),
                ('hno', models.IntegerField()),
                ('uno', models.CharField(max_length=30)),
                ('odate', models.DateField()),
                ('ostart', models.TimeField()),
                ('oend', models.TimeField()),
                ('otype', models.IntegerField()),
                ('onum', models.IntegerField()),
                ('oready', models.IntegerField()),
                ('obarbecue', models.IntegerField()),
                ('ofapiao', models.IntegerField()),
                ('otip', models.TextField()),
                ('ototal', models.IntegerField()),
                ('ocno', models.IntegerField()),
                ('otime', models.DateTimeField()),
                ('osign', models.CharField(max_length=40)),
                ('osign2', models.CharField(max_length=40)),
                ('prepay_id', models.CharField(max_length=64)),
                ('ostatus', models.IntegerField()),
            ],
            options={
                'db_table': 'orders',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('uid', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('unickname', models.TextField(db_column='unickName')),
                ('ugender', models.IntegerField()),
                ('ulanguage', models.TextField()),
                ('ucity', models.TextField()),
                ('uprovince', models.TextField()),
                ('ucountry', models.TextField()),
                ('uavatarurl', models.TextField()),
                ('usigntime', models.DateTimeField(db_column='USigntime')),
            ],
            options={
                'db_table': 'Users',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UsersLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uno', models.CharField(max_length=32)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('speed', models.FloatField()),
                ('accuracy', models.FloatField()),
                ('time', models.DateTimeField()),
            ],
            options={
                'db_table': 'Users_location',
                'managed': False,
            },
        ),
    ]
