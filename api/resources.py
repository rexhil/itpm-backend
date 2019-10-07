# from import_export import fields, resources
# from import_export.widgets import ForeignKeyWidget
# from .models import InputData, Location, Attribute, RuleType, ReportTable, SummaryReport
#
#
# class InputDataResource(resources.ModelResource):
#     location = fields.Field(column_name='location', attribute='location',
#                             widget=ForeignKeyWidget(Location, 'location_name'))
#
#     attribute = fields.Field(column_name='attribute', attribute='attribute',
#                              widget=ForeignKeyWidget(Attribute, 'attribute_name'))
#
#     rule_type = fields.Field(column_name='rule_type', attribute='rule_type',
#                              widget=ForeignKeyWidget(RuleType, 'rule_type_name'))
#
#     class Meta:
#         model = InputData
#
#
# class ReportTableResources(resources.ModelResource):
#     location = fields.Field(column_name='location', attribute='location',
#                             widget=ForeignKeyWidget(Location, 'location_name'))
#
#     attribute = fields.Field(column_name='attribute', attribute='attribute',
#                              widget=ForeignKeyWidget(Attribute, 'attribute_name'))
#
#     rule_type = fields.Field(column_name='rule_type', attribute='rule_type',
#                              widget=ForeignKeyWidget(RuleType, 'rule_type_name'))
#
#     class Meta:
#         model = ReportTable
#
#
# class SummaryReportResources(resources.ModelResource):
#     location = fields.Field(column_name='location', attribute='location',
#                             widget=ForeignKeyWidget(Location, 'location_name'))
#
#     attribute = fields.Field(column_name='attribute', attribute='attribute',
#                              widget=ForeignKeyWidget(Attribute, 'attribute_name'))
#
#     rule_type = fields.Field(column_name='rule_type', attribute='rule_type',
#                              widget=ForeignKeyWidget(RuleType, 'rule_type_name'))
#
#     class Meta:
#         model = SummaryReport
