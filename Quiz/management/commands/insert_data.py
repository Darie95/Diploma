from django.core.management.base import BaseCommand
from Quiz.models import Quiz
import requests
import re


class Command(BaseCommand):
    def handle(self, *args, **options):
        response1 = requests.get('http://vk.com/mzgb_minsk')
        result1 = str(response1.text)
        temp1 = re.findall(r'<div class="pp_status">(.*)<div class="basisGroup__buttonsRow">',
                          result1, re.DOTALL)
        if len(temp1)==0:
            temp1='Нет новой информации'
        else:
            temp1=temp1[0]
        temp1_1 = re.sub(r'&quot;', '', temp1).replace('&#33;','')
        temp1_new=re.sub(r'<.*?>','',temp1_1)
        Quiz.objects.filter(id=1).update(fresh=temp1_new)
        response2 = requests.get('http://www.vk.com/fmquiz')
        result2 = str(response2.text)
        temp2 = re.findall(r'<div class="pp_status">(.*)<div class="basisGroup__buttonsRow">',
            result2,re.DOTALL)
        if len(temp2)==0:
            temp2='Нет новой информации'
        else:
            temp2=temp2[0]
        temp2_1 = re.sub(r'&quot;', '', temp2).replace('&#33;','')
        temp2_new=re.sub(r'<.*?>','',temp2_1)
        Quiz.objects.filter(id=2).update(fresh=temp2_new)
        response3 = requests.get('https://vk.com/detectit')
        result3 = str(response3.text)
        temp3 = re.findall(r'<div class="pp_status">(.*)<div class="basisGroup__buttonsRow">',
                           result3, re.DOTALL)
        if len(temp3)==0:
            temp3='Нет новой информации'
        else:
            temp3=temp3[0]
        temp3_1 = re.sub(r'&quot;', '', temp3).replace('&#33;','')
        temp3_new = re.sub(r'<.*?>', '', temp3_1)
        Quiz.objects.filter(id=3).update(fresh=temp3_new)
        response4 = requests.get('https://vk.com/newtonquiz.minsk')
        result4 = str(response4.text)
        temp4 = re.findall(r'<div class="pp_status">(.*)<div class="basisGroup__buttonsRow">',
                           result4, re.DOTALL)
        if len(temp4)==0:
            temp4='Нет новой информации'
        else:
            temp4=temp4[0]
        temp4_1 = re.sub(r'&quot;', '', temp4).replace('&#33;','')
        temp4_new = re.sub(r'<.*?>', '', temp4_1)
        Quiz.objects.filter(id=4).update(fresh=temp4_new)
        response5 = requests.get('https://vk.com/bernard_show')
        result5 = str(response5.text)
        temp5 = re.findall(r'<div class="pp_status">(.*)<div class="basisGroup__buttonsRow">',
                           result5, re.DOTALL)
        if len(temp5)==0:
            temp5='Нет новой информации'
        else:
            temp5=temp5[0]
        temp5_1 = re.sub(r'&quot;', '', temp5).replace('&#33;','')
        temp5_new = re.sub(r'<.*?>', '', temp5_1)
        Quiz.objects.filter(id=5).update(fresh=temp5_new)
        response6 = requests.get('https://vk.com/golovolomkaqz')
        result6 = str(response6.text)
        temp6 = re.findall(r'<div class="pp_status">(.*)</div>',
                           result6, re.DOTALL)
        if len(temp6)==0:
            temp6='Нет новой информации'
        else:
            temp6=temp6[0]
        temp6_1 = re.sub(r'&quot;', '', temp6).replace('&#33;','')
        temp6_new = re.sub(r'<.*?>', '', temp6_1)
        Quiz.objects.filter(id=6).update(fresh=temp6_new)
        response7 = requests.get('https://vk.com/mozg_minsk')
        result7 = str(response7.text)
        temp7 = re.findall(r'<div class="pp_status">(.*)<div class="basisGroup__buttonsRow">',
                           result7, re.DOTALL)
        if len(temp7)==0:
            temp7='Нет новой информации'
        else:
            temp7=temp7[0]
        temp7_1 = re.sub(r'&quot;', '', temp7).replace('&#33;','')
        temp7_new = re.sub(r'<.*?>', '', temp7_1)
        Quiz.objects.filter(id=7).update(fresh=temp7_new)
        response8 = requests.get('https://vk.com/umka.minsk')
        result8 = str(response8.text)
        temp8 = re.findall(r'<div class="pp_status">(.*)<div class="basisGroup__buttonsRow">',
                           result8, re.DOTALL)
        if len(temp8)==0:
            temp8='Нет новой информации'
        else:
            temp8=temp8[0]
        temp8_1 = re.sub(r'&quot;', '', temp8).replace('&#33;','')
        temp8_new = re.sub(r'<.*?>', '', temp8_1)
        Quiz.objects.filter(id=8).update(fresh=temp8_new)
        self.stdout.write(
            self.style.SUCCESS('Successfully update data'))
