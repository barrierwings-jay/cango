from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bfm.serializers import *
from customUserModel.models import CangoUser
from bfm.models import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core import serializers
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.db import transaction


class VerifyView(LoginRequiredMixin, ListView):
	login_url = '/admin/'
	template_name = 'bfm/verify.html'
	context_object_name = 'place_list'
	queryset = Place.objects.filter(verified_flag=False).filter(failed_flag=False)


class FailView(LoginRequiredMixin, ListView):
	login_url = '/admin/'
	template_name = 'bfm/fail.html'
	context_object_name = 'place_list'
	queryset = Place.objects.filter(failed_flag=True)


class DetailView(LoginRequiredMixin, DetailView):
	login_url = '/admin/'
	model = Place
	template_name = 'bfm/verify_detail.html'


class VerifyConfirmView(LoginRequiredMixin, View):
	login_url = '/admin/'

	def post(self, request, *args, **kwargs):
		if self.request.user.is_admin:
			if request.POST.get('verified_pk'):
				pk = request.POST.get('verified_pk')
				if request.POST.get('result') == 'failed' :
					try :
						place = Place.objects.get(id=pk)
						place.failed_flag = True
						place.save()
					except Exception as e:
						print("error :",e)
				elif request.POST.get('result') == 'verified' :
					try:
						place = Place.objects.get(id=pk)
						place.verified_flag = True
						user = place.user
						user.point = F('point') + 200
						user.level = F('level') + 100
						with transaction.atomic():
							user.save()
							place.save()
					except Exception as e:
						print("error :", e)
				else:
					print('error : no result')

		return redirect('bfm:verify_main')


