# About kr8s and invoking the k8s API

Kr8s is a Pythonic API client for kubernetes. It's a pretty high-level client that
supports objects for some k8s resources.

However, it's not very good at resource discovery and it doesn't know about the
aggregated API discovery endpoints.

So I have to make it use them. Unfortunately, it can't do requests to arbitrary URLs
either, which is why I have to monkey patch one of the private methods to support it.

I would stop using it entirely, but it still handles some pretty useful stuff like:

1. Authentication
2. Retries
3. SSL-related stuff
4. Handling status codes

Ideally, there would be a separate lower-level component that just does that, which is an
idea for a future project. But right now I don't feel like implementing any of it,
so I'm going to piggy back on kr8s and use its lower-level API in this weird way.
