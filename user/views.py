from django.shortcuts import render

# Create your views here.
class UserRegisterView(ModelViewSet):
	parser_classes = (JSONParser,)
	serializer_class = UserSerializer
	permission_classes = [AllowAny]

	def create(self, request):
		serializer = self.serializer_class(data=request.data)
		
		status_code = status.HTTP_201_CREATED
		response_data = {}

		if not serializer.is_valid():
			response_data = serializer.errors
			status_code = status.HTTP_400_BAD_REQUEST
		else:
			serializer.save()
			response_data = serializer.data

		return Response(data=response_data, status=status_code)
