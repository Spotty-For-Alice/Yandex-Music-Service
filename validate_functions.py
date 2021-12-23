# from marshmallow import ValidationError
#
# # from models.accounts import User
#
#
# def validate_service_name(service_name):
#     if service_name not in ['spotify', 'apple']:
#         raise ValidationError("Неправильное название сервиса - ожидается spotify/apple")
#
#
# def validate_user_exist(login):
#     user = User.query.filter_by(login=login).first()
#     if user:
#         raise ValidationError("Пользователь с таким логином уже зарегистрирован в сервисе Yandex")
#
#
# def validate_exist_user_by_id(user_id):
#     user = User.query.filter_by(id=user_id).first()
#     if not user:
#         raise ValidationError(f"Пользователь с id={user_id} не существует")