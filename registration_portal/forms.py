from django import forms
from registration_portal.models import Team

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('team_name', 'team_member_one', 'team_member_two')