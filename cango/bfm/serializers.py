from rest_framework import serializers
from .fields import Base64ImageField
from customUserModel.models import CangoUser
from bfm.models import *
from rest_framework import status


# User Update를 위한 serializer
class UserInfoSerializer(serializers.ModelSerializer):
	profile_pic = Base64ImageField(max_length=None,use_url=True)

	class Meta:
		model = CangoUser
		fields = ['id', 'email', 'profile_pic', 'date_of_birth', 
		'use_wheelchair', 'point', 'level', 'nickname']
		#read_only_fields = ('id', 'email', 'point', 'level')
		#extra_kwargs = {''}

	def validate_nickname(self, value):
		if CangoUser.objects.filter(nickname=value).exists():
			raise serializers.ValidationError("This nickname exist. please try another nickname.")
		return value

	def __init__(self, *args, **kwargs):
		super(UserInfoSerializer, self).__init__(*args, **kwargs)
		for field in self.fields:
			if field in ['id', 'email', 'point', 'level']:
				self.fields[field].required = False
				self.fields[field].read_only = True
			if field in ['profile_pic']:
				self.fields[field].required = False


# comment 등록용 serializer
class CommentRegisterSerializer(serializers.ModelSerializer):

	class Meta:
		model = Comment
		fields = ('content', 'place')


# comment Get으로 해당 리스트 받기 위한 serializer
class CommentSerializer(serializers.ModelSerializer):
	user = serializers.StringRelatedField()

	class Meta:
		model = Comment
		fields = ('id', 'content', 'user', 'created_at')


class LikeRegisterSerializer(serializers.ModelSerializer):

	class Meta:
		model = Like
		fields = ('place',)


class BookmarkRegisterSerializer(serializers.ModelSerializer):

	class Meta:
		model = Bookmark
		fields = ('place',)


class BookmarkSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Bookmark
		fields = ('place', 'created_at')

class PlaceStatusSerializer(serializers.ModelSerializer):
	class Meta:
		model = Place
		fields = ('name', 'address', 'address_new', 'created_at', 'verified_flag', 'failed_flag')



class PlaceInfoSerializer(serializers.ModelSerializer):
	comment = CommentSerializer(many=True, read_only=True)
	user = serializers.StringRelatedField()

	class Meta:
		model = Place
		
		fields = (
			'id',
			'category',
			'created_at',
			'comment',
			'user',
			'name', 
			'address', 
			'address_new', 
			'phone_number', 
			'latitude', 
			'longitude',
			'c_barrier', 
			'c_floor', 
			'c_elevator_exist', 
			'c_elevator_capacity', 
			'c_chair_movable',
			'c_toilet_available', 
			'c_handicapped_toilet', 
			'c_parking_lot_exist',
			'c_handicapped_parking_lot', 
			'extra_info',
			'p_entrance', 
			'p_interior',
			'p_extra_pic1', 
			'p_extra_pic2', 
			'p_extra_pic3', 
			'p_extra_pic4', 
			'p_extra_pic5',
		)

	# def from_native(self, data, files):
	# 	data['extra'] = self.context['extra']
	# 	return super(PlaceInfoSerializer, self).from_native(data, files)


class PlaceRegisterSerializer(serializers.ModelSerializer):
	p_entrance = Base64ImageField(max_length=None,use_url=True)
	p_interior = Base64ImageField(max_length=None,use_url=True)
	p_extra_pic1 = Base64ImageField(max_length=None,use_url=True)
	p_extra_pic2 = Base64ImageField(max_length=None,use_url=True)
	p_extra_pic3 = Base64ImageField(max_length=None,use_url=True)
	p_extra_pic4 = Base64ImageField(max_length=None,use_url=True)
	p_extra_pic5 = Base64ImageField(max_length=None,use_url=True)

	class Meta:
		model = Place
		fields = [
			'category',
			'name', 
			'address', 
			'address_new', 
			'phone_number', 
			'latitude', 
			'longitude',
			'c_barrier', 
			'c_floor', 
			'c_elevator_exist', 
			'c_elevator_capacity', 
			'c_chair_movable',
			'c_toilet_available', 
			'c_handicapped_toilet', 
			'c_parking_lot_exist',
			'c_handicapped_parking_lot', 
			'extra_info',
			'p_entrance', 
			'p_interior',
			'p_extra_pic1', 
			'p_extra_pic2', 
			'p_extra_pic3', 
			'p_extra_pic4', 
			'p_extra_pic5',
		]

	def __init__(self, *args, **kwargs):
		super(PlaceRegisterSerializer, self).__init__(*args, **kwargs)
		list = [
			'category',
			'c_elevator_exist', 
			'c_elevator_capacity', 
			'c_elevator_exist', 
			'c_elevator_capacity', 
			'c_chair_movable', 
			'c_toilet_available', 
			'c_handicapped_toilet',
			'c_parking_lot_exist', 
			'c_handicapped_parking_lot', 
			'extra_info',
			'p_entrance', 
			'p_interior',
			'p_extra_pic1', 
			'p_extra_pic2', 
			'p_extra_pic3', 
			'p_extra_pic4', 
			'p_extra_pic5',
		]
		for field in self.fields:
			if field in list:
				self.fields[field].required = False
