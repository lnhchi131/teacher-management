from ..models.teaching_rate_model import get_teaching_rate, update_teaching_rate

def get_rate_data():
    return get_teaching_rate()

def update_rate_data(form_data):
    amount = float(form_data['amount'])
    update_teaching_rate(amount)
    return True