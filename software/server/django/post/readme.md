# what

this demos a post request that runs an arbitrary python function. 

The index ("root") page has 2 buttons, that each send a post request to another
page `post`. One form has one hidden field _plug_. The other has no fields. On
pressing a button:

1. The form's value is submitted to the page `post/`.
2. A function "post" recieves the request data.
3. If the request contains a field named plug, the function echoes its value to
   stdout and DOES NOT load another page. If not, it redirects to a page and
   complains.

This is intended to be used to toggle a plug's ON/OFF.

# list of what was done to produce this dir

1. pacman -S python-django
2. django-admin startproject post
2. editing `post\urls.py`

# refs

<https://docs.djangoproject.com/en/4.0/intro/tutorial01/>
<https://docs.djangoproject.com/en/4.0/intro/tutorial04/>
<https://docs.djangoproject.com/en/4.0/topics/templates/>
<https://www.w3schools.com/tags/att_input_type_hidden.asp>
<https://docs.djangoproject.com/en/4.0/topics/http/views/#customizing-error-views-1>
<https://docs.djangoproject.com/en/4.0/ref/request-response/>
<https://drive.google.com/drive/folders/1y4xEgg5B9JR7TIvxBum3i_vt6Q69BfnN>
