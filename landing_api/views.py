import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

COLLECTION = "favoritos"


def _collection_url():
    return f"{settings.FIREBASE_DATABASE_URL}/{COLLECTION}.json"


def _item_url(item_id):
    return f"{settings.FIREBASE_DATABASE_URL}/{COLLECTION}/{item_id}.json"


class LandingAPI(APIView):
    def get(self, request):
        response = requests.get(_collection_url())
        if response.status_code != 200:
            return Response(
                {"error": "No se pudo leer la base de datos"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        data = response.json() or {}
        if isinstance(data, dict):
            items = [{"id": key, **value} for key, value in data.items()]
        else:
            items = []
        return Response(items, status=status.HTTP_200_OK)

    def post(self, request):
        payload = request.data
        if "nombre" not in payload or "favorito" not in payload:
            return Response(
                {"error": "Los campos 'nombre' y 'favorito' son obligatorios"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = requests.post(_collection_url(), json=payload)
        if response.status_code != 200:
            return Response(
                {"error": "No se pudo guardar el registro"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        new_id = response.json().get("name")
        return Response({"id": new_id, **payload}, status=status.HTTP_201_CREATED)


class LandingDetailAPI(APIView):
    def _find(self, item_id):
        return requests.get(_item_url(item_id)).json()

    def get(self, request, item_id):
        data = self._find(item_id)
        if data is None:
            return Response(
                {"error": f"No existe el registro {item_id}"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response({"id": item_id, **data}, status=status.HTTP_200_OK)

    def put(self, request, item_id):
        if self._find(item_id) is None:
            return Response(
                {"error": f"No existe el registro {item_id}"},
                status=status.HTTP_404_NOT_FOUND,
            )
        requests.put(_item_url(item_id), json=request.data)
        return Response({"id": item_id, **request.data}, status=status.HTTP_200_OK)

    def patch(self, request, item_id):
        current = self._find(item_id)
        if current is None:
            return Response(
                {"error": f"No existe el registro {item_id}"},
                status=status.HTTP_404_NOT_FOUND,
            )
        requests.patch(_item_url(item_id), json=request.data)
        return Response({"id": item_id, **current, **request.data}, status=status.HTTP_200_OK)

    def delete(self, request, item_id):
        if self._find(item_id) is None:
            return Response(
                {"error": f"No existe el registro {item_id}"},
                status=status.HTTP_404_NOT_FOUND,
            )
        requests.delete(_item_url(item_id))
        return Response(status=status.HTTP_204_NO_CONTENT)
