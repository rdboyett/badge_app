import json
import csv
import re

from django.shortcuts import render, render_to_response, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from directory_app.models import UserInfo, UserAdmin
from badge_app.models import Badge, BadgeUser
from google_login.models import GoogleUserInfo


import logging
log = logging.getLogger(__name__)






@login_required
def badgeManager(request):
    if UserAdmin.objects.filter(email=request.user.email):
        userAdmin = True
    else:
        userAdmin = False
    
    userInfo = UserInfo.objects.all().order_by('lastName')
    badges = Badge.objects.all().order_by('name')
    
    args = {
        'userAdmin':userAdmin,
        'user':request.user,
        'userInfo':userInfo,
        'badgeManage':True,
        'badges':badges,
    }
    args.update(csrf(request))
        
    return render_to_response('badge_app/badgeManager.html', args )






@csrf_exempt
def checkSessionLogin(request):
    if request.method == 'POST':
        bLogin = request.POST["bLogin"].strip()
        
        data = {'success':'success'}
        
        if bLogin == 'True':
            if 'googleExtension_id' in request.session:
                google_id = request.session['googleExtension_id']
                if UserInfo.objects.filter(google_id=google_id):
                    userInfo = UserInfo.objects.get(google_id=google_id)
                    googleUserInfo = GoogleUserInfo.objects.get(google_id=google_id)
                
                    data['user'] = 'loggedIn'
		    data['google_id'] = userInfo.google_id
                    data['firstName'] = userInfo.firstName
                    data['lastName'] = userInfo.lastName
                    data['school'] = userInfo.school
                    data['grade'] = userInfo.grade
                    data['job'] = userInfo.job
                    data['subject'] = userInfo.subject
                    data['roomNumber'] = userInfo.roomNumber
                    data['phoneExtension'] = userInfo.phoneExtension
                    data['picture'] = googleUserInfo.googleAvatar
                    
                    # for testing purposes
                    #request.session.delete()
                    
                else:
                    data = {'error': "no user in system",}
            else:
                data = {'error': "no session id",}
        else:
            data = {'error': "no login password",}
    else:
        data = {'error': "no post made",}
        
            
    return HttpResponse(json.dumps(data))






@csrf_exempt
def checkUser(request):
    if request.method == 'POST':
        google_id = request.POST["google_id"]
        firstName = request.POST["first_name"]
        lastName = request.POST["last_name"]
        google_email = request.POST["email"]
        picture = request.POST["picture"]
        
        data = {'success':'success'}
        
        emailEnding = google_email.split("@")[1]
        userName = "@"+google_email.split("@")[0]
        
        if User.objects.filter(email=google_email):
            # Make sure that the e-mail is unique.
            user = User.objects.get(email=google_email)
            #userInfo = UserInfo.objects.get(user=user)
        else:
            if 'alvaradoisd.net' in emailEnding:
                if 'student' in emailEnding:
                    data = {'error': "Please sign in with an Alvarado ISD Employee Email Account.",}
                    return HttpResponse(json.dumps(data))
                else:
                    bTeacher = True
                
                    user = User.objects.create(
                        username = userName,
                        first_name = firstName,
                        last_name = lastName,
                        email = google_email,
                        password = 'password',
                    )
                    
                    data['account'] = 'created'
            else:
                data = {'error': "Please sign in with your Alvarado ISD account.",}
                return HttpResponse(json.dumps(data))
        
        if UserInfo.objects.filter(email=google_email):
	    userInfo = UserInfo.objects.get(google_id=google_id)
        else:
            userInfo = UserInfo.objects.create(
                user = user,
                google_id = google_id,
                lastName = lastName,
                firstName = firstName,
                email=google_email,
            )
            
            
        # create Badge user 
        if BadgeUser.objects.filter(google_id=google_id):
            badgeUser = BadgeUser.objects.get(google_id=google_id)
        else:
            badgeUser = BadgeUser.objects.create(
                user = user,
                google_id = google_id,
            )
            
        # create google user 
        #Check to see if a google account has been setup yet
        if GoogleUserInfo.objects.filter(google_id=google_id):
            googleUserInfo = GoogleUserInfo.objects.get(google_id=google_id)
        else:
            googleUserInfo = GoogleUserInfo.objects.create(
                user = user,
                google_id = google_id,
                googleAvatar = picture,
            )
        
        
        data['user'] = 'loggedIn'
        
        
    else:
        data = {
            'error': "There was an error posting this request. Please try again.",
        }
            
    return HttpResponse(json.dumps(data))






