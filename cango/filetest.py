import os, sys, django
import fnmatch
sys.path.append("/cango/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cango.settings")
from django.conf import settings
django.setup()

from bfm.models import Place
from customUserModel.models import CangoUser
from django.db.models import Q

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)

PIC_BASE_DIR = os.path.join('/home/cango/application/cango/', 'media/naver/11ganghyunwoo')
print(PIC_BASE_DIR)

num = 0
result = []
picture = ['p_extra_pic1', 'p_extra_pic2', 'p_extra_pic3', 'p_extra_pic4', 'p_extra_pic5']
for file in os.listdir(PIC_BASE_DIR):
    try:
        if Place.objects.filter(Q(name__contains=file.split('_')[3]) & Q(user__id=65)).exists():
            if len(Place.objects.filter(Q(name__contains=file.split('_')[3]) & Q(user__id=65))) == 1:
                place = Place.objects.filter(Q(name__contains=file.split('_')[3]) & Q(user__id=65))[0]
                result.append(place)
                for p in picture:
                    print("p : ", type(getattr(place, p)), "file :", file)
                    if bool(getattr(place, p)) is False:
                        print("save : ", file)
                        setattr(place, p,'naver/10boram/' + file)
                        place.save()
                        break;
    except Exception as e:
        print("error",e)


result_set = set(result)
print("length:", len(result_set))
for name in result_set:
    print("name:", name)   
