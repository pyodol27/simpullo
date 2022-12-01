from django.shortcuts import render, redirect
import json
from .models import lcl, air, fcl, airother
from django.http import JsonResponse
from django.db.models import Q
# Create your views here.
def index(request):
    return render(request, 'index.html')

def quotation(request):
    return render(request, 'quotation.html')

def lclinfo(request):
    info = lcl.objects.all().order_by('id')
    context = {'info' : info}
    return render(request, 'lclinfo.html', context)

def airinfo(request):
    info = air.objects.all().order_by('id')
    context = {'info' : info}
    return render(request, 'airinfo.html', context)

def airotherinfo(request):
    info = airother.objects.all().order_by('id')
    context = {'info' : info}
    return render(request, 'airotherinfo.html', context)

def fclinfo(request):
    info = fcl.objects.all().order_by('id')
    context = {'info' : info}
    return render(request, 'fclinfo.html', context)

def showquote(request):
    jsonObject = json.loads(request.body)
    origin = jsonObject.get('origin')
    dest = jsonObject.get('dest')
    incoterms = jsonObject.get('incoterms')
    cbm = jsonObject.get('cbm')
    kg = jsonObject.get('kg')
    
    q= Q(origin = origin, dest = dest)
    if incoterms == 'EXW':
        q.add(Q(chargeAt = 'freight')|Q(chargeAt = 'destination')|Q(chargeAt = 'origin'), q.AND)
        #rate = lcl.objects.filter(q)
    elif incoterms == 'FOB':
        q.add(Q(chargeAt = 'freight')|Q(chargeAt = 'destination'), q.AND)
        #rate = lcl.objects.filter(q)
    elif incoterms == 'DAP':
        q.add(Q(chargeAt = 'freight')|Q(chargeAt = 'destination')|Q(chargeAt = 'origin'), q.AND)
        #rate = lcl.objects.filter(q)
    elif incoterms == 'CFR':
        q.add(Q(chargeAt = 'freight')|Q(chargeAt = 'origin'), q.AND)
        #rate = lcl.objects.filter(q)
        
    rate = lcl.objects.filter(q)
    
    print(rate[0].cur) #첫번재 놈의 통화s
    print(rate[0].rate)
    print(rate[0].unit)
    
    #lcl.object에있는 데이터 중 origin과 dest값이 같은 xxxxxx
    #ver2 콘솔사별로 뽑고, 비교, 
    lcltotal = 0
    for i in range(0, len(rate)):
        if rate[i].cur == 'USD':
            if rate[i].unit == 'R/TON':
                total = float(rate[i].rate) * 1400  * float(cbm)
            elif rate[i].unit == 'BL':
                total = float(rate[i].rate) * 1400
            elif rate[i].unit == 'KG':
                total = float(rate[i].rate) * 1400  * float(kg)
        else:
            if rate[i].unit == 'R/TON':
                total = float(rate[i].rate) * float(cbm)
            elif rate[i].unit == 'BL':
                total = float(rate[i].rate)
            elif rate[i].unit == 'KG':
                total = float(rate[i].rate) * float(kg)
                
        lcltotal = lcltotal + total
        
    print(lcltotal)
    
    context = {'lcltotal' : lcltotal}


    return JsonResponse(context)



def lcladd(request):
    jsonObject = json.loads(request.body)
    
    lcladd = lcl.objects.create(
        origin = jsonObject.get('origin'),
        dest = jsonObject.get('dest'),
        consol = jsonObject.get('consol'),
        name = jsonObject.get('name'),
        cur = jsonObject.get('cur'), 
        rate = jsonObject.get('rate'), 
        unit = jsonObject.get('unit'), 
        chargeAt = jsonObject.get('chargeAt'),
        group = jsonObject.get('group'), 
    )
    lcladd.save()
    id = lcladd.id
    context = {
        'id' : id
    }
    
    return JsonResponse(context)

def airadd(request):
    jsonObject = json.loads(request.body)
    
    airadd = air.objects.create(
        origin = jsonObject.get('origin'),
        dest = jsonObject.get('dest'),
        consol = jsonObject.get('consol'),
        line = jsonObject.get('line'), 
        cur= jsonObject.get('cur'), 
        minimum = jsonObject.get('minimum'), 
        normal = jsonObject.get('normal'),
        over45 = jsonObject.get('over45'), 
        over100 = jsonObject.get('over100'), 
        over300 = jsonObject.get('over300'), 
        over500 = jsonObject.get('over500'), 
        over1000 = jsonObject.get('over1000'), 
        fsc = jsonObject.get('fsc'), 
        skdl = jsonObject.get('skdl'), 
        via = jsonObject.get('via'), 
    )
    airadd.save()
    id = airadd.id
    context = {
        'id' : id
    }
    
    return JsonResponse(context)


