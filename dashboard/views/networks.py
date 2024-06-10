from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from dashboard.helpers import (list_network,
                               inspect_network,
                               delete_network)


def networks_list(request):
    resp = list_network()
    if not resp:
        return render(request, 'dashboard/networks.html', {})

    networks = []
    try:
        for r in resp:
        
            _resp = inspect_network(r['Id'])
            if not _resp:
                return render(request, 'dashboard/networks.html', {})
            
            network = {
                'id': r['Id'][:12],
                'name': r['Name'],
                'ipv4net': r['IPAM']['Config'][0]['Subnet'],
                'containers': len(_resp['Containers']),
            }
            networks.append(network)
        return render(request, 'dashboard/networks.html', {'networks': networks})  
    except (KeyError, TypeError):
        return render(request, 'dashboard/networks.html', {})

class DeleteNetwork(APIView):

    def post(self, request):
        try:
            network = request.data['name']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        resp = delete_network(network)

        if resp:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
