from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse as res
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.


def home_view(req):
    return render(req, "home.html")

# vista/funcion para la registar al usuario


def register_view(req):
    # saber cual es metodo de la peticion y saber si debe de retornar la vista
    # o registrar al usuario

    if req.method == "GET":
        return render(req, "register.html", {
            "form": UserCreationForm()
        })
    else:
        # si las contraseñas ingresadas son iguales
        # intentar registrar al usuario
        print(req, req.POST)
        
        if req.POST["password1"] == req.POST["password2"]:
            try:
                # crear al usuario
                # guardarlo en la DB
                # iniciar sesion
                # redireccionar a la vista de las teras

                user = User.objects.create_user(username=req.POST["username"],
                                                password=req.POST["password1"])

                user.save()

                login(req, user)

                return redirect("tasks")
            except IntegrityError:
                # manejar la excepcion "IntegrityError"
                # para saber si el usuario ya existe

                return render(req, "register.html", {
                    "form": UserCreationForm(),
                    "error": f"EL usuario ya existe"
                })
            except Exception as e:
                # mostrar en la vista si hubo un error al crear el usuario

                return render(req, "register.html", {
                    "form": UserCreationForm(),
                    "error": f"Error al crear usuario: {e}"
                })
        else:
            return render(req, "register.html", {
                "form": UserCreationForm(),
                "error": "Las contraseñas no coinciden"
            })


def login_view(req):
    if req.method == "GET":
        return render(req, "login.html", {
            "form": AuthenticationForm()
        })
    else:
        try:
            user = authenticate(
                req, username=req.POST["username"], password=req.POST["password"])

            if user is None:
                return render(req, "login.html", {
                    "form": AuthenticationForm,
                    "error": "Credenciales invalidas"
                })
            else:
                login(req, user)
                return redirect("tasks")
        except Exception as e:
            return render(req, "login.html", {
                "form": AuthenticationForm,
                "error": "Error al iniciar sesion"
            })


@login_required
def logout_view(req):
    logout(req)
    return redirect("home")


@login_required
def tasks_view(req):
    try:
        # asi se llaman todas las tareas en la DB
        # tasks = Task.objects.all()
        # solo tomar las tareas de el usurio sin completar
        tasks = Task.objects.filter(user=req.user, datecomplete__isnull=True)

        return render(req, "tasks.html", {
            "tasks": tasks
        })
    except AttributeError:
        return render(req, "tasks.html", {
            "error": "No se ha iniciado sesion"
        })


@login_required
def create_task_view(req):
    if req.method == "GET":
        return render(req, "create_task.html", {
            "form": TaskForm()
        })
    else:
        try:
            # crear un nuevo obj/tarea
            # -
            form = TaskForm(req.POST)

            new_task = form.save(commit=False)
            new_task.user = req.user

            new_task.save()

            print(new_task)

            return redirect("tasks")
        except ValueError:
            return render(req, "create_task.html", {
                "form": TaskForm(),
                "error": "Introduzca valores validos"
            })


@login_required
def task_detail_view(req, task_id):
    if req.method == "GET":
        try:
            # forma para obtener la tarea mediante el id
            # task = Task.objects.get(id=task_id, user=req.user)

            # forma para obtener la tarea mediante el id mas eficiente
            task = get_object_or_404(Task, pk=task_id, user=req.user)
            form = TaskForm(instance=task)

            return render(req, "task_detail.html", {
                "task": task,
                "form": form
            })
        except Exception as e:
            return render(req, "task_detail.html", {
                "error": "No se encontro la tarea"
            })
    else:
        # codigo para actulizar la informacion de la tarea
        # - obtener el obj/tarea
        # - crear un nueva instancia con los datos enviados de el front y obj task como argumgento
        # - guardar la tarea /  actualizar la informacion de esta

        try:
            task = get_object_or_404(Task, pk=task_id, user=req.user)
            print(task)
            form = TaskForm(req.POST, instance=task)
            form.save()
            return redirect("tasks")
        except ValueError:
            return render(req, "task_detail.html", {
                "error": "Error al actualizar la tarea"
            })


@login_required
def complete_task(req, task_id):
    task = get_object_or_404(Task, pk=task_id, user=req.user)

    if req.method == "POST":
        try:
            task.datecomplete = timezone.now()
            task.save()

            return redirect("tasks_completed")
        except Exception as e:
            print(f"Error al completar tarea: {e}")


@login_required
def delete_task(req, task_id):

    task = get_object_or_404(Task, pk=task_id, user=req.user)

    if req.method == "POST":
        try:
            task.delete()

            return redirect("tasks")
        except Exception as e:
            print(f"Error al eliminar la tarea: {e}")


@login_required
def completed_tasks_view(req):
    try:
        tasks = Task.objects.filter(user=req.user, datecomplete__isnull=False)

        return render(req, "tasks.html", {
            "tasks": tasks
        })
    except Exception as e:
        print(f"Error: {e}")
