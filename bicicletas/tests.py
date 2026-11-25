from django.db import DatabaseError, transaction
from django.test import Client, TestCase
from django.urls import reverse

from .models import Bicicleta


class InventarioTests(TestCase):
    def setUp(self):
        self.datos = {
            "marca": "Trek", "modelo": "Marlin 5", "tipo": "mtb", "aro": "29",
            "color": "Negro", "precio": "399990", "stock": "3", "descripcion": "",
        }
        self.bicicleta = Bicicleta.objects.create(**self.datos)

    def url(self, nombre, pk=None):
        return reverse(f"bicicletas:{nombre}", args=[pk] if pk is not None else [])

    def test_inicio(self):
        respuesta = self.client.get(self.url("inicio"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.context["total_referencias"], 1)
        self.assertEqual(respuesta.context["total_stock"], 3)
        self.assertEqual(respuesta.context["sin_stock"], 0)

    def test_listar(self):
        respuesta = self.client.get(self.url("listar"))
        self.assertContains(respuesta, "Marlin 5")

    def test_busqueda_y_filtro(self):
        Bicicleta.objects.create(**{**self.datos, "marca": "Oxford", "modelo": "Orion", "tipo": "urbana"})
        respuesta = self.client.get(self.url("listar"), {"q": "marlin", "tipo": "mtb"})
        self.assertContains(respuesta, "Marlin 5")
        self.assertNotContains(respuesta, "Orion")

    def test_formulario_crear(self):
        respuesta = self.client.get(self.url("crear"))
        self.assertTemplateUsed(respuesta, "crear.html")
        self.assertContains(respuesta, "Registrar bicicleta")

    def test_crear_persiste_en_bd(self):
        respuesta = self.client.post(self.url("crear"), {**self.datos, "modelo": "Marlin 6"})
        self.assertRedirects(respuesta, self.url("listar"))
        self.assertTrue(Bicicleta.objects.filter(modelo="Marlin 6").exists())
        self.assertEqual(Bicicleta.objects.count(), 2)

    def test_rechazar_datos_invalidos(self):
        casos = [("marca", ""), ("modelo", "   "), ("precio", "0"), ("precio", "-1"),
                 ("precio", "abc"), ("precio", "1.5"), ("stock", "-1"),
                 ("stock", "1.5"), ("stock", ""), ("tipo", "invalido"), ("aro", "100")]
        for campo, valor in casos:
            with self.subTest(campo=campo, valor=valor):
                respuesta = self.client.post(self.url("crear"), {**self.datos, campo: valor})
                self.assertEqual(respuesta.status_code, 200)
                self.assertIn(campo, respuesta.context["form"].errors)
                self.assertEqual(Bicicleta.objects.count(), 1)

    def test_stock_cero_es_valido(self):
        respuesta = self.client.post(self.url("crear"), {**self.datos, "modelo": "Sin stock", "stock": "0"})
        self.assertRedirects(respuesta, self.url("listar"))
        self.assertTrue(Bicicleta.objects.filter(modelo="Sin stock", stock=0).exists())

    def test_formulario_editar_precargado(self):
        respuesta = self.client.get(self.url("editar", self.bicicleta.pk))
        self.assertTemplateUsed(respuesta, "editar.html")
        self.assertEqual(respuesta.context["form"].initial["modelo"], "Marlin 5")

    def test_editar_no_duplica_registro(self):
        respuesta = self.client.post(self.url("editar", self.bicicleta.pk), {**self.datos, "precio": "419990", "stock": "6"})
        self.assertRedirects(respuesta, self.url("listar"))
        self.bicicleta.refresh_from_db()
        self.assertEqual(self.bicicleta.precio, 419990)
        self.assertEqual(self.bicicleta.stock, 6)
        self.assertEqual(Bicicleta.objects.count(), 1)

    def test_editar_invalido_no_modifica_bd(self):
        respuesta = self.client.post(self.url("editar", self.bicicleta.pk), {**self.datos, "precio": "0"})
        self.assertIn("precio", respuesta.context["form"].errors)
        self.bicicleta.refresh_from_db()
        self.assertEqual(self.bicicleta.precio, 399990)

    def test_get_eliminar_solo_confirma(self):
        respuesta = self.client.get(self.url("eliminar", self.bicicleta.pk))
        self.assertTemplateUsed(respuesta, "eliminar.html")
        self.assertTrue(Bicicleta.objects.filter(pk=self.bicicleta.pk).exists())

    def test_post_eliminar_borra_registro(self):
        respuesta = self.client.post(self.url("eliminar", self.bicicleta.pk))
        self.assertRedirects(respuesta, self.url("listar"))
        self.assertFalse(Bicicleta.objects.filter(pk=self.bicicleta.pk).exists())

    def test_id_inexistente_devuelve_404(self):
        for nombre in ("editar", "eliminar"):
            self.assertEqual(self.client.get(self.url(nombre, 999999)).status_code, 404)

    def test_post_sin_csrf_es_rechazado(self):
        cliente = Client(enforce_csrf_checks=True)
        respuesta = cliente.post(self.url("eliminar", self.bicicleta.pk))
        self.assertEqual(respuesta.status_code, 403)
        self.assertTrue(Bicicleta.objects.filter(pk=self.bicicleta.pk).exists())

    def test_busqueda_independiente(self):
        Bicicleta.objects.create(**{**self.datos, "marca": "Oxford", "modelo": "Orion"})
        for consulta in ("trek", "marlin"):
            with self.subTest(consulta=consulta):
                respuesta = self.client.get(self.url("listar"), {"q": consulta})
                self.assertContains(respuesta, "Marlin 5")
                self.assertNotContains(respuesta, "Orion")

    def test_filtro_independiente(self):
        Bicicleta.objects.create(**{**self.datos, "marca": "Oxford", "modelo": "Orion", "tipo": "urbana"})
        respuesta = self.client.get(self.url("listar"), {"tipo": "urbana"})
        self.assertContains(respuesta, "Orion")
        self.assertNotContains(respuesta, "Marlin 5")

    def test_metodos_http_no_permitidos(self):
        self.assertEqual(self.client.post(self.url("inicio")).status_code, 405)
        self.assertEqual(self.client.post(self.url("listar")).status_code, 405)
        self.assertEqual(self.client.put(self.url("crear")).status_code, 405)
        self.assertEqual(self.client.put(self.url("editar", self.bicicleta.pk)).status_code, 405)
        self.assertEqual(self.client.delete(self.url("eliminar", self.bicicleta.pk)).status_code, 405)
        self.assertEqual(Bicicleta.objects.count(), 1)

    def test_bd_rechaza_precio_cero(self):
        # update() evita el formulario: comprobamos la restricción de la BD.
        with self.assertRaises(DatabaseError), transaction.atomic():
            Bicicleta.objects.filter(pk=self.bicicleta.pk).update(precio=0)
        self.bicicleta.refresh_from_db()
        self.assertEqual(self.bicicleta.precio, 399990)

    def test_bd_rechaza_stock_negativo(self):
        # MariaDB en modo estricto rechaza valores fuera del rango UNSIGNED.
        with self.assertRaises(DatabaseError), transaction.atomic():
            Bicicleta.objects.filter(pk=self.bicicleta.pk).update(stock=-1)
        self.bicicleta.refresh_from_db()
        self.assertEqual(self.bicicleta.stock, 3)
