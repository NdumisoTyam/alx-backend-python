from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

User = get_user_model()

@login_required
@require_POST
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('account_deleted')  # Replace with your actual redirect target
