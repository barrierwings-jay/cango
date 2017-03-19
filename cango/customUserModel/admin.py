from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from customUserModel.models import CangoUser


class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='Password',
		widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation',
		widget=forms.PasswordInput)

	class Meta:
		model = CangoUser
		fields = ('email', 'date_of_birth', 'use_wheelchair')

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("passwords don't match")
		return password2
		#need to add password rule like
		#you should put at least one word and number together


	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user


class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = CangoUser
		fields = ('email', 'password', 'date_of_birth',
			'is_active', 'is_admin')

	def clean_password(self):
		return self.initial["password"]


class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm

	list_display = ('email', 'nickname', 'profile_pic', 'date_of_birth', 'is_admin',
		'use_wheelchair', 'point', 'level')
	list_filter = ('is_admin', )
	fieldsets = (
		(None, {
			'fields': ('email', 'nickname', 'password')
		}),
		('Personal info', {
			'fields': ('profile_pic','date_of_birth', 'use_wheelchair', 'point', 'level')
		}),
		('Permissions', {
			'fields':('is_admin',)
		}),
	)

	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'nickname', 'profile_pic', 'date_of_birth', 
				'use_wheelchair', 'password1', 'password2')}
			),
		)
	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()


admin.site.register(CangoUser, UserAdmin)
admin.site.unregister(Group)