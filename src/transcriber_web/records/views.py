from django.views import View
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from transcriber_web.services import ServiceContainer
from accounts.utils import LoginRequiredMixin
from .forms import AudioUploadForm

container = ServiceContainer()


class AudioUploadView(LoginRequiredMixin, View):
    template_name = "records/upload.html"
    form_class = AudioUploadForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            file = request.FILES["file"]
            fs = FileSystemStorage(location="media/audio")
            filename = fs.save(file.name, file)
            file_path = fs.path(filename)

            storage = container.storage_service.get_user_storage(request.user.id)
            if not storage:
                storage = container.storage_service.create_storage(request.user.id)

            with open(file_path, "rb") as f:
                content = f.read()

            container.audio_record_service.create_audio(
                file_name=file.name,
                content=content,
                file_path=file_path,
                storage_id=storage.id,
                language=form.cleaned_data["language"],
                max_speakers=form.cleaned_data["max_speakers"],
                main_theme=form.cleaned_data["main_theme"],
            )
            return redirect(reverse_lazy("profile"))

        return render(request, self.template_name, {"form": form})


class RecordListView(LoginRequiredMixin, View):
    template_name = "records/record_list.html"

    def get(self, request):
        storage = container.storage_service.get_user_storage(request.user.id)
        records = (
            container.audio_record_service.get_records(storage.id) if storage else []
        )
        return render(request, self.template_name, {"records": records})


class RecordDetailView(LoginRequiredMixin, View):
    template_name = "records/record_detail.html"

    def get(self, request, record_id):
        record = container.audio_record_service.get_by_id(record_id)
        if (
            not record
            or record.storage_id
            != container.storage_service.get_user_storage(request.user.id).id
        ):
            return render(
                request,
                self.template_name,
                {"error": "Запись не найдена или недоступна"},
            )
        return render(request, self.template_name, {"record": record})

    def post(self, request, record_id):
        action = request.POST.get("action")
        record = container.audio_record_service.get_by_id(record_id)
        if (
            not record
            or record.storage_id
            != container.storage_service.get_user_storage(request.user.id).id
        ):
            return render(
                request,
                self.template_name,
                {"error": "Запись не найдена или недоступна"},
            )

        try:
            if action == "add_tag":
                tag = request.POST.get("tag")
                container.audio_tag_service.add_tag_to_record(record_id, tag)
            elif action == "remove_tag":
                tag = request.POST.get("tag")
                container.audio_tag_service.remove_tag_from_record(record_id, tag)
            elif action == "remove_stopwords":
                container.audio_text_service.remove_stopwords(
                    record_id, remove_swear_words=True
                )
            elif action == "export":
                fs = FileSystemStorage(location="media/exports")
                container.audio_text_service.export_record_text(
                    record_id, fs.base_location, "docx"
                )
                return redirect(reverse_lazy("record_list"))
            elif action == "rename":
                name = request.POST.get("name")
                container.audio_text_service.change_record_name(record_id, name)
        except ValueError as e:
            return render(
                request, self.template_name, {"record": record, "error": str(e)}
            )

        return redirect(reverse_lazy("record_detail", kwargs={"record_id": record_id}))
