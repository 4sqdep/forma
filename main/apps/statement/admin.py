from django.contrib import admin
from ..statement.models.statement import Statement
from ..statement.models.statement_information import StatementInformation



admin.site.register(Statement)
admin.site.register(StatementInformation)
