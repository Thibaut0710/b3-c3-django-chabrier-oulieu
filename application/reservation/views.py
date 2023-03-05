from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import *
from django.contrib import messages


def index(request):
  today = datetime.today()
  minDate = today.strftime('%Y-%m-%d')
  deltatime = today + timedelta(days=21)
  strdeltatime = deltatime.strftime('%Y-%m-%d')
  maxDate = strdeltatime
  appointments = Appointment.objects.filter(day__range=[minDate, maxDate]).order_by('day', 'time')
  compteurReservationMilitaire = 0
  compteurReservationCivile = 0
  compteurReservationLoisirSportive = 0
  for evenement in appointments:
    print(evenement.ecoles)
    if evenement.ecoles == "aviationMilitaire":
      compteurReservationMilitaire = compteurReservationMilitaire + 1
    elif evenement.ecoles == "aviationCivile":
      compteurReservationCivile = compteurReservationCivile + 1
    elif evenement.ecoles == "aviationLoisirSportif":
      compteurReservationLoisirSportive = compteurReservationLoisirSportive + 1
    reservationsEcoles = {'Ecole Aviation Militaire': compteurReservationMilitaire,'Ecole Aviation Civile':compteurReservationCivile,"Ecole spécialisé dans l'avation loisir et sportive":compteurReservationLoisirSportive}
  return render(request, "index.html",{"reservationsEcoles":reservationsEcoles})


def reservation(request):
  weekdays = validWeekday(22)
  print(weekdays)

  validateWeekdays = isWeekdayValid(weekdays)

  if request.method == 'POST':
    ecoles = request.POST.get('ecoles')
    day = request.POST.get('day')
    if ecoles == None:
      messages.success(request, "Veuillez séléctionner une ecole !")
      return redirect('reservation')

    request.session['day'] = day
    request.session['ecoles'] = ecoles

    return redirect('horaires')

  return render(request, 'reservation.html', {
    'weekdays': weekdays,
    'validateWeekdays': validateWeekdays,
  })


def horaires(request):
  user = request.user
  times = [
    "8h", "10h", "12h", "14h", "16h", "18h", "20h"
  ]
  today = datetime.now()
  minDate = today.strftime('%Y-%m-%d')
  deltatime = today + timedelta(days=21)
  strdeltatime = deltatime.strftime('%Y-%m-%d')
  maxDate = strdeltatime

  day = request.session.get('day')
  ecoles = request.session.get('ecoles')

  hour = checkTime(times, day)
  if request.method == 'POST':
    time = request.POST.get("time")
    date = dayToWeekday(day)

    if ecoles != None:
      if day <= maxDate and day >= minDate:
        if date == 'Monday' or date == 'Saturday' or date == 'Wednesday':
          if Appointment.objects.filter(day=day).count() < 11:
            if Appointment.objects.filter(day=day, time=time).count() < 1:
              AppointmentForm = Appointment.objects.get_or_create(
                user=user,
                ecoles=ecoles,
                day=day,
                time=time,
              )
              messages.success(request, "Rendez-vous réservé !")
              return redirect('index')
            else:
              messages.success(request, "Cette plage horaire à déja été reservé !")
          else:
            messages.success(request, "Ce jour est déja complet !")
        else:
          messages.success(request, "La date sélectionné est incorrecte !")
      else:
        messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
    else:
      messages.success(request, "Veuillez selectionner un événement !")

  return render(request, 'horaires-reservations.html', {
    'times': hour,
  })


def userPanel(request):
  user = request.user
  appointments = Appointment.objects.filter(user=user).order_by('day', 'time')
  return render(request, 'userPanel.html', {
    'user': user,
    'appointments': appointments,
  })


def removeReservation(request, id):
  Appointment.objects.filter(pk=id).delete()
  return userPanel(request)


