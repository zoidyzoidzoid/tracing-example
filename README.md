# Tracing Examples

At the moment this repo just has some Django projects and some Python to
add other things to OpenCensus and try upstream them, whenever I
realise there is an integration that would be nice.

I'll probably use this code as examples in a blog post coming soon. :tm:

`prometheus/` and `docker-compose.yml` come from [docker-zipkin](https://github.com/openzipkin/docker-zipkin)

## Example Django Project

![image](https://user-images.githubusercontent.com/2572493/47270938-28f68500-d573-11e8-87d2-4ef01d73122c.png)

With a frontend that talks to an API that fetches the weather from a third party API.

I'll probably flesh it out some more to have some good examples for a
monolith and a service orientated architecture.

What it does so far:
- [x] HTTP Propogation (consuming a trace ID)
- [x] HTTP Propogation (propagating a trace ID), which I didn't think
      I'd need to manually enable. See [this code](https://github.com/zoidbergwill/tracing-example/commit/eeeb1ecbd488def16a4593a57eb0318042398444#diff-ab3e6505f8e871d26d09934adae619e0R27)
- [ ] Integrations
  - [x] DB
        [Census Related Issue](https://github.com/census-instrumentation/opencensus-python/issues/356)
  - [ ] Cache
  - [x] HTTP client
  - [ ] Celery integration: [Custom BaseTask](http://docs.celeryproject.org/en/latest/userguide/tasks.html#task-inheritance)
        [Census Related Issue](https://github.com/census-instrumentation/opencensus-python/issues/357)
  - [ ] Kafka integration

Tools:

- [ ] logs
- [ ] stats
- [x] tracing: Zipkin integration

At the moment, we support tracing via the Zipkin exporter, which POSTs directly to Zipkin, but in a bigger scale system you might want something like exporting to Kafka or in the future [openensus-service](https://github.com/census-instrumentation/opencensus-service), which can write to Zipkin directly or Kafka, and can be scraped by Prometheus, which is very useful in a world with short-lived processes like Python or PHP.

If you have any suggestions for integrations or use cases to test,
please feel free to [file an issue](https://github.com/zoidbergwill/tracing-example/issues/new)