def fcladd(request):
    jsonObject = json.loads(request.body)
    
    fcladd = fcl.objects.create(
        origin = jsonObject.get('origin'),
        dest = jsonObject.get('dest'),
        line = jsonObject.get('line'),
        name = jsonObject.get('name'), 
        cur = jsonObject.get('cur'), 
        rate = jsonObject.get('rate'), 
        unit = jsonObject.get('unit'),
        chargeAt = jsonObject.get('chargeAt'),
        ttime = jsonObject.get('ttime'),
        vaildity = jsonObject.get('vaildity'),
        group = jsonObject.get('group'), 
    )
    fcladd.save()
    id = fcladd.id
    context = {
        'id' : id
    }
    
    return JsonResponse(context)

def fcldelete(request):
    jsonObject = json.loads(request.body)
    fcldelete = fcl.objects.get(id=jsonObject.get('id'))
    fcldelete.delete()
    context = {
        'success' : 'success'
    }
    return JsonResponse(context)

def fclupdate(request):
    jsonObject = json.loads(request.body)
    fclupdate = fcl.objects.filter(id=jsonObject.get('id'))
    fclupdate.update(
        origin = jsonObject.get('origin'),
        dest = jsonObject.get('dest'),
        line = jsonObject.get('line'),
        name = jsonObject.get('name'), 
        cur = jsonObject.get('cur'), 
        rate = jsonObject.get('rate'), 
        unit = jsonObject.get('unit'),
        chargeAt = jsonObject.get('chargeAt'),
        ttime = jsonObject.get('ttime'),
        vaildity = jsonObject.get('vaildity'),
        group = jsonObject.get('group'),
    )
    context = {'success' : 'success'}
    return JsonResponse(context)

def lcldelete(request):
    jsonObject = json.loads(request.body)
    lcldelete = lcl.objects.get(id=jsonObject.get('id'))
    lcldelete.delete()
    context2 = {
        'success' : 'success'
    }
    return JsonResponse(context2)

def lclupdate(request):
    jsonObject = json.loads(request.body)
    lclupdate = lcl.objects.filter(id=jsonObject.get('id'))
    lclupdate.update(
        origin = jsonObject.get('origin'),
        dest = jsonObject.get('dest'),
        consol = jsonObject.get('consol'),
        name = jsonObject.get('name'),
        cur = jsonObject.get('cur'), 
        rate = jsonObject.get('rate'), 
        unit = jsonObject.get('unit'), 
        chargeAt = jsonObject.get('chargeAt'),
        group = jsonObject.get('group'),
    )
    context3 = {'success' : 'success'}
    return JsonResponse(context3)

def airupdate(request):
    jsonObject = json.loads(request.body)
    airupdate = air.objects.filter(id=jsonObject.get('id'))
    airupdate.update(
        consol = jsonObject.get('consol'),
        line = jsonObject.get('line'),
        cur = jsonObject.get('cur'),
        minimum = jsonObject.get('minimum'), 
        normal = jsonObject.get('normal'), 
        over45 = jsonObject.get('over45'),
        over100 = jsonObject.get('over100'),
        over300 = jsonObject.get('over300'),
        over500 = jsonObject.get('over500'),
        over1000 = jsonObject.get('over1000'),
        fsc = jsonObject.get('fsc'),
        skdl = jsonObject.get('skdl'),
        via = jsonObject.get('via'),
    )
    context = {'airupdate' : 'airupdate'}
    return JsonResponse(context)

def airdelete(request):
    jsonObject = json.loads(request.body)
    airdelete = air.objects.get(id=jsonObject.get('id'))
    airdelete.delete()
    context = {
        'success' : 'success'
    }
    return JsonResponse(context)

def airotheradd(request):
    jsonObject = json.loads(request.body)
    
    airotheradd = airother.objects.create(
        origin = jsonObject.get('origin'),
        dest = jsonObject.get('dest'),
        name = jsonObject.get('name'),
        cur = jsonObject.get('cur'), 
        rate = jsonObject.get('rate'), 
        unit = jsonObject.get('unit'), 
        chargeAt = jsonObject.get('chargeAt'),
        group = jsonObject.get('group'), 
    )
    airotheradd.save()
    id = airotheradd.id
    context = {
        'id' : id
    }
    
    return JsonResponse(context)

def airotherdelete(request):
    jsonObject = json.loads(request.body)
    airotherdelete = airother.objects.get(id=jsonObject.get('id'))
    airotherdelete.delete()
    context = {
        'success' : 'success'
    }
    return JsonResponse(context)

def airotherupdate(request):
    jsonObject = json.loads(request.body)
    airotherupdate = airother.objects.filter(id=jsonObject.get('id'))
    airotherupdate.update(
        origin = jsonObject.get('origin'),
        dest = jsonObject.get('dest'),
        name = jsonObject.get('name'),
        cur = jsonObject.get('cur'), 
        rate = jsonObject.get('rate'), 
        unit = jsonObject.get('unit'), 
        chargeAt = jsonObject.get('chargeAt'),
        group = jsonObject.get('group'),
    )
    context3 = {'success' : 'success'}
    return JsonResponse(context3)