def userUpdate(request, id):
  appointment = Appointment.objects.get(pk=id)
  userdatepicked = appointment.day
  today = datetime.today()
  minDate = today.strftime('%d-%m-%Y')

  delta24 = (userdatepicked).strftime('%d-%m-%Y') >= (today + timedelta(days=1)).strftime('%d-%m-%Y')
  weekdays = validWeekday(22)

  validateWeekdays = isWeekdayValid(weekdays)

  if request.method == 'POST':
    ecoles = request.POST.get('ecoles')
    day = request.POST.get('day')

    request.session['day'] = day
    request.session['ecoles'] = ecoles

    return redirect('userUpdateSubmit', id=id)

  return render(request, 'userUpdate.html', {
    'weekdays': weekdays,
    'validateWeekdays': validateWeekdays,
    'delta24': delta24,
    'id': id,
  })


def userUpdateSubmit(request, id):
  user = request.user
  times = [
    "8h", "10h", "12h", "14h", "16h", "18h", "20h"
  ]
  today = datetime.now()
  minDate = today.strftime('%Y-%m-%d')
  deltatime = today + timedelta(days=21)
  strdeltatime = deltatime.strftime('%d-%m-%Y')
  maxDate = strdeltatime

  day = request.session.get('day')
  ecoles = request.session.get('ecoles')

  hour = checkEditTime(times, day, id)
  appointment = Appointment.objects.get(pk=id)
  userSelectedTime = appointment.time
  if request.method == 'POST':
    time = request.POST.get("time")
    date = dayToWeekday(day)

    if ecoles != None:
      if day <= maxDate and day >= minDate:
        if date == 'Monday' or date == 'Saturday' or date == 'Wednesday':
          if Appointment.objects.filter(day=day).count() < 11:
            if Appointment.objects.filter(day=day, time=time).count() < 1 or userSelectedTime == time:
              AppointmentForm = Appointment.objects.filter(pk=id).update(
                user=user,
                ecoles=ecoles,
                day=day,
                time=time,
              )
              messages.success(request, "Rendez-vous modifié !")
              return redirect('index')
            else:
              messages.success(request, "Cette plage horaire à déja été reservé !")
          else:
            messages.success(request, "Ce jour est déja complet !")
        else:
          messages.success(request, "La date sélectionné est incorrecte ! ")
      else:
        messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
    else:
      messages.success(request, "Veuillez selectionner un événement !")
    return redirect('userPanel')

  return render(request, 'userUpdateSubmit.html', {
    'times': hour,
    'id': id,
  })


def ecolesReservations(request):
  today = datetime.today()
  minDate = today.strftime('%Y-%m-%d')
  deltatime = today + timedelta(days=21)
  strdeltatime = deltatime.strftime('%Y-%m-%d')
  maxDate = strdeltatime
  items = Appointment.objects.filter(day__range=[minDate, maxDate]).order_by('day', 'time')

  return render(request, 'ecoles-reservations.html', {
    'items': items,
  })


def dayToWeekday(x):
  z = datetime.strptime(x, "%Y-%m-%d")
  y = z.strftime('%A')
  return y


def validWeekday(days):
  today = datetime.now()
  weekdays = []
  for i in range(0, days):
    x = today + timedelta(days=i)
    y = x.strftime('%A')
    if y == 'Monday' or y == 'Saturday' or y == 'Wednesday':
      weekdays.append(x.strftime('%Y-%m-%d'))
  return weekdays


def isWeekdayValid(x):
  validateWeekdays = []
  for j in x:
    if Appointment.objects.filter(day=j).count() < 7:
      validateWeekdays.append(j)
  return validateWeekdays


def checkTime(times, day):
  x = []
  for k in times:
    if Appointment.objects.filter(day=day, time=k).count() < 1:
      x.append(k)
  return x


def checkEditTime(times, day, id):
  x = []
  appointment = Appointment.objects.get(pk=id)
  time = appointment.time
  for k in times:
    if Appointment.objects.filter(day=day, time=k).count() < 1 or time == k:
      x.append(k)
  return x
