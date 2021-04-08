from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import story, authors
from django.views import View
import json


# Create your views here.

@csrf_exempt
def login(request):
  response = HttpResponse()
  response.content = "username or password incorrect"
  response.status_code = 403
  data = ""
  if request.method == 'POST':
    data = request.POST
  user = authors.objects.filter(username=data['username'], password=data['password'])
  if user.exists():
    response.content = "log in successfully,Welcome! " + user[0].name
    response.status_code = 200
    request.session['id'] = user[0].id
    request.session['username'] = data['username']
    request.session['is_login'] = True
  return response


@csrf_exempt
def logout(request):
  response = HttpResponse()
  response.content = "logout successfully"
  response.status_code = 200
  del request.session['id']
  del request.session['username']
  del request.session['is_login']
  return response


@csrf_exempt
def poststory(request):
  print(request.session.get("username"))
  response = HttpResponse()
  if request.session['is_login']:

    data = ""
    if request.method == "POST":
      data = eval(request.body)
    headline = data['headline']
    category = data['category']
    region = data['region']
    details = data['details']
    author = authors.objects.get(id=request.session.get('id'))
    new_story = story(headline=headline, category=category, region=region, details=details, author=author)
    new_story.save()
    response.content = "post successfully"
    response.status_code = 201
  else:
    response.status_code = 403
    response.content = "permission denied"

  return response


@csrf_exempt
def getstories(request):
  stories = story.objects.all()
  storyList = []
  category = None
  region = None
  date = None
  response = HttpResponse()
  response.content = None
  response.status_code = 404
  if request.method == "GET":
    data = eval(request.body)
    category = data['story_cat']
    region = data['story_region']
    date = data['story_date']
  for singleStory in stories:
    if (singleStory.category == category or category == "*") and (singleStory.region == region or region == "*") and (
      date_match(singleStory.date,date) or date == "*"):
      storyInfo = {
        "key": singleStory.id,
        "headline": singleStory.headline,
        "story_cat": singleStory.category,
        "story_region": singleStory.region,
        "author": singleStory.author.name,
        "story_date": str(singleStory.date.year) + '/' + str(singleStory.date.month) + '/' + str(singleStory.date.day),
        "story_details": singleStory.details,
      }
      storyList.append(storyInfo)
      response.status_code = 200
  response.content = '{"stories":' + json.dumps(storyList) + "}"
  if response.status_code == 404:
    response.content = "no story found"
  return response


@csrf_exempt
def deletestory(request):
  response = HttpResponse()
  if request.session['is_login']:
    if request.method == "POST":
      data = eval(request.body)
      key = data['story_key']
      targetStory = story.objects.filter(id=key)
      if targetStory.exists():
        targetStory.delete()
        response.status_code = 201
        response.content = "delete successfully"
      else:
        response.status_code = 503
        response.content = "story not found "
    else:
      response.status_code = 404
      response.content = "delete operation only allows POST method"
  else:
    response.status_code = 403
    response.content = "permission denied"
  return response


def date_match(date_database, date_post):
  if date_post!="*":
    year_database = date_database.year
    month_database = date_database.month
    day_database = date_database.day
    date_post_split = date_post.split("/", 2)
    year_post = int(date_post_split[2])
    month_post = int(date_post_split[1])
    day_post = int(date_post_split[0])
    if year_database == year_post and month_database == month_post and day_database == day_post:
      return True
  return False
