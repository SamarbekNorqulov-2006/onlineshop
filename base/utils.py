import re
from rest_framework.exceptions import ValidationError

email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
phone_regex = re.compile(r'\+998(90|91|92|93|94|95|98|99|33|97|71)\d{7}$')

def email_phone_regex(user_input):
    if re.fullmatch(email_regex, user_input):
        return 'email'
    
    elif re.fullmatch(phone_regex, user_input):
        return 'phone'
    
    else:
        raise ValidationError("Siz xato email yoki telifon raqam kiritdingiz")