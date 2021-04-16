from django.shortcuts import render, HttpResponse, redirect
from MyToDo.models import ToDo
from MyToDo.forms import ToDoForm

# Create your views here.
def home(request):
    name = 'home.html'
    todo_list = ToDo.objects.all()  #request query set
    form = ToDoForm()

    context = {'app_name': "ToDo App", 'todo_list': todo_list, 'form': form}
    return render(request, name, context=context)


def add_todo(request):
    if request.method == 'POST':
        # save the todo
        form = ToDoForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            ToDo.objects.create(text=text)
    
    return redirect('home')


def delete_todo(request, todo_id):
    if request.method == 'POST':
        todo_obj = ToDo.objects.get(pk=todo_id)
        todo_obj.delete()

    return redirect('home')


def edit_todo(request, todo_id):
    todo_obj = ToDo.objects.get(pk=todo_id)

    if request.method == 'POST':
        form = ToDoForm(request.POST, initial={'text': todo_obj.text})
        if form.is_valid():
            todo_obj.todo_text = form.cleaned_data.get('text')
            todo_obj.save()
            return redirect('home')

    name = 'edit.html'
    form = ToDoForm(initial={'text': todo_obj.text})
    context = {'app_name': "ToDo App", 'form': form, 'todo_obj': todo_obj}
    return render(request, name, context)