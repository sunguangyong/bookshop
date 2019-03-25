from django.db import models
from hashlib import sha1


class BaseModel(models.Model):
    """模型抽象基类"""

    id_delete = models.BooleanField(default=False, verbose_name="删除标记")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now_add=True, verbose_name="更新时间")

    class Meta:
        abstract = True


class Passport(BaseModel):
    """用户类模型"""

    username = models.CharField(max_length=20, verbose_name="用户名称")
    password = models.CharField(max_length=40, verbose_name="用户密码")
    email = models.EmailField(verbose_name="用户邮箱")
    is_active = models.BooleanField(default=False, verbose_name="激活状态")

    # 用户表管理器
    objects = PassportManger()

    class Meta:
        db_table = "s_user_accout"


class PassportManger(models.Manager):

    def ad_one_passport(self, username, password, email):
        """添加一个账户信息"""
        passport = self.create(username=username, password=get_hash(password))
        return passport

    def get_one_password(self, username, password):
        """根据用户名查找账户信息"""

        try:
            passport = self.get(username=username, password=get_hash(password))
        except self.model.DoesNotExist:
            passport = None
        return passport


def get_hash(str):
    sh = sha1()
    sh.update(str.encode("utf8"))
    return sh.hexdigest()
