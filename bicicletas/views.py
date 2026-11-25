from django.contrib import messages
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import BicicletaCrearForm, BicicletaEditarForm
from .models import Bicicleta


@require_http_methods(["GET"])
def inicio(request):
    bicicletas = Bicicleta.objects.all()
    contexto = {
        "total_referencias": bicicletas.count(),
        # Si no hay bicicletas, Sum devuelve None en lugar de cero.
        "total_stock": bicicletas.aggregate(total=Sum("stock"))["total"] or 0,
        "sin_stock": bicicletas.filter(stock=0).count(),
        "recientes": bicicletas.order_by("-fecha_registro", "-pk")[:5],
    }
    return render(request, "inicio.html", contexto)


@require_http_methods(["GET"])
def listar(request):
    bicicletas = Bicicleta.objects.all()
    buscar = request.GET.get("q", "").strip()
    tipo = request.GET.get("tipo", "")
    if buscar:
        bicicletas = bicicletas.filter(Q(marca__icontains=buscar) | Q(modelo__icontains=buscar))
    if tipo in dict(Bicicleta.TIPOS):
        bicicletas = bicicletas.filter(tipo=tipo)
    else:
        tipo = ""
    return render(request, "listar.html", {
        "bicicletas": bicicletas, "buscar": buscar, "tipo": tipo, "tipos": Bicicleta.TIPOS,
    })


@require_http_methods(["GET", "POST"])
def crear(request):
    if request.method == "POST":
        form = BicicletaCrearForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Bicicleta registrada correctamente.")
            return redirect("bicicletas:listar")
    else:
        form = BicicletaCrearForm()
    return render(request, "crear.html", {"form": form})


@require_http_methods(["GET", "POST"])
def editar(request, pk):
    bicicleta = get_object_or_404(Bicicleta, pk=pk)
    if request.method == "POST":
        # instance permite actualizar la bicicleta existente en vez de crear otra.
        form = BicicletaEditarForm(request.POST, instance=bicicleta)
        if form.is_valid():
            form.save()
            messages.success(request, "Bicicleta actualizada correctamente.")
            return redirect("bicicletas:listar")
    else:
        form = BicicletaEditarForm(instance=bicicleta)
    return render(request, "editar.html", {"form": form, "bicicleta": bicicleta})


@require_http_methods(["GET", "POST"])
def eliminar(request, pk):
    bicicleta = get_object_or_404(Bicicleta, pk=pk)
    # GET muestra la confirmación; solo POST elimina el registro.
    if request.method == "POST":
        bicicleta.delete()
        messages.success(request, "Bicicleta eliminada correctamente.")
        return redirect("bicicletas:listar")
    return render(request, "eliminar.html", {"bicicleta": bicicleta})
