from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = 'accounts:login'
    def test_func(self):
        return self.request.user.is_staff
