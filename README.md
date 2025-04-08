# kubeq
`kube` is a *diagnostic* tool for running queries on a k8s cluster across multiple resources types. It’s essentially a primitive but powerful query engine that runs locally.

It works by *reducing* its more complex query structure it into multiple simpler queries that the k8s API can digest, and then sending them all with a degree of parallelism.

This lets you answer such zany questions as:

- What’s in that namespace?
- What are all the flux resources in our cluster?
- Are there any resources that aren’t in a ready state?

Kubeq can result in an ungodly amount of stress on your control plane. Modern kubernetes versions support rate limiting by default, so most likely kubeq will just fail, but it also comes with its own safety features just in case.

You might also have to disable them.
# How it works
Kubeq uses queries that are very similar to what `kubectl get` supports, with a few exceptions:

1. There are actually two queries — a *kind query* and a *resource query*.
2. The *resource query* supports query operators for fields.
3. You can also query annotations.
4. It adds glob and regular expression operators to everything.

For example, here is how you can get a list of *all* Flux resources in your cluster that have a name starting with `the-awesome-` using the CLI:

```bash
kubeq get -k '*.fluxcd.io/*' -s 'name ~ the-awesome-*'
```

This query will return all the resources with any kind and version, and a resource 
group that ends with `fluxcd.io`. 

Under the hood, this query is processed as follows:

1. First, we retrieve all the registered resources from the control plane or use a cache.
2. We scan those resources to find matches for the glob under `-k`.
3. For each resource, we send a query with no selectors, since k8s doesn’t support globs.
4. We filter the results in memory based on the glob.
5. We print the results.

# Kind queries
Kind queries support just querying the resource kind identifier, which is the string that includes the kind, resource group, and version.

This is the string you get from `kubectl` that describes the resource you’re dealing with. Here are some examples:
```
git.source.toolkit.fluxcd.io/v1
kustomization.kustomize.config.k8s.io/v1beta1
```

You can use globs and regular expressions. Globs are used by default, and you can enable regex by surrounding the entire kind query with `/.../`. You don’t need to escape `/` inside the regex. 

Regardless of what you use, you have to match **the entire kind**.

Using the CLI:

```
-k '*.fluxcd.io/*'
-k '/.*\.fluxcd.io/.*/'
```
# Selectors
A selector narrows down the list of retrievable resources based on or more properties. Like `kubectl`, `kubeq` does not support disjunctions or unions. 

This means that you can’t query resources based on something like:

```
🚫 NOT POSSIBLE 🚫
field1 = 1 OR field2 = 1
```

Instead, multiple selectors combine using `AND`, just like when using `kubectl`. However, you can also use the `in` operator to match one of several complete literals.

```bash
-s 'name in (name1, name2, name3)'
```

As a general rule, it’s better to have **more selectors** than less, because it reduces the number of records that must be retrieved. The most performance intensive query is just:

```bash
😨 never do this!
kubeq get -k '*' -s 'name ~ *'
```

Which just retrieves **every single thing in the cluster**.

The properties you can use include the following:

1. Labels.
2. Annotations.
3. Resource-specific fields.

The type of property is determined by a *property prefix* which includes:

- Names of labels begin with `%`
- Names of annotations begin with `^`

If a property doesn’t have a prefix, it’s considered a field. 

You combine the property specifier with an operator. You can use one of the following operator structures:

```
%app = podinfo
^annotation != something
name in (one, two)
name not in (one, two)
name ~ gl?b
name ~ /regex/
```

## Passing down
kubeq will pass as much of your query as possible to the API, but a lot of things can’t be passed down. That includes:

1. Query operators on fields
2. Glob and regex matching.
3. Any selector on annotations, which can’t normally be queried.

When this happens, one of two things will happen:

- The query will be split into two queries that when combined result in what you asked for.
- The selector will be erased, which will cause the response to have extra results that need to be filtered out.

This means that a query that seems to have a lot of selectors might actually end up retrieving the entire cluster and sending hundreds of queries. There are some safety mechanisms in place, but it’s still a possibility.

To be clear, the strain on kubeq is less important than the strain this kind of thing puts on your control plane. 

## Combining selectors
You can combine multiple selectors on the command line using several `-s` flags, like this:

```bash
kubeq get -s '%app = thingy' -s '%whatever/hello-world = nope'
```

Remember, this **reduces** the number of results you’re going to get. You can even use several `-s` clauses on the same property if you want.

```bash
kubeq get -s 'name in (abba, arnold, zim, flouride)' -s 'name ~ a*'
```

# OOP API
kubeq is written in Python, and it supports a Pythonic OOP query API, including lots of type hints to make sure you’re using it right.

Here are some examples of it being used:

```python
from kubeq import KubeQ, SelectionFormula, Eq, Glob, In
client = KubeQ(context="minikube")
formula = SelectionFormula(
	{
		Kind("version"): Eq("v1") | Eq("v2"),
		Kind("ident"): Glob("P*"),
		Field("metadata.namespace"): In("default", "kube-system"),
	}
)
results = await client.query(formula)
for r in results:
	print(f"- {r.metadata.name}")

```

# 😨 Safety 
Kubeq is a tool that can end up pulling your entire cluster — or more likely tripping internal rate limiting and crashing itself. 

Some disclaimers:
- It only protects from individually large queries, not lots of people running queries at the same time.
- Kubernetes rate limiting is also a thing and probably does a better job.

There are two fairly primitive mechanisms.
1. A limit on the total number of queries
2. A limit on the total number of resources seen

The default limits are 100 requests and 500 resources seen. They can be configured using:

```
--max-resources 500
--max-requests 100
```

If your query exceeds the values, partial results will still be retrieved, with a message that further data might be available.

Besides these hard limits, there are extra mechanisms that affect query performance.

```
--reqs-per-minute 20
--reqs-parallel 5
```

These change number of requests per minute (completed or inflight) and number of parallel inflight requests.


# Why is this?
kubeq is an irresponsibly powerful tool for querying your k8s cluster. It arose from the need to answer one simple question:

> What the hell is in that namespace?

Kubernetes has a problem — while resources can be organized across many different hierarchies, its REST API allows you to query them across just one. Namely:

```
group → version → kind → namespace → name
```

No tool or dashboard lets you go around this hierarchy. It’s basically set in stone.

But you often do want to look at collections of different types of resources. Namespaces serve one organizational tool for doing so. 

You can create one, fill it with different resources, and then delete it — but there is no command that can tell you what the hell was in it.




