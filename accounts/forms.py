from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """Registration form with email-first signup fields."""
    email = forms.EmailField(
        required=True,
        max_length=100,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#89b83a] outline-none transition-all',
            'placeholder': 'Ваш email'
        })
    )
    first_name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#89b83a] outline-none transition-all',
            'placeholder': "Ваше ім'я"
        })
    )
    last_name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#89b83a] outline-none transition-all',
            'placeholder': 'Ваше прізвище'
        })
    )

    def __init__(self, *args, **kwargs):
        """Customize password widgets and labels."""
        super().__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#89b83a] outline-none transition-all',
            'placeholder': 'Придумайте пароль'
        })
        self.fields['password1'].help_text = ''
        self.fields['password1'].label = 'Password'

        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#89b83a] outline-none transition-all',
            'placeholder': 'Підтвердіть пароль'
        })
        self.fields['password2'].help_text = ''
        self.fields['password2'].label = 'Confirm Password'

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_email(self):
        """Reject duplicate emails before creating a new user."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Цей email вже використовується.')
        return email

    def save(self, commit=True):
        """Persist user while keeping username disabled."""
        user = super().save(commit=False)
        user.username = None
        if commit:
            user.save()
        return user


class CustomUserLoginForm(AuthenticationForm):
    """Login form that authenticates using email and password."""
    username = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#89b83a] outline-none transition-all input-register form-control',
                                      'placeholder': 'Ваш email',})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#89b83a] outline-none transition-all input-register form-control',
                                          'placeholder': 'Ваш пароль'})
    )

    def clean(self):
        """Validate credentials and active account status."""
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('Невірний email або пароль.')
            elif not self.user_cache.is_active:
                raise forms.ValidationError('Цей акаунт деактивовано.')
        return self.cleaned_data


class CustomUserUpdateForm(forms.ModelForm):
    """Profile details update form with read-only email."""
    first_name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'input-register form-control', 'placeholder': "Ваше ім'я"})
    )
    last_name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'input-register form-control', 'placeholder': 'Ваше прізвище'})
    )

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'input-register form-control', 'readonly': 'readonly'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_email(self):
        """Keep the original email unchanged from the model instance."""
        return self.instance.email


class CustomSetPasswordForm(SetPasswordForm):
    """Password reset confirmation form with custom styling."""

    def __init__(self, *args, **kwargs):
        """Apply consistent UI attributes to password fields."""
        super().__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs.update({
            'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#89b83a] outline-none transition-all',
            'placeholder': 'Новий пароль'
        })
        self.fields['new_password1'].label = 'New password'
        self.fields['new_password1'].help_text = ''

        self.fields['new_password2'].widget.attrs.update({
            'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#89b83a] outline-none transition-all',
            'placeholder': 'Підтвердіть новий пароль'
        })
        self.fields['new_password2'].label = 'Confirm a new password'
        self.fields['new_password2'].help_text = ''

class CustomPasswordResetForm(PasswordResetForm):
    """Password reset request form with custom email input styling."""

    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#89b83a] outline-none transition-all',
            'placeholder': 'Ваш email',
            'autocomplete': 'email',
        })
    )