from django.core.management.utils import get_random_secret_key
a = get_random_secret_key()
print('~~~~~~~~~' + a + '~~~~~~~~~~~~')