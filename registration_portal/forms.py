from django import forms
from registration_portal.models import Team

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('leader', 'leader_email', 'leader_profilephoto_url', 'team_name', 'team_member_one', 'team_member_two')
        extra_kwargs = {
            'leader' : {'read_only' : True},
            'leader_email' : {'read_only' : True},
            'leader_profilephoto_url' : {'read_only' : True}
        }