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
    #print(rate[0].cur) #첫번재 놈의 통화
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
    
    
    fclrate = fcl.objects.filter(q)
    twototal = 0
    for i in range(0, len(fclrate)):
        if fclrate[i].cur == 'USD':
            if fclrate[i].unit == '20FT':
                total = float(fclrate[i].rate)* 1400
            elif fclrate[i].unit == 'BL':
                total = float(fclrate[i].rate)* 1400
        else:
            if fclrate[i].unit == '20FT':
                total = float(fclrate[i].rate)
            elif fclrate[i].unit == 'BL':
                total = float(fclrate[i].rate)
        
        twototal = twototal + total
    print(twototal)
  #  
  #  fototal=0
  #  for a in range(0, len(fclrate)):
  #      if fclrate[a].cur == 'USD':
  #          if fclrate[a].unit == '40FT':
  #              total = float(fclrate[a].rate)* 1400
  #          elif fclrate[a].unit == 'BL':
  #              total = float(fclrate[a].rate)* 1400
  #      else:
  #          if fclrate[a].unit == '40FT':
  #              total = float(fclrate[a].rate)
  #          elif fclrate[a].unit == 'BL':
  #              total = float(fclrate[a].rate)
  #      
  #      fototal = fototal + total
  #  print(fototal)

    #print(lcltotal)
    if float(cbm) * 167 > float(kg) :
        cw =  float(cbm)*167
    else :
        cw = float(kg)
    
    ao = airother.objects.filter(origin = origin, dest = dest)
    #print(ao[0].cur)
    othertotal = 0
    
    for a in range(0, len(ao)):
        if ao[a].cur == 'USD':
            if ao[a].unit == 'BL':
                total = float(ao[a].rate) * 1400
            elif ao[a].unit == 'KG':
                total = float(ao[a].rate) * 1400  * float(cw)
        else:
            if ao[a].unit == 'BL':
                total = float(ao[a].rate)
            elif ao[a].unit == 'KG':
                total = float(ao[a].rate) * float(cw)
    
        othertotal = othertotal + total
    
        
        
    
    afc = air.objects.filter(origin = origin, dest = dest)
    
    afclist =[]
    for i in range(0, len(afc)):
        if afc[i].cur == 'USD':
            if cw < 45 : #nomal
                if cw*(float(afc[i].normal)+float(afc[i].fsc))*1400 < float(afc[i].minimum)*1400 :
                    afclist.append(float(afc[i].minimum)*1400)  
                else:
                    if cw*(float(afc[i].normal)+float(afc[i].fsc))*1400 > 45*(float(afc[i].over45)+float(afc[i].fsc))*1400 :
                        afclist.append(float(afc[i].over45)*1400*45)
                    else :
                        afclist.append(cw*(float(afc[i].normal)+float(afc[i].fsc))*1400)
                        
            elif cw < 100 : #+45
                if cw*(float(afc[i].over45)+float(afc[i].fsc))*1400 < float(afc[i].minimum)*1400 :
                    afclist.append(float(afc[i].minimum)*1400)
                else :
                    if cw*(float(afc[i].over45)+float(afc[i].fsc))*1400 > 100*(float(afc[i].over100)+float(afc[i].fsc))*1400 :
                        afclist.append(float(afc[i].over100)*1400*100)
                    else:
                        afclist.append(cw*(float(afc[i].over45)+float(afc[i].fsc))*1400)
                
            elif cw < 300 : #+100
                if cw*(float(afc[i].over100)+float(afc[i].fsc))*1400 < float(afc[i].minimum)*1400 :
                    afclist.append(float(afc[i].minimum)*1400)
                else :
                    if cw*(float(afc[i].over100)+float(afc[i].fsc))*1400 > 300*(float(afc[i].over300)+float(afc[i].fsc))*1400 :
                        afclist.append(float(afc[i].over300)*1400*300)
                    else:
                        afclist.append(cw*(float(afc[i].over100)+float(afc[i].fsc))*1400)
                
            elif cw < 500 :
                if cw*(float(afc[i].over300)+float(afc[i].fsc))*1400 < float(afc[i].minimum)*1400 :
                    afclist.append(float(afc[i].minimum)*1400)
                else :
                    if cw*(float(afc[i].over300)+float(afc[i].fsc))*1400 > 500*(float(afc[i].over500)+float(afc[i].fsc))*1400 :
                        afclist.append(float(afc[i].over500)*1400*500)
                    else:
                        afclist.append(cw*(float(afc[i].over300)+float(afc[i].fsc))*1400)
                
            elif cw < 1000 :
                if cw*(float(afc[i].over500)+float(afc[i].fsc))*1400 < float(afc[i].minimum)*1400 :
                    afclist.append(float(afc[i].minimum)*1400)
                else :
                    if cw*(float(afc[i].over500)+float(afc[i].fsc))*1400 > 1000*(float(afc[i].over1000)+float(afc[i].fsc))*1400 :
                        afclist.append(float(afc[i].over1000+float(afc[i].fsc))*1400*1000)
                    else:
                        afclist.append(cw*(float(afc[i].over500)+float(afc[i].fsc))*1400)
                
            elif cw > 1000 :
                if cw*(float(afc[i].over1000)+float(afc[i].fsc))*1400 > float(afc[i].minimum)*1400 :
                    afclist.append(cw*(float(afc[i].over1000) + float(afc[i].fsc))*1400)
                else :
                    afclist.append(float(afc[i].minimum)*1400)
            
        elif afc[i].cur == 'KRW':
            if cw < 45 :
                if cw*(float(afc[i].normal)+float(afc[i].fsc)) < float(afc[i].minimum) :
                        afclist.append(float(afc[i].minimum))  
                else:
                    if cw*(float(afc[i].normal)+float(afc[i].fsc)) > 45*(float(afc[i].over45)+float(afc[i].fsc)) :
                        afclist.append(float(afc[i].over45)*45)
                    else :
                        afclist.append(cw*(float(afc[i].normal)+float(afc[i].fsc)))
                    
            elif cw < 100 :
                if cw*(float(afc[i].over45)+float(afc[i].fsc)) < float(afc[i].minimum) :
                    afclist.append(float(afc[i].minimum))
                else :
                    if cw*(float(afc[i].over45)+float(afc[i].fsc)) > 100*(float(afc[i].over100)+float(afc[i].fsc))*1400 :
                        afclist.append(float(afc[i].over100)*100)
                    else:
                        afclist.append(cw*(float(afc[i].over45)+float(afc[i].fsc)))
            
            elif cw < 300 :
                if cw*(float(afc[i].over100)+float(afc[i].fsc)) < float(afc[i].minimum) :
                    afclist.append(float(afc[i].minimum))
                else :
                    if cw*(float(afc[i].over100)+float(afc[i].fsc)) > 300*(float(afc[i].over300)+float(afc[i].fsc)) :
                        afclist.append(float(afc[i].over300)*300)
                    else:
                        afclist.append(cw*(float(afc[i].over100)+float(afc[i].fsc)))

            elif cw < 500 :
                if cw*(float(afc[i].over300)+float(afc[i].fsc)) < float(afc[i].minimum) :
                    afclist.append(float(afc[i].minimum))
                else :
                    if cw*(float(afc[i].over300)+float(afc[i].fsc)) > 500*(float(afc[i].over500)+float(afc[i].fsc)) :
                        afclist.append(float(afc[i].over500)*500)
                    else:
                        afclist.append(cw*(float(afc[i].over300)+float(afc[i].fsc)))
                    
            elif cw < 1000 :
                if cw*(float(afc[i].over500)+float(afc[i].fsc)) < float(afc[i].minimum) :
                    afclist.append(float(afc[i].minimum))
                else :
                    if cw*(float(afc[i].over500)+float(afc[i].fsc)) > 1000*(float(afc[i].over1000)+float(afc[i].fsc)) :
                        afclist.append(float(afc[i].over1000+float(afc[i].fsc))*1000)
                    else:
                        afclist.append(cw*(float(afc[i].over500)+float(afc[i].fsc)))
  
            elif cw > 1000 :
                if cw*(float(afc[i].over1000)+float(afc[i].fsc)) > float(afc[i].minimum) :
                    afclist.append(cw*(float(afc[i].over1000) + float(afc[i].fsc)))
                else :
                    afclist.append(float(afc[i].minimum))
            
    airtotal = othertotal + min(afclist)
   
        
    context = {'lcltotal' : lcltotal, 'airtotal' : airtotal, 'twototal' : twototal}


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