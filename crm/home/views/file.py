from django.apps import apps
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from home.models import File, FileStatus
from home.utils import get_object_or_none, upload_file


@api_view(("POST",))
def upload_files_to_google_drive(request: Request) -> Response:
    model_name = request.data.get("model", None)
    object_id = request.data.get("id", None)
    fields = request.data.getlist("fields[]")
    files = request.FILES.getlist("files[]")

    if not (model_name and object_id and files):
        return Response(
            {"error": "Missing required parameters"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        model = apps.get_model(app_label="home", model_name=model_name)
    except LookupError:
        return Response(
            {"error": f"Model '{model_name}' not found"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    object = get_object_or_none(model, pk=object_id)
    if not object:
        return Response(
            {"error": f"Object with ID {object_id} not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    for field_name, file in zip(fields, files):
        if not hasattr(object, field_name):
            return Response(
                {
                    "error": f"Field '{field_name}' does not exist on model '{model_name}'"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if getattr(object, field_name):
            setattr(object, field_name, None)

        try:
            url = upload_file(file)
            file_status = FileStatus.SUCCESS
        except Exception as e:
            file_status = FileStatus.FAILED

        setattr(
            object,
            field_name,
            File.objects.create(
                name=file.name,
                url=url,
                size=file.size,
                mime_type=file.content_type,
                status=file_status,
            ),
        )

    object.save()

    return Response({"message": "File uploaded"}, status=status.HTTP_201_CREATED)
