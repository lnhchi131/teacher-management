from ..models.class_coefficients_model import (
    get_class_coefficients, add_class_coefficient, update_class_coefficient, delete_class_coefficient
)

def get_class_coefficients_data():
    return get_class_coefficients()

def add_class_coefficient_data(form_data):
    add_class_coefficient(
        int(form_data['min_students']),
        int(form_data['max_students']),
        float(form_data['coefficient'])
    )
    return True

def update_class_coefficient_data(form_data):
    update_class_coefficient(
        int(form_data['id']),
        int(form_data['min_students']),
        int(form_data['max_students']),
        float(form_data['coefficient'])
    )
    return True

def delete_class_coefficient_data(id):
    delete_class_coefficient(id)
    return True