import os
from django.conf import settings
from django.utils.crypto import get_random_string
from django.db import models
from django.utils.encoding import smart_text
from customUserModel.models import CangoUser

class Test(models.Model):
	name = models.CharField(max_length=30)

class Place(models.Model):
	def get_image_path(instance, filename):
		sampleList = filename.split('.')
		name = sampleList[0]
		extender = sampleList[1]
		rest_dir = 'place/{0}/{1}'.format(smart_text(instance.name, encoding='utf-8', string_only=False, errors='strict'), filename)

		filepath = os.path.join(settings.BASE_DIR, rest_dir)
		while os.path.exists(filepath):
			filename = name + get_random_string(5) + '.' + extender
			rest_dir = 'place/{0}/{1}'.format(smart_text(instance.name, encoding='utf-8', string_only=False, errors='strict'), filename)			

		return 'place/{0}/{1}'.format(instance.name, filename)

	daumID = models.CharField(max_length=30, null=True)
	category = models.CharField(max_length=100, null=True)
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=200)
	address_new = models.CharField(max_length=200)
	phone_number = models.CharField(max_length=40, null=True)
	latitude = models.DecimalField(max_digits=12, decimal_places=9)
	longitude = models.DecimalField(max_digits=12, decimal_places=9)
	user = models.ForeignKey(CangoUser, on_delete=models.SET_NULL, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	verified_flag = models.BooleanField(default=False)
	failed_flag = models.BooleanField(default=False)

	# 단차
	# 1 : 문 턱이 없거나 경사로 있음
	# 2 : 일반카드 세로 길이 이하 (5.35cm 이하)
	# 3 : 일반카드 세로 길이 이상 (5.35cm 초과) - 배리어프리 X
	c_barrier = models.PositiveSmallIntegerField()

	# 장소 층 수
	# 1 : 1층 / 2 : 1층이 아님 / 3 : 여러 층 사용
	c_floor = models.PositiveSmallIntegerField(null=True)

	# 엘레베이터 유무
	# 1 : 있음 / 2 : 없음
	c_elevator_exist = models.PositiveSmallIntegerField(null=True)

	# 엘레베이터 정원
	# Interger Type 정원 수 입력
	c_elevator_capacity = models.PositiveSmallIntegerField(null=True)

	# 테이블과 의자의 이동 가능 여부
	# 1 : 둘다 가능 / 2 : 테이블만 가능 / 3 : 의자만 가능 / 4 : 둘다 고정 / 5: 해당없음 
	c_chair_movable = models.PositiveSmallIntegerField(null=True)

	# 화장실 접근 가능 여부
	# 1 : 가능 / 2 : 불가능 / 3: 화장실 없음
	c_toilet_available = models.PositiveSmallIntegerField(null=True)

	# 장애인화장실 유무
	# 1 : 있음 / 2 : 없음
	c_handicapped_toilet = models.PositiveSmallIntegerField(null=True)

	# 주차장 유무
	# 1 : 있음 / 2 : 없음
	c_parking_lot_exist = models.PositiveSmallIntegerField(null=True)

	# 장애인주차장 유무
	# 1 : 있음 / 2 : 없음
	c_handicapped_parking_lot = models.PositiveSmallIntegerField(null=True)

	# 기타사항
	extra_info = models.TextField(max_length=300, null=True)

	p_entrance = models.ImageField(upload_to = 'test/',
		null=True)
	p_interior = models.ImageField(upload_to = 'test/',
		null=True,)
	p_extra_pic1 = models.ImageField(upload_to = get_image_path,
		null=True)
	p_extra_pic2 = models.ImageField(upload_to = get_image_path,
		null=True)	
	p_extra_pic3 = models.ImageField(upload_to = get_image_path,
		null=True)
	p_extra_pic4 = models.ImageField(upload_to = get_image_path,
		null=True)
	p_extra_pic5 = models.ImageField(upload_to = get_image_path,
		null=True)
	p_extra_pic6 = models.ImageField(upload_to = get_image_path,
		null=True)
	p_extra_pic7 = models.ImageField(upload_to = get_image_path,
		null=True)
	p_extra_pic8 = models.ImageField(upload_to = get_image_path,
		null=True)

	def __str__(self):
		return self.name


class PlaceHistory(models.Model):
	groupID = models.ForeignKey(Place)
	daumID = models.CharField(max_length=30, null=True)
	category = models.CharField(max_length=100, null=True)
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=200)
	address_new = models.CharField(max_length=200)
	phone_number = models.CharField(max_length=40, null=True)
	latitude = models.DecimalField(max_digits=12, decimal_places=9)
	longitude = models.DecimalField(max_digits=12, decimal_places=9)
	user = models.ForeignKey(CangoUser, on_delete=models.SET_NULL, null=True)
	c_barrier = models.PositiveSmallIntegerField()
	c_floor = models.PositiveSmallIntegerField(null=True)
	c_elevator_exist = models.PositiveSmallIntegerField(null=True)
	c_elevator_capacity = models.PositiveSmallIntegerField(null=True)
	c_chair_movable = models.PositiveSmallIntegerField(null=True)
	c_toilet_available = models.PositiveSmallIntegerField(null=True)
	c_handicapped_toilet = models.PositiveSmallIntegerField(null=True)
	c_parking_lot_exist = models.PositiveSmallIntegerField(null=True)
	c_handicapped_parking_lot = models.PositiveSmallIntegerField(null=True)
	extra_info = models.TextField(max_length=300, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	verified_flag = models.BooleanField(default=False)	


class Comment(models.Model):
	content = models.CharField(max_length=100)
	user = models.ForeignKey(CangoUser, related_name='user', on_delete=models.SET_NULL, null=True)
	place = models.ForeignKey(Place, related_name='comment')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return self.content, self.user

class Like(models.Model):
	user = models.ForeignKey(CangoUser)
	place = models.ForeignKey(Place)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.place, self.user


class Bookmark(models.Model):
	user = models.ForeignKey(CangoUser)
	place = models.OneToOneField(Place)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.place, self.user
