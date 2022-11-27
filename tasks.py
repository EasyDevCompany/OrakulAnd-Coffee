from celery import Celery
from app.core.containers import Container
from app.services.telegram_user_service import TelegramUserService
from app.services.users_limit_service import UserLimitService
from dependency_injector.wiring import Provide, inject
from datetime import datetime

app = Celery("tasks", broker="redis://app_redis/0")
app.config_from_object("celeryconfig")


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        60.0,
        check_user_limits.s(),
        name="check users limits"
    )


@app.task
@inject
def check_user_limits(
        telegram_user_service: TelegramUserService = Provide[Container.telegram_user_service],
        users_limits: UserLimitService = Provide[Container.users_limit_service]
):
    users = telegram_user_service.list_sync()
    for user in users:
        if users_limits.get_limit(user_id=user.user_id) <= datetime.today().date():
            users_limits.reset_limits(user_id=user.id)
