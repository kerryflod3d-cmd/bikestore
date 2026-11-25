from django import forms
from .models import Bicicleta


class BicicletaCrearForm(forms.ModelForm):
    """Formulario para registrar una bicicleta nueva."""

    class Meta:
        model = Bicicleta
        fields = ["marca", "modelo", "tipo", "aro", "color", "precio", "stock", "descripcion"]
        labels = {"precio": "Precio (CLP)", "aro": "Aro (pulgadas)", "descripcion": "Descripción"}
        widgets = {
            "precio": forms.NumberInput(attrs={"min": 1, "step": 1}),
            "stock": forms.NumberInput(attrs={"min": 0, "step": 1}),
            "descripcion": forms.Textarea(attrs={"rows": 3}),
        }
        help_texts = {"precio": "Ingresa el precio en pesos chilenos, sin decimales.",
                      "stock": "Cantidad de unidades disponibles."}


class BicicletaEditarForm(BicicletaCrearForm):
    """Formulario de edición: mismos campos y reglas, con ayuda contextual."""

    class Meta(BicicletaCrearForm.Meta):
        help_texts = {"precio": "Actualiza el precio de venta en pesos chilenos.",
                      "stock": "Indica la cantidad actual de unidades disponibles."}
