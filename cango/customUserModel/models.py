from django.db import models
from django.contrib.auth.models import (
	BaseUserManager, AbstractBaseUser
)
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os


class CangoUserManager(BaseUserManager):
	
	def create_user(self, email, use_wheelchair, date_of_birth, nickname, supporters, password=None):
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
			email=self.normalize_email(email),
			use_wheelchair=use_wheelchair,
			date_of_birth=date_of_birth,
			nickname=nickname,
			supporters=supporters,
			)
		#class models.BaseUserManager
		#classmethod normalize_email(email)
		#foo@bar.com and foo@BAR.com are equivalent

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, use_wheelchair, date_of_birth, nickname, password, supporters):
		user = self.create_user(
			email,
			password=password,
			use_wheelchair=use_wheelchair,
			date_of_birth=date_of_birth,
			nickname=nickname,
			supporters=supporters,
			)
		user.is_admin = True
		user.save(using=self._db)
		return user


class OverwriteStorage(FileSystemStorage):

	def get_available_name(self, name, max_length=None):
		# name : user_profile\{pk}.jpg
		if self.exists(name):
			os.remove(os.path.join(settings.MEDIA_ROOT, name))
		return super(OverwriteStorage, self).get_available_name(name)


class CangoUser(AbstractBaseUser):
	class Meta:
		db_table = 'cango_user'

	def get_image_path(self, filename):
		list = filename.split('.')
		extender = list[1] # 확장자
		return 'user_profile/{0}'.format(str(self.id)+'.'+extender)

	email = models.EmailField(
		verbose_name='email address',
		max_length=255,
		unique=True,
		)
	nickname = models.CharField(max_length=16, unique=True, null=True)
	date_of_birth = models.DateField(null=True)
	profile_pic = models.ImageField(
		upload_to = get_image_path,
		default='user_profile/default.png',
		storage=OverwriteStorage(),
		)	
	use_wheelchair = models.BooleanField(default=False)
	point = models.IntegerField(default=0)
	level = models.IntegerField(default=0)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	supporters = models.IntegerField(default=0)
	date_registered = models.DateTimeField(auto_now_add=True)

	objects = CangoUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['nickname', 'date_of_birth', 'use_wheelchair', 'supporters']

	def get_full_name(self):
		return self.email

	def get_short_name(self):
		return self.email

	def __str__(self):
		return self.nickname

	def has_perm(self, perm, obj=None):
		#Should I write more codes to check if user have
		#specific permission?
		return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		return self.is_admin
