from registration.forms import RegistrationForm
from django.contrib.localflavor.br.forms import BRCPFField

class UserRegistrationForm(RegistrationForm):
    cpf = BRCPFField()
