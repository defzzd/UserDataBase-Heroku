from django.shortcuts import render

from django.http import HttpResponseRedirect

# Create your views here.

from udb.models import UserObject
from udb.forms import CreateUserForm, EditUserForm
from django.core.urlresolvers import reverse



## NOTE: I've chosen to leave a lot of commented code in here to reflect my learning process.
## I spent a lot of time reading through tutorials since I'd never used Django before.
## The critical piece of information that was holding me back for days was that HTML receives data from the views.foofunction() that the urls.py url() call invokes from the regex-parsed url.
## In other words:
## 1. a URL hits the server
## 2. a url()'s regex in urls.py serves up a views.foo_function 
## 3. views.foo_function() does Python on the HTTP request and whatever it was called with ((which is nothing for the first index view triggered by my index's url() call))
## ---- database access happens ONLY during step 3
## 4. views.foo_function serves up some form of next-page call, as a render(), HttpResponse(), HttpResponseRedirect()...
## 5. the HTML I functionally associate with the views.foofunction() is displayed AFTER views.foofunction() is FULLY executed.
## 6. the HTML contains the thing that causes the user to send another URL to the server, moving them to the next page. NOT THE VIEWS FUNCTION
## ---- My not understanding these last two parts in particular made it very confusing to understand how anything I wrote in here interacted with HTML. For days.



def userobject_index(request):

    UserObject_list = UserObject.objects.all().order_by('first_name')
    context = {'userobject_list': UserObject_list}
    return render(request, 'userobject_index.html', context)
    
 

def edit_userobject(request, userobject_id):

    userobject_id = userobject_id
    
    editable_userobject = UserObject.objects.get(pk=userobject_id)
    
    invalidation_string = ''
    
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
    
        # create a form instance and populate it with data from the request:
        form = EditUserForm(request.POST)
        
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            #print(str(form.cleaned_data))
            
            if form.cleaned_data['first_name'] != '':
                editable_userobject.first_name = form.cleaned_data['first_name']
                
                #first_name = editable_userobject.get(pk=request.POST['first_name'])
            
            if form.cleaned_data['last_name'] != '':
                editable_userobject.last_name = form.cleaned_data['last_name']
                
                #last_name = editable_userobject.get(pk=request.POST['last_name'])
                
            if form.cleaned_data['email_address'] != '':
                editable_userobject.email_address = form.cleaned_data['email_address']
            
                #email_address = editable_userobject.get(pk=request.POST['email_address'])

            
            #new_userobject = UserObject.objects.create(first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'], email_address=form.cleaned_data['email_address'])
            
            editable_userobject.save()
            
            # redirect to a new URL:
            
            #return HttpResponseRedirect(reverse('udb:edit_userobject', args=(editable_userobject.id,)))
            
            ## All reverse() does is let me use a string to call up an html page, or something, instead of using a more machiney variable somewhere. It's in the docs.
            return HttpResponseRedirect(reverse('udb:userobject_index'))
            #return HttpResponseRedirect('/udb/userobject_index.html')
        

        else:
            invalidation_string = 'Invalid entry! Email address must be of the form xxx@xxx.xxx'
            
    # if a GET (or any other method) we'll create a blank form
    else:
        form = EditUserForm()
        
    #return render(request, 'edit_userobject.html', {'form': form})
    
    ## seeing if I can add extra info to the edit_userobject page through this dictionary...
    ## Whoa it works!!
    ## ... it also saved me from the hours-long pit of insufficiently explicit tutorials
    ## that were keeping me from realizing everything the html page associated with this view renders with...
    ## has to come from the dictionary supplied to THIS render() call, only and completely.
    ## Specifically the userobject_id was what was holding me up for hours and hours of googling and reading.
    ## As soon as I realize the html was getting all its foreign variables from here, everything became easy.
    ## Even the JavaScript+HTML tutorial, which I saved for last and had a similar misconception about.
    ## ((I'd done HTML and JS tutorials separately but never got far enough into frontend dev to integrate the two))
    return render(request, 'edit_userobject.html',
        {
        'form': form,
        'invalidation_string': invalidation_string,
        'userobject_id': userobject_id,
        'supplied_first_name': editable_userobject.first_name,
        'supplied_last_name': editable_userobject.last_name,
        'supplied_email_address': editable_userobject.email_address
        })



def delete_userobject(request, userobject_id):


    UserObject.objects.get(pk=userobject_id).delete()
    
    return HttpResponseRedirect(reverse('udb:userobject_index')) 
    

    
    
def create_userobject(request):

    # if this is a POST request we need to process the form data
 
    invalidation_string = ''   
    
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreateUserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            print(str(form.cleaned_data))
            new_userobject = UserObject.objects.create(first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'], email_address=form.cleaned_data['email_address'])
            
            new_userobject.save()
            
            # redirect to a new URL:
            return HttpResponseRedirect('/udb/userobject_index.html')

        else:
            invalidation_string = 'Invalid entry! Email address must be of the form xxx@xxx.xxx'    
            
            
    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreateUserForm()

    return render(request, 'create_userobject.html', {
        'form': form,
        'invalidation_string': invalidation_string,
        })