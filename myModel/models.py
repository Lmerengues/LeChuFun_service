# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Users(models.Model):
    uid = models.CharField(primary_key=True, max_length=30)
    unickname = models.TextField(db_column='unickName')  # Field name made lowercase.
    ugender = models.IntegerField()
    ulanguage = models.TextField()
    ucity = models.TextField()
    uprovince = models.TextField()
    ucountry = models.TextField()
    uavatarurl = models.TextField()
    usigntime = models.DateTimeField(db_column='USigntime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Users'


class UsersLocation(models.Model):
    uno = models.CharField(max_length=32)
    latitude = models.FloatField()
    longitude = models.FloatField()
    speed = models.FloatField()
    accuracy = models.FloatField()
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'Users_location'
        unique_together = (('uno', 'time'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Contact(models.Model):
    cno = models.AutoField(primary_key=True)
    uno = models.CharField(max_length=30)
    uname = models.CharField(max_length=10)
    uphone = models.CharField(max_length=20)
    uwechat = models.TextField()
    ufirm = models.TextField()
    udepartment = models.TextField()
    ucode = models.CharField(max_length=10)
    utime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'contact'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Equip(models.Model):
    eno = models.AutoField(primary_key=True)
    tno = models.IntegerField()
    ename = models.TextField()
    eurl = models.TextField()

    class Meta:
        managed = False
        db_table = 'equip'


class House(models.Model):
    hno = models.AutoField(primary_key=True)
    htitle1 = models.TextField()
    htitle2 = models.TextField()
    htitle3 = models.TextField()
    hdetail = models.TextField()
    haddress = models.TextField()
    hlongitude = models.FloatField()
    hlatitude = models.FloatField()
    hprice = models.IntegerField()
    hprice_old = models.IntegerField()
    hsquare = models.IntegerField()
    htype = models.TextField()
    hpic = models.TextField()
    hvalue = models.FloatField()

    class Meta:
        managed = False
        db_table = 'house'


class HouseDiscount(models.Model):
    hno = models.IntegerField(primary_key=True)
    hour = models.IntegerField(primary_key=True)
    discount = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'house_discount'
        unique_together = (('hno', 'hour'),)


class HouseDisplay(models.Model):
    hno = models.IntegerField(primary_key=True)
    hflag = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'house_display'
        unique_together = (('hno', 'hflag'),)


class HouseEquip(models.Model):
    hno = models.IntegerField()
    eno = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'house_equip'
        unique_together = (('hno', 'eno'),)


class HouseIcon(models.Model):
    hno = models.IntegerField()
    ino = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'house_icon'
        unique_together = (('hno', 'ino'),)


class HouseLabel(models.Model):
    lno = models.AutoField(primary_key=True)
    lname = models.CharField(max_length=8)
    hno = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'house_label'


class HouseMemory(models.Model):
    mno = models.AutoField(primary_key=True)
    hno = models.IntegerField()
    murl = models.TextField()

    class Meta:
        managed = False
        db_table = 'house_memory'


class HousePic(models.Model):
    pno = models.AutoField(primary_key=True)
    hno = models.IntegerField()
    purl = models.TextField()

    class Meta:
        managed = False
        db_table = 'house_pic'


class Icon(models.Model):
    ino = models.AutoField(primary_key=True)
    iname = models.TextField()
    iurl = models.TextField()

    class Meta:
        managed = False
        db_table = 'icon'


class Logs(models.Model):
    lno = models.AutoField(primary_key=True)
    ldetail = models.TextField()
    ltime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'logs'


class Orders(models.Model):
    ono = models.AutoField(primary_key=True)
    oid = models.CharField(max_length=30)
    hno = models.IntegerField()
    uno = models.CharField(max_length=30)
    odate = models.DateField()
    ostart = models.TimeField()
    oend = models.TimeField()
    otype = models.IntegerField()
    onum = models.IntegerField()
    oready = models.IntegerField()
    obarbecue = models.IntegerField()
    ofapiao = models.IntegerField()
    otip = models.TextField()
    ototal = models.IntegerField()
    ocno = models.IntegerField()
    otime = models.DateTimeField()
    osign = models.CharField(max_length=40)
    osign2 = models.CharField(max_length=40)
    prepay_id = models.CharField(max_length=64)
    ostatus = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'orders'
