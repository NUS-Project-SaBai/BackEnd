# 🛠️ Backend Architecture Guide

This document serves as a guide for developers contributing to the Sabai backend after our major refactor based on the [HackSoft Django Styleguide](https://github.com/HackSoftware/Django-Styleguide). It explains:

* What changes were made
* Best practices and rationale
* Common gotchas to avoid
* How to write new model pipelines (Model ➝ Serializer ➝ Service ➝ View ➝ URL)

---

## ✅ Key Changes

### 1. 📁 Modular `routes/` Directory for URLs

**Old:** All routes in a single `urls.py` file.

**New:**

* Routes are split by feature/module under `api/routes/`:

  ```py
  # api/routes/patients.py
  urlpatterns = [
      path("", PatientView.as_view()),
      path("<int:pk>/", PatientView.as_view()),
  ]
  ```

* Main `api/urls.py` includes:

  ```py
  from api.routes import patients, visits, vitals

  urlpatterns = [
      path("patients/", include(patients.urlpatterns)),
      path("visits/", include(visits.urlpatterns)),
      ...
  ]
  ```

**Rationale:** Easier to maintain and extend, cleaner separation of concerns.

---

### 2. 💡 Dual-Field Pattern in Serializers

**When you want both:**

* To accept an FK ID on `POST/PATCH`
* To return nested serialized data on `GET`

**Use this pattern:**

```py
consult_id = serializers.PrimaryKeyRelatedField(
    source="consult",
    queryset=Consult.objects.all(),
    write_only=True,
)
consult = ConsultSerializer(read_only=True)
```

**Rationale:** This avoids overriding `to_representation` manually. Clear input/output separation.

**Naming convention:**
If you're only sending an FK, name it `xxx_id`:

```json
{ "consult_id": 4 }  # ✅ good
{ "consult": 4 }     # 🚫 unclear/ambiguous
```

---

### 3. 🧠 Introduced Service Layer

Business logic is extracted from views into `api/services/`, for example:

```py
# services/patients_service.py

def create_patient(data, face_encoding):
    return Patient.objects.create(**data, face_encodings=face_encoding)
```

**Views now delegate like this:**

```py
from api.services import patients_service

patient = patients_service.create_patient(data, encoding)
```

**Rationale:** Keeps views simple and readable. Business logic is testable and reusable.

---

## ⚠️ Things to Watch Out For

### 🔗 Forward Slash Required

**Always end API URLs with a `/`.**

**Why?** Django auto-redirects if you forget it, but query parameters like `?visit=4` can get lost in the redirect.

```bash
# 🚫 Will likely break:
curl http://localhost:8000/vitals?visit=4

# ✅ Always use:
curl http://localhost:8000/vitals/?visit=4
```

### 🧼 Clean Partial Update Requests

When patching:

* Filter out empty fields before sending.
* Especially important for numeric/optional fields in PATCH.

Example (JS):

```ts
const payload = Object.fromEntries(
  Object.entries(vital).filter(([, v]) => v !== "" && v !== undefined)
);
```

### 🤔 Don't Trust `request.data["xxx"]`

Use `.get()` with fallback or validations where necessary. DRF `request.data` may wrap file uploads or non-primitives.

---

## 🧱 How to Create a New Pipeline (Model ➝ Endpoint)

Let's say you're adding a `LabResult` model.

### 1. Create the Model

```py
# models/lab_result.py
class LabResult(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    hemoglobin = models.DecimalField(...)
    glucose = models.DecimalField(...)
```

### 2. Add Serializer

```py
# serializers/lab_result_serializer.py
class LabResultSerializer(serializers.ModelSerializer):
    visit_id = serializers.PrimaryKeyRelatedField(source="visit", queryset=Visit.objects.all(), write_only=True)
    visit = VisitSerializer(read_only=True)

    class Meta:
        model = LabResult
        fields = "__all__"
```

### 3. Write Service

```py
# services/lab_results_service.py

def list_lab_results():
    return LabResult.objects.all()

def get_lab_result(pk):
    return get_object_or_404(LabResult, pk=pk)
```

### 4. Create View

```py
# views/lab_results_view.py
class LabResultView(APIView):
    def get(self, request, pk=None):
        ...
    def post(self, request):
        ...
```

### 5. Add Route

```py
# routes/lab_results.py
urlpatterns = [
    path("", LabResultView.as_view()),
    path("<int:pk>/", LabResultView.as_view()),
]

# api/urls.py
from api.routes import lab_results
path("lab-results/", include(lab_results.urlpatterns)),
```

---

## ✅ Conclusion

With this new architecture, the backend is now:

* Cleaner to navigate
* Easier to debug and extend
* Ready for scalable growth

Use this guide whenever you:

* Add a new feature
* Extend an existing model
* Refactor for clarity
