# Download GeoLite2-City and GeoLite2-Country as GZIP
# https://www.maxmind.com/en/accounts/489209/geoip/downloads

# Read the top paragraph for installation
# https://docs.djangoproject.com/en/3.1/ref/contrib/gis/geoip2/

from django.contrib.auth.signals import user_logged_in
from .models import LoginHistory
from django.contrib.gis.geoip2 import GeoIP2
from django.dispatch import Signal
import re
from datetime import timedelta

g = GeoIP2()
pattern = re.compile(r'\((.+?)\)')  # pattern to grab os/system architecture
def create_login_info(sender, request, user, **kwargs):
    user_agent = request.META.get('HTTP_USER_AGENT')
    ip = request.META.get('REMOTE_ADDR', None)
    try:
        data = g.city(ip)
    except Exception as e:
        # in dictionary if a particular key is not found and you are looking up with .get() method then it will return None
        data = {}
        print(e)
    LoginHistory.objects.create(
        user = user,
        longitude = data.get('longitude'),
        latitude = data.get('latitude'),
        ip = ip,
        city = data.get('city'),
        postal_code = data.get('postal_code'),
        country_name = data.get('country_name'),
        country_code=data.get('country_code'),
        continent_name=data.get('continent_name'),
        continent_code=data.get('continent_code'),
        timezone = data.get('time_zone'),
        is_in_european_union=data.get('is_in_european_union'),
        user_agent = user_agent,
        device = re.findall(pattern,user_agent)[0]
    )
user_logged_in.connect(create_login_info)

def create_membership(sender, user, transaction, **kwargs):
    member_for = timedelta(days=30)
    time_of_transaction = transaction.status_history[0].timestamp,
    print(time_of_transaction[0]+member_for)
    sender.objects.create(
        user = user,
        braintree_id = transaction.id,
        created = time_of_transaction[0],
        expiry = time_of_transaction[0] + member_for
    )

create_membership_signal = Signal()
create_membership_signal.connect(create_membership, dispatch_uid='create_member_signal')


