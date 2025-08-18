from api.models import MedicationReview, Order
from collections import defaultdict

def get_medication_history_viewmodel(medicine_id: int):
    medication_reviews = MedicationReview.objects.filter(medicine_id=medicine_id).order_by("-date")
    
    medication_history = []
    
    for mr in medication_reviews:
        order = Order.objects.filter(medication_review=mr).first()
        doctor_name = "-"
        patient_name = "-"
        
        if order and order.consult:
            doctor_name = order.consult.doctor.nickname if order.consult.doctor else "-"
            patient_name = order.consult.visit.patient.name if order.consult.visit and order.consult.visit.patient else "-"
        
        medication_history.append({
            "approval_name": getattr(mr.approval, "name", "-") if mr.approval else "-",
            "doctor_name": doctor_name,
            "patient_name": patient_name,
            "qty_changed": mr.quantity_changed,
            "qty_remaining": mr.quantity_remaining,
            "date": mr.date.isoformat() if mr.date else None,
        })
    
    return medication_history
