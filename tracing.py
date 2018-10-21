# coding=utf-8
# class HoneyDBWrapper(object):
#
#     def __call__(self, execute, sql, params, many, context):
#         vendor = context['connection'].vendor
#         trace_name = "django_%s_query" % vendor
#
#         with beeline.tracer(trace_name):
#             beeline.add_context({
#                 "type": "db",
#                 "db.query": sql,
#                 "db.query_args": params,
#             })
#
#             try:
#                 db_call_start = datetime.datetime.now()
#                 result = execute(sql, params, many, context)
#                 db_call_diff = datetime.datetime.now() - db_call_start
#                 beeline.add_context_field(
#                     "db.duration", db_call_diff.total_seconds() * 1000)
#             except Exception as e:
#                 beeline.add_context_field("db.error", str(type(e)))
#                 beeline.add_context_field("db.error_detail", str(e))
#                 raise
#             else:
#                 return result
#             finally:
#                 if vendor == "postgresql" or vendor == "mysql":
#                     beeline.add_context({
#                         "db.last_insert_id": context['cursor'].cursor.lastrowid,
#                         "db.rows_affected": context['cursor'].cursor.rowcount,
#                     })
#
#
# class CensusDBMiddleware(object):
#     def __call__(self, request):
#         try:
#             db_wrapper = HoneyDBWrapper()
#             # db instrumentation is only present in Django > 2.0
#             with connection.execute_wrapper(db_wrapper):
#                 response = self.create_http_event(request)
#         except AttributeError:
#             response = self.create_http_event(request)
#
#         return response
#
from django.db import connection
from opencensus.trace import span as span_module
from opencensus.trace import execution_context
from opencensus.trace.ext.django.middleware import OpencensusMiddleware


# Based on https://github.com/opencensus-integrations/ocsql/blob/master/driver.go#L186
# MODULE_NAME = 'sql'


class CensusDBMiddleware(OpencensusMiddleware):
    def process_request(self, request):
        connection.execute_wrappers.append(self.trace_db_call)
        return super(CensusDBMiddleware, self).process_request(request)

    def trace_db_call(self, execute, sql, params, many, context):
        print(context['connection'])
        print(context['cursor'])
        _tracer = execution_context.get_opencensus_tracer()
        if _tracer is not None:
            if many:
                method_name = 'executemany'
            else:
                method_name = 'execute'
            db_type = context['connection'].vendor
            # Note that although get_opencensus_tracer() returns a NoopTracer
            # if no thread local has been set, set_opencensus_tracer() does NOT
            # protect against setting None to the thread local - be defensive
            # here
            _span = _tracer.start_span()
            _span.name = '{}.query'.format(db_type)
            _span.span_kind = span_module.SpanKind.CLIENT
            _tracer.add_attribute_to_current_span(
                '{}.query'.format(db_type), sql)
            _tracer.add_attribute_to_current_span(
                '{}.cursor.method.name'.format(db_type), method_name)

        result = execute(sql, params, many, context)

        if _tracer is not None:
            _tracer.end_span()

        return result