@login_required
def createBadge(request):
    if request.method == 'POST':
        name = request.POST["name"].strip().title()
        link = request.POST["link"].strip()
        imageurl = request.POST["imageurl"].strip()
        
        if Badge.objects.filter(name=name):
            data = {'error':'Sorry, that name already exists.'}
        else:
            Badge.objects.create(
                name=name,
                link=link,
                imageURL=imageurl,
            )
            data = {'success':'success'}
        
        
    else:
        data = {
            'error': "There was an error posting this request. Please try again.",
        }
            
    return HttpResponse(json.dumps(data))




@csrf_exempt
def badgeInfo(request):
    if request.method == 'POST':
        badgeID = request.POST["badgeID"].strip()
        
        if Badge.objects.filter(id=badgeID):
            badge = Badge.objects.get(id=badgeID)
            data = {
                'badgeName':badge.name,
                'badgeLink':badge.link,
                'badgeImageURL':badge.imageURL,
                }
        else:
            data = {'error':'Sorry, that badge does not exist.'}
        
    else:
        data = {
            'error': "There was an error posting this request. Please try again.",
        }
            
    return HttpResponse(json.dumps(data))






@login_required
def editBadge(request):
    if request.method == 'POST':
        badgeID = request.POST["badge"].strip()
        name = request.POST["name"].strip().title()
        link = request.POST["link"].strip()
        imageurl = request.POST["imageurl"].strip()
        
        if Badge.objects.filter(id=badgeID):
            badge = Badge.objects.get(id=badgeID)
            badge.name=name
            badge.link=link
            badge.imageURL=imageurl
            badge.save()
            data = {'success':'success'}
        else:
            data = {'error':'Sorry, that badge does not exist.'}
        
    else:
        data = {
            'error': "There was an error posting this request. Please try again.",
        }
            
    return HttpResponse(json.dumps(data))





@login_required
def awardBadge(request):
    if request.method == 'POST':
        addOrRemove = request.POST["addOrRemove"]
        badgeID = request.POST["badge"].strip()
        userInfoID = request.POST["name"].strip()
        
        if Badge.objects.filter(id=badgeID):
            badge = Badge.objects.get(id=badgeID)
        else:
            data = {'error':'Sorry, that badge does not exist.'}
            
        if UserInfo.objects.filter(id=userInfoID):
            userInfo = UserInfo.objects.get(id=userInfoID)
            
            if BadgeUser.objects.filter(user=userInfo.user):
                badgeUser = BadgeUser.objects.get(user=userInfo.user)
            else:
                badgeUser = BadgeUser.objects.create(
                    user = userInfo.user,
                    google_id = userInfo.google_id,
                )
                
            if badge:
                if addOrRemove=='add':
                    badgeUser.badges.add(badge)
                else:
                    badgeUser.badges.remove(badge)
                data = {'success':'success'}
                
                
        else:
            data = {'error':'Sorry, that user does not exist.'}
            
            
        
    else:
        data = {
            'error': "There was an error posting this request. Please try again.",
        }
            
    return HttpResponse(json.dumps(data))








@csrf_exempt
def viewUserBadges(request):
    if request.method == 'POST':
        userInfoID = request.POST["userInfoID"].strip()
        
        if UserInfo.objects.filter(id=userInfoID):
            userInfo = UserInfo.objects.get(id=userInfoID)
            
            if BadgeUser.objects.filter(user=userInfo.user):
                badgeUser = BadgeUser.objects.get(user=userInfo.user)
            else:
                badgeUser = BadgeUser.objects.create(
                    user = userInfo.user,
                    google_id = userInfo.google_id,
                )
                
        else:
            userInfo = False
            
            
        args = {
            'userInfo':userInfo,
            'badgeUser':badgeUser
        }
        args.update(csrf(request))
            
        return render_to_response('badge_app/badgeDisplay.html', args )
        
    else:
        return HttpResponse('error')
            




@csrf_exempt
def getBadgesExtension(request):
    if request.method == 'POST':
        google_id = request.POST["google_id"].strip()
        
        if BadgeUser.objects.filter(google_id=google_id):
            badgeUser = BadgeUser.objects.get(google_id=google_id)
            
            badges = badgeUser.badges.all().order_by('name')
            
            badgesList = []
            for badge in badges:
                badgeDict = {
                    'name':badge.name,
                    'link':badge.link,
                    'imageURL':badge.imageURL
                }
                badgesList.append(badgeDict)
            
            data = {'badges':badgesList}
            
            
        else:
            data = {'error':'Sorry, that user does not exist.'}
            
            
        
    else:
        data = {
            'error': "There was an error posting this request. Please try again.",
        }
            
    return HttpResponse(json.dumps(data))
            










