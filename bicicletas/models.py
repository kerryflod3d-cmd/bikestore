
from django.db import models
from django.core.validators import MinValueValidator


class Bicicleta(models.Model):

    TIPOS = [
        ("mtb", "Mountain Bike"),
        ("urbana", "Urbana"),
        ("ruta", "Ruta"),
        ("bmx", "BMX"),
        ("electrica", "Eléctrica"),
        ("infantil", "Infantil"),
    ]

    AROS = [
        ("12", "12 pulgadas"),
        ("14", "14 pulgadas"),
        ("16", "16 pulgadas"),
        ("18", "18 pulgadas"),
        ("20", "20 pulgadas"),
        ("24", "24 pulgadas"),
        ("26", "26 pulgadas"),
        ("27.5", "27.5 pulgadas"),
        ("28", "28 pulgadas"),
        ("29", "29 pulgadas"),
    ]

    marca = models.CharField(max_length=60)
    modelo = models.CharField(max_length=100)

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS
    )

    # El aro se guarda como texto para admitir medidas como 27.5.
    aro = models.CharField(
        max_length=4,
        choices=AROS
    )

    color = models.CharField(max_length=50)

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        validators=[MinValueValidator(1)]
    )

    stock = models.PositiveIntegerField(default=0)

    descripcion = models.TextField(blank=True)

    fecha_registro = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["marca", "modelo"]
        verbose_name = "Bicicleta"
        verbose_name_plural = "Bicicletas"

        # MariaDB también debe rechazar precios menores o iguales a cero.
        constraints = [
            models.CheckConstraint(
                condition=models.Q(precio__gt=0),
                name="bicicleta_precio_positivo"
            )
        ]

    def __str__(self):
        return f"{self.marca} {self.modelo}"
