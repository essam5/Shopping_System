from django.contrib.auth import get_user_model, authenticate
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth.models import Permission
from django.utils.translation import ugettext_lazy as _
from .models import Address, Profile
from rest_framework import serializers
from django.contrib.auth.forms import SetPasswordForm
from django.conf import settings
from drf_extra_fields.fields import Base64ImageField

# Get the UserModel
UserModel = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    gender = serializers.SerializerMethodField()
    profile_picture = Base64ImageField()

    def get_gender(self, obj):
        return obj.get_gender_display()

    class Meta:
        model = Profile
        fields = ["user", "profile_picture", "phone_number", "gender", "about"]



class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(source="profile.profile_picture")
    gender = serializers.CharField(source="profile.gender")
    about = serializers.CharField(source="profile.about")
    phone_number = PhoneNumberField(source="profile.phone_number")
    online = serializers.BooleanField(source="profile.online")

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "online",
            "last_login",
            "gender",
            "about",
            "phone_number",
            "profile_picture",
            "is_active",
        ]


class UserMiniSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(source="profile.profile_picture")
    gender = serializers.CharField(source="profile.gender")
    phone_number = PhoneNumberField(source="profile.phone_number")

    class Meta:
        model = get_user_model()
        fields = ["username", "profile_picture", "gender", "phone_number"]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ["updated"]


class CreateAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ["primary", "user"]


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["name", "codename", "content_type"]


class UserPermissionretriveSerializer(serializers.ModelSerializer):
    user_permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = UserModel
        fields = ("user_permissions",)


class UserPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("user_permissions",)


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    def __init__(self, *args, **kwargs):
        self.old_password_field_enabled = getattr(
            settings, "OLD_PASSWORD_FIELD_ENABLED", False
        )
        self.logout_on_password_change = getattr(
            settings, "LOGOUT_ON_PASSWORD_CHANGE", False
        )
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)

        self.request = self.context.get("request")
        self.user = getattr(self.request, "user", None)

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.old_password_field_enabled,
            self.user,
            not self.user.check_password(value),
        )

        if all(invalid_password_conditions):
            raise serializers.ValidationError("Invalid password")
        return value

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        old_password_match = (
            self.user,
            attrs["old_password"] == attrs["new_password1"],
        )

        if all(old_password_match):
            raise serializers.ValidationError(
                "your new password matching with old password"
            )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        self.set_password_form.save()
        if not self.logout_on_password_change:
            from django.contrib.auth import update_session_auth_hash

            update_session_auth_hash(self.request, self.user)
