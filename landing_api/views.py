from datetime import datetime

from firebase_admin import db
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "favoritos"

    @staticmethod
    def _firebase_error_response():
        return Response(
            {"error": "La conexión con Firebase no está configurada."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    def get(self, request):
        try:
            ref = db.reference(f"{self.collection_name}")
            data = ref.get()
            return Response(data, status=status.HTTP_200_OK)
        except Exception:
            return self._firebase_error_response()

    def post(self, request):
        data = request.data.copy()

        if not data:
            return Response(
                {"error": "El cuerpo de la solicitud no puede estar vacío."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            ref = db.reference(f"{self.collection_name}")
            current_time = datetime.now()
            custom_format = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower() \
                .replace('am', 'a. m.').replace('pm', 'p. m.')
            data.update({"timestamp": custom_format})
            new_resource = ref.push(data)
            return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)
        except Exception:
            return self._firebase_error_response()


class LandingDetailAPI(APIView):
    """CRUD por elemento sobre la misma colección."""

    name = "Landing API - Item"
    collection_name = "favoritos"

    @staticmethod
    def _firebase_error_response():
        return Response(
            {"error": "La conexión con Firebase no está configurada."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    def _reference(self, item_id):
        return db.reference(f"{self.collection_name}/{item_id}")

    def get(self, request, item_id):
        try:
            data = self._reference(item_id).get()
            if data is None:
                return Response(
                    {"error": f"No existe el registro {item_id}."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            return Response({"id": item_id, **data}, status=status.HTTP_200_OK)
        except Exception:
            return self._firebase_error_response()

    def put(self, request, item_id):
        try:
            ref = self._reference(item_id)
            if ref.get() is None:
                return Response(
                    {"error": f"No existe el registro {item_id}."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            data = request.data.copy()
            ref.set(data)
            return Response({"id": item_id, **data}, status=status.HTTP_200_OK)
        except Exception:
            return self._firebase_error_response()

    def patch(self, request, item_id):
        try:
            ref = self._reference(item_id)
            current = ref.get()
            if current is None:
                return Response(
                    {"error": f"No existe el registro {item_id}."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            ref.update(dict(request.data))
            return Response({"id": item_id, **ref.get()}, status=status.HTTP_200_OK)
        except Exception:
            return self._firebase_error_response()

    def delete(self, request, item_id):
        try:
            ref = self._reference(item_id)
            if ref.get() is None:
                return Response(
                    {"error": f"No existe el registro {item_id}."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            ref.delete()
            return Response(
                {"message": f"Registro {item_id} eliminado."},
                status=status.HTTP_200_OK,
            )
        except Exception:
            return self._firebase_error_response()