# user 정보 업데이트
class UserInfoUpdateView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self, request, format=None):
		cangoUser = CangoUser.objects.filter(id=request.user.id)
		serializer = UserInfoSerializer(cangoUser, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request, format=None):
		cangoUser = CangoUser.objects.get(id=request.user.id)
		serializer = UserInfoSerializer(cangoUser, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRankList(APIView):

	def get(self, request, format=None):
		cangoUser = CangoUser.objects.order_by('-level')[:100]
		serializer = UserInfoSerializer(cangoUser, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


class UserPlaceList(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self, request, format=None):
		user = self.request.user
		serializer = PlaceStatusSerializer(user.place_set.all(), many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


class SearchPlace(APIView):

	def post(self, request, format=None):
		if request.POST.get('keyword'):
			keyword = request.POST.get('keyword')
			print('key word : ', keyword)
			place = Place.objects.filter(name__contains=keyword)
			serializer = PlaceInfoSerializer(place, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response('keyword is not valid', status=status.HTTP_400_BAD_REQUEST)


# 장소 댓글
class CommentView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self, request, format=None):
		# 해당되는 장소의 PK 값을 해더에 보내야 함. place : pk값
		# django rest framework에서 header key이름인 place를 대문자에다가 HTTP_을 자동으로 붙임
		if request.META.get('HTTP_PLACE'):
			place_pk = request.META.get('HTTP_PLACE')
			
			try:
				place = Place.objects.get(id=place_pk)
			except Exception:
				# 없는 place의 pk를 보냈을 경우 error 발생
				error = {'error' : 'place does not exist.'}
				return Response(error, status=status.HTTP_400_BAD_REQUEST)

			# 해당되는 장소와 FK로 연결된 모든 코멘트를 전달
			serializer = CommentSerializer(place.comment.all(), many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			# 해더값에 place pk 번호를 넘기지 않으면 에러 문구로 안내
			error = {'error' : 'you should send place pk in header'}
			return Response(error, status=status.HTTP_400_BAD_REQUEST)

	def post(self, request, format=None):
		place_pk = request.POST.get('place')
		# 먼저 Post로 보낸 place pk가 존재하는 것인지 check
		try:
			place = Place.objects.get(id=place_pk)
		except Exception:
			error = {'error' : 'place does not exist.'}
			return Response(error, status=status.HTTP_400_BAD_REQUEST)

		serializer = CommentRegisterSerializer(data=request.data)
		if serializer.is_valid():
			# Token값을 보낸 아이디로 자동 저장
			serializer.save(user=self.request.user)
			serializer = CommentSerializer(place.comment.all(), many=True)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	# 자신의 comment를 지우기 위함
	def delete(self, request, format=None):
		if request.META.get('HTTP_COMMENT'):
			comment_pk = request.META.get('HTTP_COMMENT')

			try:
				comment = Comment.objects.get(id=comment_pk)
				place_pk = comment.place.id
			except Exception:
				error = {'error' : 'comment does not exist.'}
				return Response(error, status=status.HTTP_400_BAD_REQUEST)

			# 본인의 comment만 지울 수 있도록 확인
			if comment.user == self.request.user:
				comment.delete()
				place = Place.objects.get(id=place_pk)
				serializer = CommentSerializer(place.comment.all(), many=True)
				return Response(serializer.data, status=status.HTTP_200_OK)
			else:
				error = {'error' : 'only possible to delete your comment.'}
				return Response(error, status=status.HTTP_400_BAD_REQUEST)			

		else:
			error = {'error' : 'you should send comment pk in header'}
			return Response(error, status=status.HTTP_400_BAD_REQUEST)

	# 자신의 comment를 Update하기 위함
	def put(self, request, format=None):
		if request.META.get('HTTP_COMMENT'):
			comment_pk = request.META.get('HTTP_COMMENT')

			try:
				comment = Comment.objects.get(id=comment_pk)
				place_pk = comment.place.id
			except Exception:
				error = {'error' : 'comment does not exist.'}
				return Response(error, status=status.HTTP_400_BAD_REQUEST)			

			if comment.user == self.request.user:
				serializer = CommentRegisterSerializer(comment, data=request.data, partial=True)
				if serializer.is_valid():
					serializer.save()
					place = Place.objects.get(id=place_pk)
					serializer = CommentSerializer(place.comment.all(), many=True)
					return Response(serializer.data, status=status.HTTP_200_OK)
				else:
					return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

			else:
				error = {'error' : 'only possible to edit your comment.'}
				return Response(error, status=status.HTTP_400_BAD_REQUEST)	
			
		else:
			error = {'error' : 'you should send comment pk in header'}
			return Response(error, status=status.HTTP_400_BAD_REQUEST)


# 장소에 좋아요 버튼 클릭
class LikeView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self, request, format=None):
		# 해당되는 장소의 PK 값을 해더에 보내야 함. place : pk값
		if request.META.get('HTTP_PLACE'):
			place_pk = request.META.get('HTTP_PLACE')
			# Like table에 해당장소와 request user의 row값이 있는지 확인
			like = Like.objects.filter(place=place_pk).filter(user=self.request.user).exists()
			number = Like.objects.filter(place=place_pk).count()
			data = {'like' : like, 'number' : number }
			return Response(data, status=status.HTTP_200_OK)
		return Response(status=status.HTTP_400_BAD_REQUEST)

	def post(self, request, format=None):
		place_pk = request.POST.get('place')

		if not Like.objects.filter(place=place_pk).filter(user=self.request.user).exists():
			serializer = LikeRegisterSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save(user=self.request.user)
				number = Like.objects.filter(place=place_pk).count()
				# 리턴 값 : 본인이 like했는지 여부와 이 장소에 대한 전체 like 숫자
				data = {'like' : 'True', 'number' : number }
				return Response(data, status=status.HTTP_200_OK)
			# validation 실패시 오류 메세지 리턴
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		
		# 이미 like버튼을 눌렀으면 like를 false로 하기 위하여 테이블에서 해당 값을 지움
		else:
			like = Like.objects.filter(place=place_pk).filter(user=self.request.user)
			like.delete()
			number = Like.objects.filter(place=place_pk).count()
			# 리턴 값 : 본인이 like했는지 여부와 이 장소에 대한 전체 like 숫자
			data = {'like' : 'False', 'number' : number }
			return Response(data, status=status.HTTP_200_OK)


# 북마크
class BookmarkView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self, request, format=None):
		user = self.request.user
		serializer = BookmarkSerializer(user.like_set.all(), many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request, format=None):
		place_pk = request.POST.get('place')

		if not Bookmark.objects.filter(place=place_pk).filter(user=self.request.user).exists():
			serializer = BookmarkRegisterSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save(user=self.request.user)
				number = Like.objects.filter(place=place_pk).count()
				# 리턴 값 : 본인이 bookmark 설정했는지 여부
				data = {'bookmark' : 'True'}
				return Response(data, status=status.HTTP_200_OK)
			# validation 실패시 오류 메세지 리턴
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		
		# 이미 bookmark버튼을 눌렀으면 bookmark설정을 false로 하기 위하여 테이블에서 해당 값을 지움
		else:
			bookmark = Bookmark.objects.filter(place=place_pk).filter(user=self.request.user)
			bookmark.delete()
			# 리턴 값 : 본인이 bookmark 설정했는지 여부
			data = {'bookmark' : 'False'}
			return Response(data, status=status.HTTP_200_OK)


class PlaceView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self, request, format=None):
		if request.META.get('HTTP_PLACE'):
			place_pk = request.META.get('HTTP_PLACE')
			place = Place.objects.get(id=place_pk)
			
			bookmark_flag = Bookmark.objects.filter(place=place).filter(user=self.request.user).exists()
			like_flag = Like.objects.filter(place=place).filter(user=self.request.user).exists()
			like_number = Like.objects.filter(place=place).count()
			extra = {'like':like_flag, 'number':like_number, 'bookmark':bookmark_flag}
			serializer = PlaceInfoSerializer(instance=place)
			extra.update(serializer.data)
			return Response(extra, status=status.HTTP_201_CREATED)

		return Response(status=status.HTTP_400_BAD_REQUEST)

	def post(self, request, format=None):
		if request.META.get('HTTP_PLACE'):
			place = Place.objects.get(id=request.META.get('HTTP_PLACE'))
			serializer = PlaceRegisterSerializer(place, data=request.data)
		else:
			serializer = PlaceRegisterSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(user=self.request.user)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
