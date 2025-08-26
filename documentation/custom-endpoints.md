# Custom “Patient Records” endpoint — decisions & structure

## Route grouping (URLs)

* All API routes are grouped under `/api/` via `api/urls.py`.
* Feature routes live in `api/routes/<feature>.py` and are included with a **prefix** in `api/urls.py`.

```python
# api/urls.py (excerpt)
urlpatterns = [
    path("test/", include(("api.routes.test", "test"))),
    path("medication/", include(("api.routes.medication", "medication"))),
    ...
    # CUSTOM ENDPOINTS
    path("patient_records/", include(("api.routes.patient_records", "patient_records"))),
]
```

```python
# api/routes/patient_records.py
from django.urls import path
from api.views.patient_records_view import PatientRecordsView

urlpatterns = [
    path("", PatientRecordsView.as_view(), name="patient_records"),
]
```

This yields the final endpoint:

```
GET /api/patient_records/?visit=<visit_id>/
```

**Why:** one place (api/urls.py) to manage `api/` prefix; each feature owns its own mini `urlpatterns`. Scales cleanly and avoids repeating `"api/"` everywhere.

---

## View → Service → ViewModel → Serializer

We deliberately split responsibilities:

### 1) View (request/response orchestration only)

`api/views/patient_records_view.py`

```python
class PatientRecordsView(APIView):
    def get(self, request):
        visit_id = request.query_params.get("visit")
        if not visit_id:
            return Response({"error": "Missing visit param"}, status=400)

        vm = get_patient_record_viewmodel(visit_id)
        serialized = PatientRecordsOutputSerializer(vm)
        return Response(serialized.data)
```

**Why:**

* The view parses input (query param), calls the service, and serializes the **result**.
* No DB logic and no heavy shaping in the view.

---

### 2) Service (fetch data only)

`api/services/patient_records_service.py`

```python
def get_patient_record_viewmodel(visit_id) -> PatientRecordViewModel:
    visit = visit_service.get_visit(pk=visit_id)
    if not visit:
        return None

    patient = visit.patient
    vitals = vitals_service.list_vitals(visit_id=visit_id).first()
    consults = consult_service.list_consults(visit_id=visit.pk)
    prescriptions = Order.objects.filter(consult__visit=visit).select_related(
        "medication_review__medicine"
    )

    return PatientRecordViewModel(patient, vitals, visit, consults, prescriptions)
```

**Why:**

* The service **only queries and aggregates model instances**.
* We keep presentation concerns out of the service, but **we do** return a single cohesive object (the ViewModel) that the serializer can consume.

---

### 3) ViewModel (bridge between domain objects and output)

`api/viewmodels/patient_records_viewmodel.py`

```python
class PatientRecordViewModel:
    def __init__(self, patient, vitals, visit, consults, prescriptions):
        self.patient = patient
        self.vitals = vitals
        self.visit_date = visit.date
        self.consults = consults
        self.prescriptions = [
            {
                "consult_id": order.consult_id,
                "visit_date": order.consult.visit.date,
                "medication": (
                    order.medication_review.medicine.medicine_name
                    if order.medication_review and order.medication_review.medicine
                    else None
                ),
                "quantity": (
                    order.medication_review.quantity_changed
                    if order.medication_review
                    else None
                ),
                "notes": order.notes,
                "status": (
                    order.medication_review.order_status
                    if order.medication_review
                    else "UNKNOWN"
                ),
            }
            for order in prescriptions
        ]
```

**Why:**

* This is the “ViewModel": a read‑only, page‑specific shape composed from multiple models.
* It removes formatting from the view and keeps the service clean, while giving the serializer a stable object to represent.

---

### 4) Output Serializer (explicit, page‑specific)

`api/serializers/patient_records_serializer.py`

```python
class DoctorMiniSerializer(serializers.Serializer):
    nickname = serializers.CharField()

class ConsultMiniSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    date = serializers.DateTimeField()
    doctor = DoctorMiniSerializer()
    referred_for = serializers.CharField()

class PrescriptionMiniSerializer(serializers.Serializer):
    consult_id = serializers.IntegerField()
    visit_date = serializers.DateTimeField()
    medication = serializers.CharField()
    quantity = serializers.IntegerField()
    notes = serializers.CharField()
    status = serializers.CharField()

class PatientRecordsOutputSerializer(serializers.Serializer):
    patient = PatientSerializer()
    vitals = VitalsSerializer(allow_null=True)
    visit_date = serializers.DateTimeField()
    consults = serializers.ListSerializer(child=ConsultMiniSerializer())
    prescriptions = serializers.ListSerializer(child=PrescriptionMiniSerializer())
```

**Why:**

* HackSoft style: **explicit, operation‑specific** serializers (no `ModelSerializer` here).
* Clear contract that matches the frontend’s expected JSON.
* Easy to evolve per page without touching core CRUD serializers.

---

## Conventions we followed

1. **Trailing slashes**
   All routes end with `/` and clients must call `/api/.../`

2. **Query params for filtering on reads**
   We use `?visit=<id>` to select which record bundle to return.
   (Writes continue to use body payloads with `*_id` fields.)

3. **ViewModel for page endpoints**

   * Use a small class to assemble a page‑specific shape from multiple models.
   * Keep it **read‑only** and scoped to the endpoint.
   * Let the serializer handle final representation.

4. **Services return domain objects**
   Services query and aggregate; they don’t serialize or build API dicts.
   (The one exception here is that our ViewModel constructor does some safe flattening for prescriptions to avoid repeated lookups in the serializer; that’s fine because it keeps the service thin and the serializer explicit.)

5. **Performance**
   Use `select_related("medication_review__medicine", "consult__visit")` to avoid N+1s.

6. **Field naming for writes (elsewhere)**
   When endpoints accept only an ID for a relation, prefer the dual‑field pattern on write endpoints:

   * `thing_id = PrimaryKeyRelatedField(source="thing", write_only=True)`
   * `thing = ThingSerializer(read_only=True)`
     For **read‑only** page endpoints like this one, explicit output serializers are enough.

---

## How to create a custom endpoint

1. **Create a route file**: `api/routes/<feature>.py` with `path("", <View>.as_view(), name="<feature>")`.
2. **Add it to `api/urls.py`** with a prefix (`path("<feature>/", include(...))`).
3. **Write a service function** to fetch domain objects only.
4. **Define a ViewModel** that represents exactly what the page needs.
5. **Add an OutputSerializer** (explicit fields) to represent the ViewModel.
6. **Write the View**: parse query params, call service, serialize ViewModel, return `Response`.
7. **Tune performance** with `select_related/prefetch_related` for any relationships you access.
8. **Keep CRUD endpoints separate** for general data operations.
