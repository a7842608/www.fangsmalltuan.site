
from django.core import signing
from authorization.models import Token


def token_check(token):
    '''token验证'''
    try:
        src = signing.b64_decode(token.encode()).decode()
        dat = signing.b64_decode(src.encode()).decode()
        stk = Token.objects.get(id=1).token
        if dat != stk:
            return 'False'
        else:
            return 'True'
    except :
        return 'False'
