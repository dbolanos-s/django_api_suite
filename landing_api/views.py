from datetime import datetime

from firebase_admin import db
from firebase_admin.exceptions import NotFoundError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class LandingAPI(APIView):
    """API para gestionar datos de Landing en Firebase Realtime Database."""

    collection_name = "landing"

    def _get_collection(self):
        try:
            ref = db.reference(self.collection_name)
            data = ref.get()
        except NotFoundError:
            return []

        if data is None:
            return []
        if isinstance(data, list):
            return data
        return [data]

    def get(self, request):
        try:
            data = self._get_collection()
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        try:
            payload = request.data
            if "titulo" not in payload:
                return Response(
                    {"error": "El campo 'titulo' es obligatorio"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            ref = db.reference(self.collection_name)
            existing_data = ref.get()

            if existing_data is None:
                existing_data = []
            elif not isinstance(existing_data, list):
                existing_data = [existing_data]

            ids = [item.get("id", 0) for item in existing_data if isinstance(item, dict)]
            new_id = max(ids) + 1 if ids else 1

            new_item = {
                "id": new_id,
                "titulo": payload.get("titulo"),
                "descripcion": payload.get("descripcion", ""),
                "url": payload.get("url", ""),
                "creado_en": datetime.now().isoformat(),
                "actualizado_en": datetime.now().isoformat(),
            }

            existing_data.append(new_item)
            ref.set(existing_data)
            return Response(new_item, status=status.HTTP_201_CREATED)

        except NotFoundError:
            ref = db.reference(self.collection_name)
            ref.set([])
            return self.post(request)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LandingDetailAPI(APIView):
    """API para operaciones en un elemento específico de landing."""

    collection_name = "landing"

    def _load_data(self):
        try:
            ref = db.reference(self.collection_name)
            data = ref.get()
        except NotFoundError:
            return []

        if data is None:
            return []
        return data if isinstance(data, list) else [data]

    def get(self, request, landing_id):
        try:
            data = self._load_data()
            for item in data:
                if isinstance(item, dict) and item.get("id") == landing_id:
                    return Response(item, status=status.HTTP_200_OK)

            return Response(
                {"error": f"Landing con ID {landing_id} no encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, landing_id):
        try:
            data = self._load_data()
            for item in data:
                if isinstance(item, dict) and item.get("id") == landing_id:
                    item["titulo"] = request.data.get("titulo", item.get("titulo"))
                    item["descripcion"] = request.data.get("descripcion", item.get("descripcion"))
                    item["url"] = request.data.get("url", item.get("url"))
                    item["actualizado_en"] = datetime.now().isoformat()
                    db.reference(self.collection_name).set(data)
                    return Response(item, status=status.HTTP_200_OK)

            return Response(
                {"error": f"Landing con ID {landing_id} no encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, landing_id):
        try:
            data = self._load_data()
            for index, item in enumerate(data):
                if isinstance(item, dict) and item.get("id") == landing_id:
                    data.pop(index)
                    ref = db.reference(self.collection_name)
                    if data:
                        ref.set(data)
                    else:
                        ref.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)

            return Response(
                {"error": f"Landing con ID {landing_id} no encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
