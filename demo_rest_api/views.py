from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid

data_list = []
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False})


class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):
        return Response(data_list, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        if 'name' not in data or 'email' not in data:
            return Response(
                {'error': 'Los campos "name" y "email" son obligatorios.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        new_item = {
            'id': str(uuid.uuid4()),
            'name': data['name'],
            'email': data['email'],
            'is_active': True,
        }
        data_list.append(new_item)
        return Response(
            {'message': 'Elemento creado exitosamente.', 'data': new_item},
            status=status.HTTP_201_CREATED
        )


class DemoRestApiItem(APIView):
    name = "Demo REST API - Item"

    def _find_item(self, item_id):
        for index, item in enumerate(data_list):
            if item['id'] == item_id:
                return index, item
        return None, None

    def put(self, request, item_id):
        data = request.data
        index, item = self._find_item(item_id)
        if index is None:
            return Response({'error': f'No se encontró el elemento con id "{item_id}".'}, status=status.HTTP_404_NOT_FOUND)
        if 'name' not in data or 'email' not in data:
            return Response({'error': 'PUT requiere los campos "name" y "email".'}, status=status.HTTP_400_BAD_REQUEST)
        updated_item = {'id': item_id, 'name': data['name'], 'email': data['email'], 'is_active': data.get('is_active', True)}
        data_list[index] = updated_item
        return Response({'message': 'Elemento reemplazado completamente.', 'data': updated_item}, status=status.HTTP_200_OK)

    def patch(self, request, item_id):
        data = request.data
        index, item = self._find_item(item_id)
        if index is None:
            return Response({'error': f'No se encontró el elemento con id "{item_id}".'}, status=status.HTTP_404_NOT_FOUND)
        updated_item = {**item}
        for field in ['name', 'email', 'is_active']:
            if field in data:
                updated_item[field] = data[field]
        data_list[index] = updated_item
        return Response({'message': 'Elemento actualizado parcialmente.', 'data': updated_item}, status=status.HTTP_200_OK)

    def delete(self, request, item_id):
        index, item = self._find_item(item_id)
        if index is None:
            return Response({'error': f'No se encontró el elemento con id "{item_id}".'}, status=status.HTTP_404_NOT_FOUND)
        if not item['is_active']:
            return Response({'error': f'El elemento "{item_id}" ya está inactivo.'}, status=status.HTTP_400_BAD_REQUEST)
        data_list[index]['is_active'] = False
        return Response({'message': f'Elemento "{item_id}" desactivado.', 'data': data_list[index]}, status=status.HTTP_200_OK)